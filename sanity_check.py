import psycopg2

try:
    connection = psycopg2.connect(
    database="postgres",
    user="desperado",
    password="6156dbdesperado",
    host="desperado-db.ctldmj6kaxoc.us-east-2.rds.amazonaws.com",
    port='5432'
)
    print("Connected to the database.")

    cursor = connection.cursor()

    # Example: Selecting items from a table
    cursor.execute(f"SELECT * FROM userinfo;")
    rows = cursor.fetchall()

    # Process the results
    if rows:
        print("Data in the table:")
        for row in rows:
            print(row)
    else:
        print("No data found in the table.")

except psycopg2.Error as e:
    print("Error connecting to the database:", e)

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()