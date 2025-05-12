from flask import Flask
from modules.actor.controller import app_actor

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(app_actor)

@app.route("/")
def hello_world():
  return "<h1>Hidd<h1/>"




#usar apenas em desenvolvimento (reload automatico)
if __name__ == "__main__":
    app.run(debug=True)