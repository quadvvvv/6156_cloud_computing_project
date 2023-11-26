import uuid
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database configuration (replace these values with your RDS details)
db_host =  "desperado-db.ctldmj6kaxoc.us-east-2.rds.amazonaws.com",
db_port = 5432,
db_user = "desperado"
db_password = "6156dbdesperado"
db_name = "postgres"

@app.route('/', methods=['GET'])
# for testing
def main():
    return "Hello World",200


# API to create a new user
@app.route('/userinfo/', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    company = data.get('company')
    email = data.get('email')
    is_recruiter = data.get('is_recruiter')
    picture_url = data.get('picture_url')

    if not name or not company or not email or is_recruiter is None or not picture_url:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Generate a new UUID
        user_uuid = str(uuid.uuid4())

        # Insert new user into the "userinfo" table
        cursor.execute(
            """
            INSERT INTO userinfo (uuid, name, company, email, is_recruiter, picture_url)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (user_uuid, name, company, email, is_recruiter, picture_url)
        )

        # Commit the transaction
        conn.commit()

        return jsonify({"message": "User created successfully"}), 201

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
# API to get information about a specific user based on the email
@app.route('/userinfo/<email>', methods=['GET'])
def get_user(email):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Retrieve user information from the "userinfo" table
        cursor.execute("SELECT * FROM userinfo WHERE email = %s;", (email,))
        user = cursor.fetchone()

        if user:
            user_info = {
                "uuid": user[0],
                "name": user[1],
                "company": user[2],
                "email": user[3],
                "is_recruiter": user[4],
                "picture_url": user[5]
            }
            return jsonify(user_info)
        else:
            return jsonify({"error": "User not found"}), 404

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# API to get all recruiters
@app.route('/userinfo/recruiters', methods=['GET'])
def get_recruiters():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Retrieve all recruiters from the "userinfo" table
        cursor.execute("SELECT * FROM userinfo WHERE is_recruiter = true;")
        recruiters = cursor.fetchall()

        recruiter_list = [{
            "uuid": user[0],
            "name": user[1],
            "company": user[2],
            "email": user[3],
            "is_recruiter": user[4],
            "picture_url": user[5]
        } for user in recruiters]

        return jsonify(recruiter_list)

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# API to get all job seekers
@app.route('/userinfo/jobseekers', methods=['GET'])
def get_jobseekers():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Retrieve all job seekers from the "userinfo" table
        cursor.execute("SELECT * FROM userinfo WHERE is_recruiter = false;")
        jobseekers = cursor.fetchall()

        jobseeker_list = [{
            "uuid": user[0],
            "name": user[1],
            "company": user[2],
            "email": user[3],
            "is_recruiter": user[4],
            "picture_url": user[5]
        } for user in jobseekers]

        return jsonify(jobseeker_list)

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# API to update a user's company
@app.route('/userinfo/<email>', methods=['POST'])
def update_user_company(email):
    data = request.json
    new_company = data.get('new_company')

    if not new_company:
        return jsonify({"error": "Missing 'new_company' field in the request body"}), 400

    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Update the user's company in the "userinfo" table
        cursor.execute("UPDATE userinfo SET company = %s WHERE email = %s;", (new_company, email))

        # Commit the transaction
        conn.commit()

        return jsonify({"message": f"User's company updated to {new_company} successfully"}), 200

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# API to delete a specific user
@app.route('/userinfo/<email>', methods=['DELETE'])
def delete_user(email):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Delete the user from the "userinfo" table
        cursor.execute("DELETE FROM userinfo WHERE email = %s;", (email,))

        # Commit the transaction
        conn.commit()

        return jsonify({"message": "User deleted successfully"}), 200

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
