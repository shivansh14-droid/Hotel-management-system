import os

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# ============================================
# LOAD ENVIRONMENT VARIABLES
# ============================================

load_dotenv()


# ============================================
# MYSQL DATABASE CONFIGURATION
# ============================================

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}


# ============================================
# CREATE DATABASE CONNECTION
# ============================================

def get_db_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )

        return connection

    except Error as e:

        print("Database connection error:", e)

        return None


# ============================================
# TEST DATABASE CONNECTION
# ============================================

if __name__ == "__main__":

    connection = get_db_connection()

    if connection:

        print("MySQL connected successfully!")

        connection.close()

    else:

        print("MySQL connection failed!")