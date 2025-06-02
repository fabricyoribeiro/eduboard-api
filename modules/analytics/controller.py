from flask import Blueprint, make_response
from modules.analytics.dao import AnalyticsDao

app_analytics = Blueprint('analytics_blueprint', __name__)
app_name = 'analytics'

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
