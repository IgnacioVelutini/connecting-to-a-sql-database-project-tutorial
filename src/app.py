import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(connection_string).execution_options(autocommit=True)
engine.connect()

engine.execute("""
CREATE TABLE IF NOT EXISTS categories(
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS products(
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT,
    FOREIGN KEY(category_id) REFERENCES categories(category_id)
);

CREATE TABLE IF NOT EXISTS customers(
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS orders(
    order_id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id INT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items(
    order_item_id SERIAL PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES products(product_id) ON DELETE CASCADE
);
""")

engine.execute("""
INSERT INTO categories (name) VALUES ('Electronics'), ('Books'), ('Clothing'), ('Toys');
INSERT INTO products (name, price, category_id) VALUES 
    ('Laptop', 1200.00, 1),
    ('Smartphone', 800.00, 1),
    ('Fiction Book', 15.00, 2),
    ('T-Shirt', 20.00, 3),
    ('Action Figure', 25.00, 4);

INSERT INTO customers (first_name, last_name, email) VALUES 
    ('John', 'Doe', 'johndoe@example.com'),
    ('Jane', 'Smith', 'janesmith@example.com');

INSERT INTO orders (order_date, customer_id) VALUES 
    ('2024-10-01', 1),
    ('2024-10-02', 2);

INSERT INTO order_items (order_id, product_id, quantity) VALUES 
    (1, 1, 1),
    (1, 3, 2),
    (2, 2, 1),
    (2, 4, 1);
""")

result_dataFrame = pd.read_sql("SELECT * FROM customers;", engine)
print(result_dataFrame)
