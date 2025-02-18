import mysql.connector
from config import Config
print("Starting the testing")
# Connection configuration

try:
    # Establish connection
    print("Trying to connect to database")
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
        )

    if connection.is_connected():
        print("connection established")
        print("Connected to MySQL database!")
        cursor = connection.cursor()
        query = "SELECT * FROM users"
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        print("MySQL Server version:", connection.get_server_info())

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed.")
