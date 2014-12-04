#!/bin/bash
source /vagrant/script/dev-env-functions
source_app_environment "www"
init_virtual_env "www"
python manage.py import-data
deactivate
