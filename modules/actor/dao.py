from database.connect import ConnectDataBase
from modules.actor.actor import Actor
import json
import pandas as pd

class ActorDao:
    _TABLE_NAME = 'ACTOR'

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(username, name, age) VALUES (%s, %s, %s) RETURNING username'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_USERNAME = f"SELECT * FROM {_TABLE_NAME} WHERE USERNAME=%s"
    _DELETE = f'DELETE FROM {_TABLE_NAME} WHERE ID=%s'
    _UPDATE = f"UPDATE {_TABLE_NAME} SET name=%s, age=%s WHERE USERNAME=%s"

    def __init__(self):
        self.pool = ConnectDataBase().get_instance()

    def save(self, actor):
        if actor.username is not None:
            conn = self.pool.getconn()
            try:
                cursor = conn.cursor()
                cursor.execute(self._INSERT_INTO, (actor.username, actor.name, actor.age))
                conn.commit()
                cursor.close()
                return actor
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                self.pool.putconn(conn)
        else:
            raise Exception("Erro ao salvar: username é None")

    def get_by_username(self, username):
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(self._SELECT_BY_USERNAME, (username,))
            coluns_name = [desc[0] for desc in cursor.description]
            actor = cursor.fetchone()
            cursor.close()
            if not actor:
                return None
            data = dict(zip(coluns_name, actor))
            return Actor(**data)
        except Exception as e:
            raise e
        finally:
            self.pool.putconn(conn)

    def get_all(self):
        # Simulando retorno com JSON fictício
        with open("base_ficticia.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        actors_list = [item["actor_username"] for item in data if "actor_username" in item]
        actors_df = pd.DataFrame(actors_list)
        unique_actors = actors_df.drop_duplicates(subset="username")
        return unique_actors.to_dict(orient="records")
