import os
from flask import Flask
from flask.ext.mongoengine import MongoEngine

#app
app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))
db = MongoEngine(app)
cors = CORS(app)

from www import views
