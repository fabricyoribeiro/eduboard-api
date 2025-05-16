from flask import Blueprint, make_response, request, jsonify

from modules.result.dao import ResultDao
from modules.result.result import Result

app_result = Blueprint('result_blueprint', __name__)
app_name = 'result'
dao_result = ResultDao()

@app_result.route(f"/{app_name}/add", methods=['POST'])
def add_result():
  data = request.get_json()
  errors = []
  for key in Result.VALUES:
    if key not in data.keys():
      errors.append({'field': key ,'message': 'Este campo é obrigatório'})
  if errors:
    return make_response({"errors": errors})
  
  result = Result(**data)
  dao_result.save(result)
  return make_response({"id": result.id})
          

@app_result.route(f"/{app_name}/<string:id>", methods=['GET'])
def get_result(id):
  
  result = dao_result.get_by_id(id)
  if not result:  
    return make_response({'error': 'O id informado não existe'})
    
  data = result.get_data_dict()
  print('result', data)
  return make_response({'result': data})

@app_result.route(f"/{app_name}/all", methods=['GET'])
def get_results():
  results = dao_result.get_all()
  data = [result.get_data_dict() for result in results]
  return make_response(jsonify(data))