from database.connect import ConnectDataBase
from modules.subject.subject import Subject

class SubjectDao:
  _TABLE_NAME = 'SUBJECT'
  
  _INSERT_INTO = f'INSERT INTO {_TABLE_NAME}(name_pt, name_en, description_pt, description_en)'\
                  'values(%s, %s, %s, %s) RETURNING id'
  _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
  _SELECT_BY_NAME_PT = "SELECT * FROM {} WHERE NAME_PT='{}'"
  _DELETE = 'DELETE FROM {} WHERE ID={}'
  _UPDATE = "UPDATE {} SET {}='{}', {}='{}', {}='{}', {}='{}', {}='{}' WHERE ID={}"

  
  def __init__(self):
    self.database = ConnectDataBase().get_instance()
  
  def save(self, subject):
    if subject.id is None:
      cursor = self.database.cursor()
      cursor.execute(self._INSERT_INTO, (subject.name_pt, subject.name_en, subject.description_pt, subject.description_en))
      id = cursor.fetchone()[0]
      self.database.commit()
      cursor.close()
      subject.id = id
      return subject
    else:
      raise Exception("Erro ao salvar")
    
  def get_by_name_pt(self, name_pt):
    cursor = self.database.cursor()
    cursor.execute(self._SELECT_BY_NAME_PT.format(self._TABLE_NAME, name_pt))
    coluns_name = [desc[0] for desc in cursor.description]
    subject = cursor.fetchone()
    if not subject:
      return None
    data = dict(zip(coluns_name, subject))
    subject = Subject(**data)
    print("subject salvo", subject)
    cursor.close()
    return subject
    
  def get_all(self):
    subjects = []
    cursor = self.database.cursor()
    cursor.execute(self._SELECT_ALL)
    all_subjects = cursor.fetchall()
    coluns_name = [desc[0] for desc in cursor.description]
    for subject_query in all_subjects:
        data = dict(zip(coluns_name, subject_query))
        subject = Subject(**data)
        subjects.append(subject)
    cursor.close()
    return subjects