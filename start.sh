#!/bin/sh
source /home/www/HU_xunta/bin/activate
nohup /home/www/HU_xunta/bin/newrelic-admin run-program /home/www/HU_xunta/bin/gunicorn_django --workers=2 -b 0.0.0.0:9998 --timeout=300&
