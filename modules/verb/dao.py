from database.connect import ConnectDataBase
from modules.verb.verb import Verb

class VerbDao:
  _TABLE_NAME = 'VERB'
  
  _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(id, display_pt, display_en)'\
                  'values(%s, %s, %s) RETURNING id'
  _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
  _SELECT_BY_ID = "SELECT * FROM {} WHERE ID='{}'"
  _DELETE = 'DELETE FROM {} WHERE ID={}'
  _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}' WHERE ID={}"

  
  def __init__(self):
    self.database = ConnectDataBase().get_instance()
  
  def save(self, verb):
    if verb.id is not None:
      cursor = self.database.cursor()
      cursor.execute(self._INSERT_INTO, (verb.id, verb.display_pt, verb.display_en))
      self.database.commit()
      cursor.close()
      return verb
    else:
      raise Exception("Erro ao salvar")
    
  def get_by_id(self, id):
    cursor = self.database.cursor()
    cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
    coluns_name = [desc[0] for desc in cursor.description]
    verb = cursor.fetchone()
    if not verb:
      return None
    data = dict(zip(coluns_name, verb))
    verb = Verb(**data)
    print("Verb salvo", verb)
    cursor.close()
    return verb
    
  def get_all(self):
    verbs = []
    cursor = self.database.cursor()
    cursor.execute(self._SELECT_ALL)
    all_verbs = cursor.fetchall()
    coluns_name = [desc[0] for desc in cursor.description]
    for verb_query in all_verbs:
        data = dict(zip(coluns_name, verb_query))
        verb = Verb(**data)
        verbs.append(verb)
    cursor.close()
    return verbs