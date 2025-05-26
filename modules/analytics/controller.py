from flask import Blueprint, make_response
from modules.analytics.dao import AnalyticsDao

app_analytics = Blueprint('analytics_blueprint', __name__)
app_name = 'analytics'

@app_analytics.route(f'/{app_name}/indicators', methods=["GET"])
def get_indicators():

  analytics = AnalyticsDao()
  indicators = analytics.get_indicators()
  
  return make_response(indicators)

