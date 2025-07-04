from flask import Blueprint, make_response, jsonify
from modules.analytics.dao import AnalyticsDao
from modules.event.dao import EventDao
import json

app_analytics = Blueprint('analytics_blueprint', __name__)
app_name = 'analytics'

dao_event = EventDao()

@app_analytics.route(f'/{app_name}/update-data', methods=["GET"])
def update_data():
  events = dao_event.get_all()
  data = [event.get_data_dict() for event in events]
  
  with open('base_ficticia.json', 'w', encoding='utf-8') as f:
      json.dump(data, f, indent=4, ensure_ascii=False, default=str)
  
  return jsonify({"message": "Dados atualizados com sucesso!"})


@app_analytics.route(f'/{app_name}/performance-classification', methods=["GET"])
def get_performance_classification():
  analytics = AnalyticsDao()
  # classification = analytics.get_performance_classification()
  classification = analytics.get_overall_individual_variables()
  return make_response(classification) 

@app_analytics.route(f'/{app_name}/indicators', methods=["GET"])
def get_indicators():
  analytics = AnalyticsDao()
  indicators = analytics.get_indicators()
  return make_response(indicators)

@app_analytics.route(f'/{app_name}/overall/hit-miss-by-object-level', methods=["GET"])
def get_overall_hit_and_miss_by_object_level():
  analytics = AnalyticsDao()
  hit_and_miss_object_level = analytics.get_overall_hit_and_miss_by_object_level()
  return make_response(hit_and_miss_object_level)

@app_analytics.route(f'/{app_name}/overall/hit-miss-rate', methods=["GET"])
def get_overall_hit_and_miss_rate():
  analytics = AnalyticsDao()
  hit_and_miss_rate = analytics.get_overall_hit_and_miss_rate()
  return make_response(hit_and_miss_rate)

@app_analytics.route(f'/{app_name}/overall/hit-miss-by-subject', methods=["GET"])
def get_overall_hit_and_miss_by_subject():
  analytics = AnalyticsDao()
  hit_and_miss_by_subject= analytics.get_overall_hit_and_miss_by_subject()
  return make_response(hit_and_miss_by_subject)

@app_analytics.route(f'/{app_name}/overall/ranking', methods=["GET"])
def get_ranking():
  analytics = AnalyticsDao()
  ranking = analytics.get_ranking()
  return make_response(ranking)

## ROTA INDIVIDUAL
@app_analytics.route(f'/{app_name}/individual/average_time_by_object', methods=["GET"])
def get_average_time_by_object():
  analytics = AnalyticsDao()
  average_time_by_object = analytics.get_average_time_by_object()
  return make_response(average_time_by_object)

