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
    with psycopg2.connect(**connection_params) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        # Commit the changes
        connection.commit()
    print(f"All entries deleted from {table_name}.")
except psycopg2.Error as e:
    print(f"Error: {e}")