import psycopg2
from psycopg2 import sql

# Connection parameters
connection_params = {
    "host": "desperado-db.ctldmj6kaxoc.us-east-2.rds.amazonaws.com",
    "port": 5432,
    "user": "desperado",
    "password": "6156dbdesperado",
    "database": "postgres",
}

# Table name
table_name = "userinfo"
# Connect to the database and execute the DELETE statement
try:
    conn = psycopg2.connect(
    database="postgres",
    user="desperado",
    password="6156dbdesperado",
    host="desperado-db.ctldmj6kaxoc.us-east-2.rds.amazonaws.com",
    port='5432'
)
    # Create a cursor to execute SQL queries
    cursor = conn.cursor()

    # Example: Add composite unique constraint to the existing table
    add_unique_constraint_query = f"""
        ALTER TABLE {table_name}
        ADD CONSTRAINT unique_email_name UNIQUE (email, name);
    """
    cursor.execute(add_unique_constraint_query)

    # Commit the changes
    conn.commit()
except psycopg2.Error as e:
    print(f"Error: {e}")


