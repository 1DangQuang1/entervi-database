import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Establishes a connection to the MySQL database.
    
    Returns:
        connection (object): MySQL connection object if successful, None otherwise.
    
    This function handles any errors during connection and returns None if the connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="Quangci@123",
            database="alibaba_db"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
