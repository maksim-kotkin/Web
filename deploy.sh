#!/bin/bash
cd /home/kotkinmax/prj/Web/1.5-ci-cd/work_with_database
git pull origin new
source /home/kotkinmax/prj/Web/1.5-ci-cd/work_with_database/env/bin/activate
pip install -r /home/kotkinmax/prj/Web/1.5-ci-cd/work_with_database/requirements.txt
python manage.py migrate
sudo systemctl restart gunicorn
