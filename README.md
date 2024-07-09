## Veja meus projetos similares ao desafio :D

> Acesse **[aqui](https://acesse.one/datalake-linkedin](https://www.linkedin.com/feed/update/urn:li:activity:7135251028911751170/)** para ver a demonstração de um dos meus projetos similar ao caso de estudo, feito na cloud AWS - Datalake e Data warehouse com pipeline automatizada com Glue Workflow.

# Desafio de Data Engineering do Programa LIGHTHOUSE

## Introdução

Neste desafio, desenvolvi um pipeline para extrair dados diariamente de um banco de dados `northwind` no PostgreSQL e de um arquivo CSV. O banco de dados Northwind não contém a tabela `order_details`, representada pelo arquivo CSV fornecido. O pipeline grava os dados extraídos no disco local e, em seguida, carrega-os em um novo banco de dados no PostgreSQL (`processed-northwind`) que eu criei, junto com as tabelas necessárias para receber os dados.

O objetivo final é combinar os pedidos (`orders` do PostgreSQL) com seus detalhes (`order_details` do CSV) em uma consulta unificada.

## Ferramentas Utilizadas

Para completar este desafio, utilizei as seguintes ferramentas integradas:

- **Meltano e Airflow**: Meltano foi usado para gerenciar a extração e carga de dados das fontes, enquanto o Airflow orquestrou e agendou as tarefas do pipeline.
- **Docker, Docker-compose e PostgreSQL**: O Postgres foi implementado dentro de um container docker, e orquestrado usando o docker-compose.

## Preparação do Ambiente e Instalação

### Parte 1: Fork e Clone

Foi feito o fork do repositório do desafio e depois o clone para o ambiente local.

### Parte 2: Criação de Dois Ambientes Virtuais

**Motivo:** Devido a conflitos de dependências entre o Airflow e o Meltano, foi necessário configurar ambientes virtuais separados para garantir a compatibilidade das bibliotecas .

- Conflito entre as versões necessárias do SQLAlchemy para ambas as ferramentas:
  > ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.limits 3.7.0 requires packaging<24,>=21, but you have packaging 24.1 which is incompatible.apache-airflow 2.8.1 requires sqlalchemy<2.0,>=1.4.28, but you have sqlalchemy 2.0.31 which is incompatible.flask-appbuilder 4.3.10 requires SQLAlchemy<1.5, but you have sqlalchemy 2.0.31 which is incompatible.

**Criando e ativando o ambiente - Meltano:**

python3 -m venv meltano_venv

source meltano_venv/bin/activate

**Criando e ativando o ambiente -Airflow:**

python3 -m venv airflow_venv

source airflow_venv/bin/activate

### Parte 3: Instalação do Meltano e Airflow com PIP em seus respectivos ambientes virtuais

pip install meltano==3.4.2

pip install "apache-airflow[celery]==2.8.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.8.txt"

### Parte 4: Criação do projeto Meltano e instalação dos plugins

- Projeto: indicium_challenge
- Plugins instalados:
  - meltano add extractor tap-csv - Extrai dados de arquivos csv
  - meltano add extractor tap-postgres - Extrai dados de um banco de dados no Postgres
  - meltano add loader target-csv - Carrega dados para arquivos csv
  - meltano add loader target-postgres - Carrega dados para um banco de dados no Postgres

### Parte 5: Instalação e Execução do Docker e docker-compose para subir os bancos de dados PostgreSQL em um container

sudo docker-compose up -d

## Desenvolvendo o Projeto

### Configuração do Meltano

#### Configuração do extractor CSV e PostgreSQL:

- Acessei o arquivo `meltano.yml` para realizar configurações diretamente.
- Especifiquei entidades, paths de arquivos, keys e configurações de banco de dados dentro do `meltano.yml`.
- Criação do novo banco de dados com as tabelas necessárias usando o script **[processed_northwind.sql](link-para-scrip-sql)**

Essas configurações foram necessárias para definir claramente as fontes de dados e garantir que os dados sejam extraídos corretamente de cada fonte e carregados para o destino correto, além de conectar com o banco de dados corretamente.

### Criação da DAG no Airflow

O DAG foi configurado no Apache Airflow para operar em um ciclo diário, lidando com dados de diferentes fontes e organizando esses dados em uma estrutura de diretórios diariamente versionada. O script da DAG pode ser encontrado **[AQUI](link-python-dag)**

Abaixo estão os principais passos e características do DAG:

1. **Criação de Diretórios Diários:**

   - A função `criar_pasta_data_atual` cria novos diretórios a cada execução diária para armazenar os dados extraídos do dia. Isso assegura que os dados de cada dia sejam mantidos de forma isolada e versionados pelo dia da execução da pipeline, permitindo um rastreamento fácil e uma organização clara baseada em datas.
     - Ex: data/postgres-northwind/categories/2024-07-09/public-categories.csv

2. **Listagem de Fontes de Dados:**

   - A função `listar_fontes` identifica todas as fontes de dados disponíveis em um diretório específico, permitindo adaptar a pipeline a novas fontes de dados dinamicamente. No caso, tenho duas fontes - csv e postgres.

3. **Configuração e Execução de Extratores Meltano:**

   - Para cada fonte de dados identificada, o DAG configura e executa extratores específicos utilizando Meltano, armazenando os dados no diretório apropriado, versionado por data. Essa etapa assegura que cada fonte de dados é processada corretamente e seus dados são organizados de forma eficiente. Os comandos do meltano foram automatizados usando operadores BASH no DAG.

4. **Escrita de Arquivo de Configuração JSON:**

   - Após a extração, a função `criar_arquivo_configuracao` gera um arquivo de configuração JSON contendo os caminhos atualizados dos dados extraídos. Este arquivo é utilizado nas etapas subsequentes para referenciar corretamente os dados no processo de carga.

5. **Configuração de Path de Destino com Meltano:**

   - Define o path de destino para a etapa final de carga, assegurando que os dados consolidados sejam armazenados no local correto. Com isso, os dados são carregados do Postgres para o ambiente local, como determinado pelo step1 da pipeline.

6. **Execução Final do Meltano para Carga no PostgreSQL:**
   - Executa a tarefa final de ETL que consolida todos os dados extraídos e os carrega no PostgreSQL, completando o ciclo de ETL. Esta etapa garante que os dados estejam disponíveis para consultas e análises subsequentes. Com isso, os dados são carregados do ambiente local para o banco de dados no Postgres, como determinado pelo step2 da pipeline.

Cada etapa da DAG foi planejada e implementada para assegurar a eficiência e a precisão do pipeline de dados. As funções principais foram implementadas utilizando operadores Python e Bash, com dependências definidas para garantir a execução sequencial e correta de cada etapa, além do **agendamento (schedule) de 1 dia para carga diária**, como determinado pelo problema.

## **Resultado do case**

O resultado, que é uma tabela consolidada dos pedidos (`orders`) com os detalhes do pedido (`orders_details`) pode ser encontrado nesse **[LINK](link-csv-resultado)**

## Conclusão

O projeto foi desafiador. Embora eu já tenha utilizado Docker, fui apresentada a muitas ferramentas novas e precisei recorrer a documentações extensivas. Encontrei problemas especialmente em relação ao Meltano. No entanto, ao final do projeto, fiquei muito satisfeita, pois foi um aprendizado significativo para minha jornada de desenvolvimento como engenheira de dados. Aprender a usar o Airflow foi particularmente valioso, demonstrando como orquestrar e automatizar pipelines de dados complexos.

A integração das ferramentas Meltano e Airflow, juntamente com a utilização do Docker para isolar os ambientes dos bancos de dados PostgreSQL, mostrou-se essencial para a criação de um pipeline robusto. Consegui extrair dados diariamente, armazená-los no disco local e carregá-los em um banco de dados PostgreSQL de destino, demonstrando a eficiência e a escalabilidade da solução. Este projeto exemplificou o que o programa da LIGHTHOUSE oferece para desenvolver habilidades técnicas e práticas, reforçando minha capacidade de resolver problemas e aprender novas ferramentas rapidamente.
