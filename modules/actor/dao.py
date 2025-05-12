from database.connect import ConnectDataBase
from modules.actor.actor import Actor

class ActorDao:
  _TABLE_NAME = 'ACTOR'
  
  _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(username, name, age)'\
                  'values(%s, %s, %s) RETURNING username'
  _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
  _SELECT_BY_USERNAME = "SELECT * FROM {} WHERE USERNAME='{}'"
  _DELETE = 'DELETE FROM {} WHERE ID={}'
  _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}', {}='{}', {}='{}', {}='{}' WHERE USERNAME={}"

  
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