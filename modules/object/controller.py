from flask import Blueprint, make_response, request, jsonify

from modules.object.dao import ObjectDao
from modules.object.object import Object

app_object = Blueprint('object_blueprint', __name__)
app_name = 'object'
dao_object = ObjectDao()

@app_object.route(f"/{app_name}/add", methods=['POST'])
def add_object():
  data = request.get_json()
  errors = []
  for key in Object.VALUES:
    if key not in data.keys():
      errors.append({'field': key ,'message': 'Este campo é obrigatório'})
  if errors:
    return make_response({"errors": errors})
  object = dao_object.get_by_id(data.get(id))
  if object:
    return make_response({'error': 'object já existe'})
  object = Object(**data)
  dao_object.save(object)
  return make_response({"id": object.id})
          

@app_object.route(f"/{app_name}/<string:id>", methods=['GET'])
def get_object(id):
  
  object = dao_object.get_by_id(id)
  if not object:  
    return make_response({'error': 'O id informado não existe'})
    
  data = object.get_data_dict()
  print('object', data)
  return make_response({'object': data})

@app_object.route(f"/{app_name}/all", methods=['GET'])
def get_objects():
  objects = dao_object.get_all()
  data = [object.get_data_dict() for object in objects]
  return make_response(jsonify(data))