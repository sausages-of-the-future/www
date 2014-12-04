from flask.ext.script import Manager, Command, prompt_bool, prompt, prompt_pass, prompt_choices
from mongoengine import connect
from www import app, models
import json
import os

import_dir = '%s/import-data' % os.path.dirname(os.path.abspath(__file__))

class ImportData(Command):

    def run(self):
        services_json = open("%s/services.json" % import_dir).read()
        services = json.loads(services_json)


#register commands
manager = Manager(app)
manager.add_command('import-data', ImportData())

if __name__ == "__main__":
    manager.run()

