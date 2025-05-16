from database.connect import ConnectDataBase
from modules.result.result import Result

class ResultDao:
  _TABLE_NAME = 'RESULT'
  
  _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(success, response, response_time_seconds)'\
                  'values(%s, %s, %s) RETURNING id'
  _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
  _SELECT_BY_ID = "SELECT * FROM {} WHERE ID='{}'"
  _DELETE = 'DELETE FROM {} WHERE ID={}'
  _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}', WHERE ID={}"

  
  def __init__(self):
    self.database = ConnectDataBase().get_instance()
  
  def save(self, result):
    if result.id is None:
      cursor = self.database.cursor()
      cursor.execute(self._INSERT_INTO, (result.success, result.response, result.response_time_seconds))
      id = cursor.fetchone()[0]
      self.database.commit()
      cursor.close()
      result.id = id
      return result
    else:
      raise Exception("Erro ao salvar")
    
  def get_by_id(self, id):
    cursor = self.database.cursor()
    cursor.execute(self._SELECT_BY_ID.format(self._TABLE_NAME, id))
    coluns_name = [desc[0] for desc in cursor.description]
    result = cursor.fetchone()
    if not result:
      return None
    data = dict(zip(coluns_name, result))
    result = Result(**data)
    print("result salvo", result)
    cursor.close()
    return result
    
  def get_all(self):
    results = []
    cursor = self.database.cursor()
    cursor.execute(self._SELECT_ALL)
    all_results = cursor.fetchall()
    coluns_name = [desc[0] for desc in cursor.description]
    for result_query in all_results:
        data = dict(zip(coluns_name, result_query))
        result = Result(**data)
        results.append(result)
    cursor.close()
    return results