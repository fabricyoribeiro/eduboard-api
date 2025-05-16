from flask import Blueprint, make_response, request, jsonify

from modules.verb.dao import VerbDao
from modules.verb.verb import Verb

app_verb = Blueprint('verb_blueprint', __name__)
app_name = 'verb'
dao_verb = VerbDao()

@app_verb.route(f"/{app_name}/add", methods=['POST'])
def add_verb():
  data = request.get_json()
  errors = []
  for key in Verb.VALUES:
    if key not in data.keys():
      errors.append({'field': key ,'message': 'Este campo é obrigatório'})
  
  if errors:
    return make_response({"errors": errors})
  verb = dao_verb.get_by_id(data.get(id))
  if verb:
    return make_response({'error': 'Verb já existe'})
  verb = Verb(**data)
  dao_verb.save(verb)
  return make_response({"id": verb.id})
          

@app_verb.route(f"/{app_name}/<string:id>", methods=['GET'])
def get_verb(id):
  
  verb = dao_verb.get_by_id(id)
  if not verb:  
    return make_response({'error': 'O id informado não existe'})
    
  data = verb.get_data_dict()
  print('verb', data)
  return make_response({'verb': data})

@app_verb.route(f"/{app_name}/all", methods=['GET'])
def get_verbs():
  verbs = dao_verb.get_all()
  data = [verb.get_data_dict() for verb in verbs]
  return make_response(jsonify(data))