import mysql.connector 
from mysql.connector import Error
def create_connection():
    try :
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'Quangci@123',
            database = 'alibaba_db'
        )
        if connection.is_connected ():
            return connection
    except Error as e:
        print(f'Cannot to connect to database, {e}')  
