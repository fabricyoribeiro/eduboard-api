class Object:
  VALUES =  ['id', 'name_pt', 'name_en', 'description_pt', 'description_en']

  def __init__(self, id, name_pt, name_en, description_pt, description_en):
    self.id = id
    self.name_pt = name_pt
    self.name_en = name_en
    self.description_pt = description_pt
    self.description_en = description_en

  def __str__(self):
    return f"id:{self.id}, name_pt:{self.name_pt}, name_en:{self.name_en}, description_pt:{self.description_pt}, description_en:{self.description_en}"

  def get_data_dict(self):
    return {
        'id': self.id,
        'name_pt': self.name_pt,
        'name_en': self.name_en,
        'description_pt': self.description_pt,
        'description_en': self.description_en
    }

    
    
