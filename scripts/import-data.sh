#!/bin/bash
source /vagrant/script/dev-env-functions
source ../environment.sh
init_virtual_env "www"
python manage.py import-data
deactivate
