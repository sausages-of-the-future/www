from flask.ext.script import Manager, Command, prompt_bool, prompt, prompt_pass, prompt_choices
from mongoengine import connect
from www import app, models
import json
import os

import_dir = '%s/import-data' % os.path.dirname(os.path.abspath(__file__))

class ImportData(Command):

    def run(self):
        models.Service.objects.delete()
        services_json = open("%s/services.json" % import_dir).read()
        services = json.loads(services_json)
        for service in services:
            service_ = models.Service()
            service_.name = service['name']
            service_.slug = service['slug']
            service_.policies = service['policies']
            service_.legislation = service['legislation']
            service_.save()

#register commands
manager = Manager(app)
manager.add_command('import-data', ImportData())

if __name__ == "__main__":
    manager.run()

