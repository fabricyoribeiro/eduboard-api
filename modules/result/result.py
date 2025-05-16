class Result:
  VALUES =  ['success', 'response', 'response_time_seconds']

  def __init__(self, success, response, response_time_seconds, id=None):
    self.id = id
    self.success = success
    self.response = response
    self.response_time_seconds = response_time_seconds

  def __str__(self):
    return f"id:{self.id}, success:{self.success}, response:{self.response}, response_time_seconds:{self.response_time_seconds}"

  def get_data_dict(self):
    return {
        'id': self.id,
        'success': self.success,
        'response': self.response,
        'response_time_seconds': self.response_time_seconds
    }

    
    
