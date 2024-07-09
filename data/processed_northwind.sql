-- Criar o banco de dados
CREATE DATABASE processed_northwind;

-- Conectar ao banco de dados
\c processed_northwind;

-- Criar a tabela de categorias
CREATE TABLE IF NOT EXISTS categories (
    category_id VARCHAR(255) NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    picture BYTEA,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar a tabela de detalhes de pedidos
CREATE TABLE IF NOT EXISTS order_details (
    order_id VARCHAR(255) NOT NULL,
    product_id VARCHAR(255),
    unit_price VARCHAR(255),  -- Transformado para string conforme a transformação no meltano
    quantity VARCHAR(255),
    discount VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar a tabela de produtos
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    supplier_id VARCHAR(255),
    category_id VARCHAR(255),
    quantity_per_unit VARCHAR(255),
    unit_price VARCHAR(255),  -- Transformado para string conforme a transformação no meltano
    units_in_stock VARCHAR(255),
    units_on_order VARCHAR(255),
    reorder_level VARCHAR(255),
    discontinued VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar a tabela de fornecedores
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    contact_title VARCHAR(255),
    address VARCHAR(255),
    city VARCHAR(255),
    region VARCHAR(255),
    postal_code VARCHAR(255),
    country VARCHAR(255),
    phone VARCHAR(255),
    fax VARCHAR(255),
    homepage VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar a tabela de clientes
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    contact_title VARCHAR(255),
    address VARCHAR(255),
    city VARCHAR(255),
    region VARCHAR(255),
    postal_code VARCHAR(255),
    country VARCHAR(255),
    phone VARCHAR(255),
    fax VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar a tabela de demonstrações do cliente
CREATE TABLE IF NOT EXISTS customer_customer_demo (
    customer_id bpchar NOT NULL,
    customer_type_id bpchar NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (customer_id, customer_type_id)
);

-- Criar a tabela de demografia do cliente
CREATE TABLE IF NOT EXISTS customer_demographics (
    customer_type_id bpchar NOT NULL,
    customer_desc VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar a tabela de pedidos
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(255) NOT NULL,
    customer_id VARCHAR(255),
    employee_id VARCHAR(255),
    order_date VARCHAR(255),
    required_date VARCHAR(255),
    shipped_date VARCHAR(255),
    ship_via VARCHAR(255),
    freight VARCHAR(255),  -- Transformado para string conforme a transformação no meltano
    ship_name VARCHAR(255),
    ship_address VARCHAR(255),
    ship_city VARCHAR(255),
    ship_region VARCHAR(255),
    ship_postal_code VARCHAR(255),
    ship_country VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar a tabela de empregados
CREATE TABLE IF NOT EXISTS employees (
    employee_id VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    title_of_courtesy VARCHAR(255),
    birth_date VARCHAR(255),
    hire_date VARCHAR(255),
    address TEXT,
    city VARCHAR(255),
    region VARCHAR(255),
    postal_code VARCHAR(255),
    country VARCHAR(255),
    home_phone VARCHAR(255),
    extension VARCHAR(255),
    photo BYTEA,
    notes TEXT,
    reports_to VARCHAR(255),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar a tabela de territórios de empregados
CREATE TABLE IF NOT EXISTS employee_territories (
    employee_id VARCHAR(255) NOT NULL,
    territory_id VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (employee_id, territory_id)
);

-- Criar a tabela de regiões
CREATE TABLE IF NOT EXISTS region (
    region_id VARCHAR(255) NOT NULL,
    region_description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar a tabela de transportadoras
CREATE TABLE IF NOT EXISTS shippers (
    shipper_id VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    phone VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar a tabela de estados dos EUA
CREATE TABLE IF NOT EXISTS us_states (
    state_id VARCHAR(255) NOT NULL,
    state_name VARCHAR(255),
    state_abbr VARCHAR(2),
    state_region VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Criar a tabela de territórios
CREATE TABLE IF NOT EXISTS territories (
    state_id VARCHAR(255),
    territory_description VARCHAR(255) NOT NULL,
    region_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

