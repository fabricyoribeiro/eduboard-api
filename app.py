

from flask import Flask
from modules.actor.controller import app_actor
from modules.verb.controller import app_verb
from modules.object.controller import app_object
from modules.subject.controller import app_subject
from modules.result.controller import app_result
from modules.event.controller import app_event
from modules.analytics.controller import app_analytics
from modules.analytics.individual.controller import app_individual_analysis
from modules.login.controller import app_login

from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(app_actor)
app.register_blueprint(app_verb)
app.register_blueprint(app_object)
app.register_blueprint(app_subject)
app.register_blueprint(app_result)
app.register_blueprint(app_event)
app.register_blueprint(app_analytics)
app.register_blueprint(app_individual_analysis)
app.register_blueprint(app_login)


@app.route("/")
def hello_world():
  return "<h1>API online<h1/>"


if __name__ == "__main__":
    app.run(debug=True)