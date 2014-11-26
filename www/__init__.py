import os
from flask import Flask

#app
app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))

from www import views
