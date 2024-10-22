#!/bin/bash
cd 1.5-ci-cd/work_with_database
git pull origin new
source 1.5-ci-cd/work_with_database/env/bin/activate
pip install -r 1.5-ci-cd/work_with_database/requirements.txt
python manage.py migrate
sudo systemctl restart gunicorn
