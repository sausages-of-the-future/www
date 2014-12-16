import os
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_restful.utils import cors

#app
app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))
db = MongoEngine(app)
cors = CORS(app, resources={r"/static/*": {"origins": "*"}})

from www import views
