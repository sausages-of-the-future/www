import os
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.cors import CORS

#app
app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))
db = MongoEngine(app)
cors = CORS(app, resources={r"/static/*": {"origins": "*"}})

from messenger import Locator
locator = Locator(app)

from www import views
