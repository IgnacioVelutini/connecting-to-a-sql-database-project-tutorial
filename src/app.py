import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch database credentials from environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Step 1: Create the connection string
connection_string = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

# Step 2: Create an engine and connect to the database
engine = create_engine(connection_string).execution_options(autocommit=True)
connection = engine.connect()

# Step 3: Create a table (if not exists)
create_table_query = """
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(100),
    salary NUMERIC
);
"""
connection.execute(create_table_query)

# Step 4: Insert some data into the table
insert_data_query = """
INSERT INTO employees (name, position, salary)
VALUES 
    ('Dustin Pedroia', 'Data Scientist', 90000),
    ('David Ortiz', 'Data Analyst', 80000),
    ('Manny Ramirez', 'Software Engineer', 95000)
ON CONFLICT DO NOTHING;
"""
connection.execute(insert_data_query)

# Step 5: Use pandas to fetch and display data from the table
df = pd.read_sql('SELECT * FROM employees', connection)
print(df)

# Close the connection after operations are done
connection.close()
