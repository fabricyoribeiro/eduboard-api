from database.connect import ConnectDataBase
from modules.actor.actor import Actor
import json
import pandas as pd


class ActorDao:
  _TABLE_NAME = 'ACTOR'
  
  _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(username, name, age)'\
                  'values(%s, %s, %s) RETURNING username'
  _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
  _SELECT_BY_USERNAME = "SELECT * FROM {} WHERE USERNAME='{}'"
  _DELETE = 'DELETE FROM {} WHERE ID={}'
  _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}' WHERE USERNAME={}"

  
  def __init__(self):
    self.database = ConnectDataBase().get_instance()
  
  def save(self, actor):
    if actor.username is not None:
      cursor = self.database.cursor()
      cursor.execute(self._INSERT_INTO, (actor.username, actor.name, actor.age))
      self.database.commit()
      cursor.close()
      return actor
    else:
      raise Exception("Erro ao salvar")
    
  def get_by_username(self, username):
    cursor = self.database.cursor()
    cursor.execute(self._SELECT_BY_USERNAME.format(self._TABLE_NAME, username))
    coluns_name = [desc[0] for desc in cursor.description]
    actor = cursor.fetchone()
    if not actor:
      return None
    data = dict(zip(coluns_name, actor))
    actor = Actor(**data)
    print("Ator salvo", actor)
    cursor.close()
    return actor

  # def get_all(self):
  #     actors = []
  #     cursor = self.database.cursor()
  #     cursor.execute(self._SELECT_ALL)
  #     all_actors = cursor.fetchall()
  #     coluns_name = [desc[0] for desc in cursor.description]
  #     for actor_query in all_actors:
  #         data = dict(zip(coluns_name, actor_query))
  #         actor = Actor(**data)
  #         actors.append(actor)
  #     cursor.close()
  #     return actors
  

  def get_all(self):
      with open("base_ficticia.json", "r", encoding="utf-8") as file:
          data = json.load(file)

      # Extrai todos os dados de 'actor_username' diretamente
      actors_list = [item["actor_username"] for item in data if "actor_username" in item]

      # Cria DataFrame com os dados dos atores
      actors_df = pd.DataFrame(actors_list)

      # Remove duplicatas com base no campo 'username'
      unique_actors = actors_df.drop_duplicates(subset="username")

      # Converte para lista de dicionários e retorna
      return unique_actors.to_dict(orient="records")