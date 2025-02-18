import mysql.connector
from config import Config

connection = None
def get_db_connection():
    global connection
    if connection is None or not connection.is_connected():
        try:
            connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE
            )
            print("Database connection established.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            connection = None
    return connection
