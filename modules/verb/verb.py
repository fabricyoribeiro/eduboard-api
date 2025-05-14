class Verb:
  VALUES =  ['id', 'display_pt', 'display_en']

  def __init__(self, id, display_pt, display_en):
    self.id = id
    self.display_pt = display_pt
    self.display_en = display_en

  def __str__(self):
    return f'id: {self.id}, display_pt: {self.display_pt}, display_en: {self.display_en}'

  def get_data_dict(self):
    return {'id':self.id, 'display_pt':self.display_pt, 'display_en':self.display_en}
    