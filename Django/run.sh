#!/bin/sh
python manage.py makemigrations app
python manage.py migrate app
gunicorn 'app.wsgi' -b 0.0.0.0:80 --access-logfile - --log-level info --timeout 90