import os
import psycopg2
import psycopg2.extras

from dotenv import load_dotenv
from interface import Interface

load_dotenv()

connection = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT"),
)

if __name__ == "__main__":
    GUI = Interface(connection)
    GUI.start()
    GUI.clean()
