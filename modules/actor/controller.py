from flask import Blueprint, request, make_response, jsonify

from modules.actor.dao import ActorDao
from modules.actor.actor import Actor

app_actor = Blueprint('actor_blueprint', __name__)
app_name = 'actor'
dao_actor = ActorDao()

@app_actor.route(f"/{app_name}/add", methods=['POST'])
def add_actor():
  data = request.get_json()
  
  errors = []
  for key in Actor.VALUES:
    if key not in data.keys():
      errors.append({'field': key, 'message': "Este campo é obrigatório"})
      
  if errors:
    return make_response({'errors': errors}, 400)
    
  actor = dao_actor.get_by_username(data.get('username'))
  if actor:
    return make_response({'error': 'Actor já existe'}, 400)
  
  actor = Actor(**data)
  actor = dao_actor.save(actor) 
  return make_response({
    'username': actor.username
  })
  

@app_actor.route(f"/{app_name}/login/<string:username>", methods=['GET'])
def login(username):
  actor = dao_actor.get_by_username(username)
  if not actor:  
    return make_response({'error': 'O username informado não existe'})
  data = actor.get_data_dict()
  print('actor', data)
  return make_response({'actor': data})


@app_actor.route(f"/{app_name}/all", methods=['GET'])
def get_actors():
  actors = dao_actor.get_all()
  # data = [actor.get_data_dict() for actor in actors]
  return make_response(actors)