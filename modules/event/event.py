from modules.actor.dao import ActorDao
from modules.object.dao import ObjectDao
from modules.result.dao import ResultDao
from modules.subject.dao import SubjectDao
from modules.verb.dao import VerbDao

class Event:
  VALUES = ['actor_username', 'verb_id', 'object_id', 'subject_id', 'result_id']

  def __init__(self,actor_username, verb_id, object_id, subject_id, result_id, date_time=None, id=None):
    self.id = id
    self.actor_username = actor_username
    self.verb_id = verb_id
    self.object_id = object_id
    self.subject_id = subject_id
    self.result_id = result_id
    self.date_time = date_time
  
  def __str__(self):
    return f'Id: {self.id}, verb_id: {self.verb_id}, veiculo id: {self.object_id}, valor gasto: {self.result_id}, km atual: {self.km_atual}'
  
  def get_data_dict(self):
    dao_actor =  ActorDao()
    dao_verb = VerbDao()
    dao_object = ObjectDao()
    dao_subject = SubjectDao()
    dao_result = ResultDao()
    
    actor = dao_actor.get_by_username(self.actor_username)
    verb = dao_verb.get_by_id(self.verb_id)
    object = dao_object.get_by_id(self.object_id)
    subject = dao_subject.get_by_id(self.subject_id)
    result = dao_result.get_by_id(self.result_id)

    return {
      'id': self.id,
      'actor_username': actor.get_data_dict(),
      'verb': verb.get_data_dict(), 
      'object': object.get_data_dict() , 
      'subject': subject.get_data_dict(),
      'result': result.get_data_dict(),
      'date_time': self.date_time
    }