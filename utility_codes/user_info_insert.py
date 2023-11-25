import uuid
import json
import psycopg2

# Read data from JSON file
with open("fake_data.json", "r") as json_file:
    fake_data = json.load(json_file)

# Connect to PostgreSQL with debug statements
try:
    connection = psycopg2.connect(
    database="postgres",
    user="desperado",
    password="6156dbdesperado",
    host="desperado-db.ctldmj6kaxoc.us-east-2.rds.amazonaws.com",
    port='5432'
)
    print("Connected to the database.")
except psycopg2.Error as err:
    print(f"Error connecting to the database: {err}")
    exit()

try:
    cursor = connection.cursor()

    # Create table with debug statements
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS userinfo (
                uuid UUID PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                company VARCHAR(255),
                email VARCHAR(255) NOT NULL,
                picture_url VARCHAR(255) NULL
            );
        """)
        print("Table 'userinfo' created or already exists.")
    except psycopg2.Error as err:
        print(f"Error creating table: {err}")

    # Insert data with debug statements
    try:
        for user in fake_data:
            cursor.execute("""
                INSERT INTO userinfo (uuid, name, company, email, picture_url)
                VALUES (%s, %s, %s, %s, %s);
            """, (user["uuid"], user["name"], user["company"], user["email"], user["picture_url"]))
            print(f"Inserted data for {user['name']} ({user['email']}).")
        connection.commit()
    except psycopg2.Error as err:
        print(f"Error inserting data: {err}")

finally:
    # Close the connection
    if 'connection' in locals() and connection is not None:
        cursor.close()
        connection.close()
        print("Database connection closed.")
