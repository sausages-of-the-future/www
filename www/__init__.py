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

from flask.ext.mail import Mail
mail = Mail()
mail.init_app(app)

from flask.ext.security import (
    Security,
    MongoEngineUserDatastore
)

from .models import User, Role
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from www import views

from www.greenpaper.views import paper
app.register_blueprint(paper)

from flask.ext.basicauth import BasicAuth
http_basic_user = os.environ.get('BASIC_AUTH_USERNAME')
http_basic_password = os.environ.get('BASIC_AUTH_PASSWORD')
if http_basic_user and http_basic_password:
    app.config['BASIC_AUTH_USERNAME'] = http_basic_user
    app.config['BASIC_AUTH_PASSWORD'] = http_basic_password
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)
