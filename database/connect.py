import psycopg2
import os

class ConnectDataBase:
    def __init__(self):
        try:
            self._connect = psycopg2.connect(os.environ.get("DATABASE_URL"))
        except psycopg2.Error as e:
            print("Erro ao conectar ao banco de dados:", e)
            self._connect = None

    def get_instance(self):
        return self._connect
