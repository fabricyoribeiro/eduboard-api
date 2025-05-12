class Actor:
  VALUES =  ['username', 'name', 'age']

  def __init__(self, username, name, age):
    self.username = username
    self.name = name
    self.age = age

  def __str__(self):
    return f'Username: {self.username}, name: {self.name}, age: {self.age}'

  def get_data_dict(self):
    return {'username':self.username, 'name':self.name, 'age':self.age}
  