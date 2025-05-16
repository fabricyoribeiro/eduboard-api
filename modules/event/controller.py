from datetime import datetime
from ntpath import join
from flask import Flask, make_response, jsonify, request, Blueprint
from modules.event.event import Event

from modules.event.dao import EventDao
from modules.actor.dao import ActorDao
from modules.verb.dao import VerbDao
from modules.object.dao import ObjectDao
from modules.subject.dao import SubjectDao
from modules.result.dao import ResultDao


app_event = Blueprint('event_blueprint', __name__)
app_name = 'event'
dao_event = EventDao()

dao_actor = ActorDao()
dao_verb = VerbDao()
dao_object = ObjectDao()
dao_subject = SubjectDao()
dao_result = ResultDao()


@app_event.route(f'/{app_name}/all', methods=['GET'])
def get_events():
    events = dao_event.get_all()
    data = [event.get_data_dict() for event in events]
    return make_response(jsonify(data))


@app_event.route(f'/{app_name}/add/', methods=['POST'])
def add_event():
    data = request.get_json()
    errors = []
    
    if data.get('actor_username') != None:
      if isinstance(data.get("actor_username"), str) == False:
        errors.append({'field': 'actor_username', 'message': 'Este campo so aceita string'})

    for key in Event.VALUES:
        if key not in data.keys() or data[key] =='':
            errors.append({'field': key, 'mensage': "Este campo é obrigátorio."})
    
    for key in ['verb_id', 'object_id']:
        if data.get(key) != None and isinstance(data.get(key), int):
            print(data[key])

            errors.append({'field': key, 'mensage': 'Este campo só aceita string'})
            break
          
    for key in ['subject_id', 'result_id']: 
        if data.get(key) != None and isinstance(data.get(key), str):
            print(data[key])

            errors.append({'field': key, 'mensage': 'Este campo só aceita números inteiros'})
            break
          

    if errors:
        return make_response({'errors': errors}, 400)
   
    actor = dao_actor.get_by_username(data.get('actor_username'))
    
    verb = dao_verb.get_by_id(data.get('verb_id'))
    
    object = dao_object.get_by_id(data.get('object_id'))
    
    subject = dao_subject.get_by_id(data.get('subject_id'))
    
    result = dao_result.get_by_id(data.get('result_id'))


    if not  actor:
        return make_response({'erro': "id do actor não existe."}, 400)

    if not  verb:
        return make_response({'erro': "id da verb não existe."}, 400)

    if not  object:
        return make_response({'erro': "id de object não existe."}, 400)

    if not  subject:
        return make_response({'erro': "id da subject não existe."}, 400)

    if not  result:
        return make_response({'erro': "id de result não existe."}, 400)

    event = Event(**data)
    event = dao_event.save(event)
    return make_response({
        'id': event.id
    })

@app_event.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_event_by_id(id):
    event = dao_event.get_by_id(id)
    if not event:
        return 'O id informado não existe'
    data = event.get_data_dict()
    return make_response(jsonify(data))


@app_event.route(f'/{app_name}/delete/<int:id>/', methods=['DELETE'])
def delete_event(id):

    event = dao_event.get_by_id(id)

    if not event:
        return make_response({'erro': 'O id informado não existe'})
    dao_event.delete_event(id)
    return make_response({
        'Detetado com sucesso': True
    })