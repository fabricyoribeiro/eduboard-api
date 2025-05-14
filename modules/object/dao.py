from database.connect import ConnectDataBase
from modules.object.object import Object

class ObjectDao:
  _TABLE_NAME = 'OBJECT'
  
  _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(id, name_pt, name_en, description_pt, description_en)'\
                  'values(%s, %s, %s, %s, %s) RETURNING id'
  _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
  _SELECT_BY_ID = "SELECT * FROM {} WHERE ID='{}'"
  _DELETE = 'DELETE FROM {} WHERE ID={}'
  _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}', {}='{}', {}='{}' WHERE ID={}"

  
  def __init__(self):
    self.database = ConnectDataBase().get_instance()
  
  def save(self, object):
    if object.id is not None:
      cursor = self.database.cursor()
      cursor.execute(self._INSERT_INTO, (object.id, object.name_pt, object.name_en, object.description_pt, object.description_en))
      self.database.commit()
      cursor.close()
      return object
    else:
      raise Exception("Erro ao salvar")
    
  def get_by_id(self, id):
    cursor = self.database.cursor()
    cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
    coluns_name = [desc[0] for desc in cursor.description]
    object = cursor.fetchone()
    if not object:
      return None
    data = dict(zip(coluns_name, object))
    object = Object(**data)
    print("object salvo", object)
    cursor.close()
    return object
    
  def get_all(self):
    objects = []
    cursor = self.database.cursor()
    cursor.execute(self._SELECT_ALL)
    all_objects = cursor.fetchall()
    coluns_name = [desc[0] for desc in cursor.description]
    for object_query in all_objects:
        data = dict(zip(coluns_name, object_query))
        object = Object(**data)
        objects.append(object)
    cursor.close()
    return objects