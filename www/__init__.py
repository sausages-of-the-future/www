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
