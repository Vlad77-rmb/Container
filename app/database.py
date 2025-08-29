from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

# подключение к БД
@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "atk"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "password"),
            autocommit=False
        )
        yield connection
    except Error as e:
        raise Exception(f"Database connection failed: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()