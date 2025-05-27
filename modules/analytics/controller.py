from flask import Blueprint, make_response
from modules.analytics.dao import AnalyticsDao

app_analytics = Blueprint('analytics_blueprint', __name__)
app_name = 'analytics'

@app_analytics.route(f'/{app_name}/indicators', methods=["GET"])
def get_indicators():

  analytics = AnalyticsDao()
  indicators = analytics.get_indicators()
  
  return make_response(indicators)

@app_analytics.route(f'/{app_name}/overall/hit-miss-rate', methods=["GET"])
def get_overall_hit_and_miss_rate():
  ##continuar
  analytics = AnalyticsDao()
  hit_and_miss_rate = analytics.get_overall_hit_and_miss_rate()

  return make_response(hit_and_miss_rate)

@app_analytics.route(f'/{app_name}/overall/ranking', methods=["GET"])
def get_ranking():
  ##continuar
  analytics = AnalyticsDao()
  ranking = analytics.get_ranking()

  return make_response(ranking)
