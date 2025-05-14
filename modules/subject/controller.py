from flask import Blueprint, make_response, request, jsonify

from modules.subject.dao import SubjectDao
from modules.subject.subject import Subject

app_subject = Blueprint('subject_blueprint', __name__)
app_name = 'subject'
dao_subject = SubjectDao()

@app_subject.route(f"/{app_name}/add", methods=['POST'])
def add_subject():
  data = request.get_json()
  errors = []
  for key in Subject.VALUES:
    if key not in data.keys():
      errors.append({'field': key ,'message': 'Este campo é obrigatório'})
  if errors:
    return make_response({"errors": errors})
  
  subject = dao_subject.get_by_name_pt(data.get('name_pt'))
  if subject:
    return make_response({'error': 'subject já existe'})
  subject = Subject(**data)
  dao_subject.save(subject)
  return make_response({"id": subject.id})
          

@app_subject.route(f"/{app_name}/<string:id>", methods=['GET'])
def get_subject(id):
  
  subject = dao_subject.get_by_id(id)
  if not subject:  
    return make_response({'error': 'O id informado não existe'})
    
  data = subject.get_data_dict()
  print('subject', data)
  return make_response({'subject': data})

@app_subject.route(f"/{app_name}/all", methods=['GET'])
def get_subjects():
  subjects = dao_subject.get_all()
  data = [object.get_data_dict() for object in subjects]
  return make_response(jsonify(data))