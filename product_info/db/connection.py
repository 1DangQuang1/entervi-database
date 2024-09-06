import mysql.connector
from config.db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Initialize mysql connection
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
