from flask.ext.script import Manager, Command, prompt_bool, prompt, prompt_pass, prompt_choices
from mongoengine import connect
from www import app, models, user_datastore
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
                service_.description = service['description']
                service_.slug = service['slug']
                service_.policies = service['policies']
                service_.legislation = service['legislation']
                service_.minister= service['minister']
                service_.registers = service['registers']
                service_.guides = service['guides']
                try:
                    service_.stats = service['stats']
                except:
                    pass
                service_.service_base_url_config = service['service_base_url_config']
                service_.save()

                print("Saved %s" % service_.name)



class CreateUser(Command):
    """
    Creates an admin user of www app. Primarily for processing user account applications
    """
    def run(self):
        from flask_security.utils import encrypt_password
        email = prompt('email')
        password = prompt_pass('password')
        if not models.User.objects.filter(email=email).first():
            user = user_datastore.create_user(email=email, password=encrypt_password(password))
            admin_role = user_datastore.find_or_create_role('ADMIN')
            user_datastore.add_role_to_user(user, admin_role)
        else:
            print("User with email:", email, "already exists")

#register commands
manager = Manager(app)
manager.add_command('import-data', ImportData())
manager.add_command('create-user', CreateUser())

if __name__ == "__main__":
    manager.run()

