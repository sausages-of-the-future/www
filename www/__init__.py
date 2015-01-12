import os
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.cors import CORS

import redis

#app
app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))
db = MongoEngine(app)
cors = CORS(app, resources={r"/static/*": {"origins": "*"}})
redis_client = redis.from_url(app.config['REDISCLOUD_URL'])

from www import views
