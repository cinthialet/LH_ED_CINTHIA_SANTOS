"""
Este script define um DAG (Directed Acyclic Graph) para o Apache Airflow, organizando uma pipeline de ETL
(Extração, Transformação e Carga) que opera em um ciclo diário. O DAG é projetado para lidar com dados de
diferentes fontes, organizar esses dados em uma estrutura de diretórios diariamente versionada e, finalmente,
executar tarefas de ETL para processamento e armazenamento em um banco de dados PostgreSQL. Abaixo estão os
principais passos e características do DAG:

1. Criação de Diretórios Diários: A cada execução, baseada no calendário diário ('{{ ds }}'), o DAG cria
   novos diretórios para armazenar os dados extraídos do dia. Isso assegura que os dados de cada dia sejam
   mantidos de forma isolada, permitindo um rastreamento fácil e uma organização clara baseada em datas.

2. Listagem de Fontes de Dados: Identifica todas as fontes de dados disponíveis em um diretório específico.
   Esta etapa é crucial para adaptar a pipeline a novas fontes de dados que podem ser adicionadas dinamicamente.

3. Configuração e Execução de Extratores Meltano: Para cada fonte de dados identificada, configura e executa
   extratores específicos utilizando Meltano. Estas tarefas são parametrizadas para armazenar os dados no
   diretório apropriado, que é versionado por data.

4. Escrita de Arquivo de Configuração JSON: Após a extração, um arquivo de configuração JSON é gerado
   contendo os caminhos atualizados dos dados extraídos. Este arquivo é usado nas etapas subsequentes para
   referenciar corretamente os dados no processo de carga.

5. Configuração de Caminho de Destino com Meltano: Define o caminho de destino para a etapa final de carga,
   assegurando que os dados consolidados sejam armazenados no local correto.

6. Execução Final do Meltano para Carga no PostgreSQL: Executa a tarefa final de ETL que consolida todos os
   dados extraídos e os carrega no PostgreSQL, completando o ciclo de ETL.

O DAG está configurado para não executar retroativamente ('catchup=False'), iniciando a partir de uma data
específica ('start_date'). Além disso, cada tarefa é configurada com tentativas de repetição em caso de falhas,
utilizando um atraso definido entre tentativas ('retry_delay') para gerenciar dependências e falhas de forma
eficaz.

Esta abordagem de versionamento diário e organização, juntos com os blocos try-catch para cuidar de error e os 
prints para acompanhar o processo, permitem uma rastreabilidade completa dos dados e facilita intervenções manuais 
ou auditorias, se necessário.
"""


import os
import json
from airflow.models.dag import DAG
from airflow.models import Variable
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def criar_pasta_data_atual(data_atual):
    folder_path = Variable.get('folder_path')
    postgres_path = os.path.join(folder_path, 'data/postgres-northwind')
    tabelas_postgres = os.listdir(postgres_path)
    csv_path = os.path.join(folder_path, 'data/csv/order_details', data_atual)
    os.makedirs(csv_path, exist_ok=True)
    print(f"Pasta para CSV criada em: {csv_path}")
    for nome_tabela in tabelas_postgres:
        tabela_path = os.path.join(postgres_path, nome_tabela, data_atual)
        os.makedirs(tabela_path, exist_ok=True)
        print(f"Pasta para tabela {nome_tabela} criada em: {tabela_path}")

def listar_fontes():
    folder_path = Variable.get('folder_path')
    dados_path = os.path.join(folder_path, 'data')
    diretorios_dados = os.listdir(dados_path)
    fontes = []
    for diretorio in diretorios_dados:
        diretorio_path = os.path.join(dados_path, diretorio)
        if os.path.isdir(diretorio_path):
            fonte_path = os.listdir(diretorio_path)
            for path in fonte_path:
                fonte = os.path.join(diretorio, path)
                fontes.append(fonte)
    print("Listagem de fontes de dados concluída.")
    return fontes

def criar_arquivo_configuracao(destino_arquivo):
    folder_path = Variable.get('folder_path')
    config_path = os.path.join(folder_path, "indicium-challenge/config.json")
    with open(config_path, "w") as arquivo_config:
        json.dump(destino_arquivo, arquivo_config)
    print("Arquivo de configuração criado com sucesso.")

argumentos_padrao = {
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "dag_indicium_challenge",
    description="Pipeline de orquestracao do teste tecnico Indicium",
    schedule=timedelta(days=1),
    start_date=datetime(2024, 6, 1),
    catchup=False,
) as dag:

    task_criar_pastas = PythonOperator(
        task_id="criar_pastas_por_dia",
        python_callable=criar_pasta_data_atual,
        op_kwargs={'data_atual': '{{ ds }}'}
    )

    fontes = listar_fontes()
    tasks_meltano = []
    config_final_csv = []
    data_execucao = '{{ ds }}'
    for fonte in fontes:
        nome_fonte = fonte.split('/')[-1]
        step_definir_destino = BashOperator(
            task_id=f"definir_path_destino_{nome_fonte}",
            bash_command=f"source /home/bruna/LH_ED_CINTHIA_SANTOS/meltano_venv/bin/activate && "
                         f"meltano --cwd /home/bruna/LH_ED_CINTHIA_SANTOS/indicium-challenge config target-{nome_fonte} "
                         f"set destination_path ../data/{fonte}/{data_execucao}",
            cwd="/home/bruna/LH_ED_CINTHIA_SANTOS/indicium-challenge"
        )
        step_executar_meltano = BashOperator(
            task_id=f"executar_extrator_{nome_fonte}",
            bash_command=f"source /home/bruna/LH_ED_CINTHIA_SANTOS/meltano_venv/bin/activate && "
                         f"meltano --cwd /home/bruna/LH_ED_CINTHIA_SANTOS/indicium-challenge run tap-{nome_fonte} target-{nome_fonte}",
            cwd="/home/bruna/LH_ED_CINTHIA_SANTOS/indicium-challenge"
        )
        tasks_meltano.append([step_definir_destino, step_executar_meltano])
        config_final_csv.append({"entity": nome_fonte, "path": f"../data/{fonte}/{data_execucao}"})

    task_criar_arquivo_config = PythonOperator(
        task_id="criar_arquivo_json",
        python_callable=criar_arquivo_configuracao,
        op_kwargs={"destino_arquivo": config_final_csv}
    )

    step_definir_arquivos = BashOperator(
        task_id="definir_arquivos",
        bash_command=f"source /home/bruna/LH_ED_CINTHIA_SANTOS/meltano_venv/bin/activate && "
                     f"meltano --cwd /home/bruna/LH_ED_CINTHIA_SANTOS/indicium-challenge config tap-destinos "
                     f"set csv_files_definition config.json",
        cwd="/home/bruna/LH_ED_CINTHIA_SANTOS/indicium-challenge"
    )

    step_executar_meltano_final = BashOperator(
        task_id="executar_extrator_final",
        bash_command=f"source /home/bruna/LH_ED_CINTHIA_SANTOS/meltano_venv/bin/activate && "
                     f"meltano --cwd /home/bruna/LH_ED_CINTHIA_SANTOS/indicium-challenge run tap-destinos target-postgres",
        cwd="/home/bruna/LH_ED_CINTHIA_SANTOS/indicium-challenge"
    )

    for task in tasks_meltano:
        task_criar_pastas >> task[0]
        task[0] >> task[1]  
        task[1] >> task_criar_arquivo_config
    
    task_criar_arquivo_config >> step_definir_arquivos >> step_executar_meltano_final
