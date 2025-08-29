import mysql.connector
from mysql.connector import Error
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()


def init_database():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS atk")
        cursor.execute("USE atk")

        # Создание таблицы users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Создание таблицы containers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS containers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                container_number CHAR(11) UNIQUE NOT NULL,
                cost DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_container_number (container_number),
                INDEX idx_cost (cost)
            )
        """)

        # Добавление тестовых пользователей
        users = [
            ("user1", "password1"),
            ("user2", "password2"),
            ("user3", "password3")
        ]

        for username, password in users:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                "INSERT IGNORE INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )

        # Добавление тестовых контейнеров
        containers = [
            ("ABCU1234567", 1000.50),
            ("DEFU7654321", 2000.75),
            ("GHIU9876543", 1500.25),
            ("JKLU4567890", 3000.00),
            ("MNOPU1239876", 2500.50),
            ("QRSTU6543210", 1800.75),
            ("VWXU7890123", 2200.25),
            ("YZAU3210987", 2700.00),
            ("BCDU8765432", 1900.50),
            ("EFGU2345678", 2100.75)
        ]

        for container_number, cost in containers:
            cursor.execute(
                "INSERT IGNORE INTO containers (container_number, cost) VALUES (%s, %s)",
                (container_number, cost)
            )

        connection.commit()
        print("Database initialized successfully")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    init_database()