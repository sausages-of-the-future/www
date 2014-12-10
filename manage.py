from flask.ext.script import Manager, Command, prompt_bool, prompt, prompt_pass, prompt_choices
from mongoengine import connect
from www import app, models
import json
import glob
import os

import_dir = '%s/import-data' % os.path.dirname(os.path.abspath(__file__))

class ImportData(Command):

    def run(self):
        models.Service.objects.delete()

        for file_name in glob.glob("/%s/services/*.json" % import_dir):
             with open(file_name, 'rb') as json_file:
                service = json.loads(json_file.read().decode(encoding='UTF-8'))
                service_ = models.Service()
                service_.name = service['name']
                service_.slug = service['slug']
                service_.policies = service['policies']
                service_.legislation = service['legislation']
                service_.minister= service['minister']
                service_.registers = service['registers']
                service_.service_base_url_config = service['service_base_url_config']
                service_.save()

                print("Saved %s" % service_.name)

#register commands
manager = Manager(app)
manager.add_command('import-data', ImportData())

if __name__ == "__main__":
    manager.run()

