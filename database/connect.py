import psycopg2
from psycopg2 import pool
import os

class ConnectDataBase:
    def __init__(self):
        try:
            self._connect = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=os.environ.get("DATABASE_URL")  # DSN deve ser uma string como: "dbname=test user=postgres password=secret host=localhost"
            )
        except psycopg2.Error as e:
            print("Erro ao conectar ao banco de dados:", e)
            self._connect = None

    def get_instance(self):
        return self._connect
