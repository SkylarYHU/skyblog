#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput
gunicorn mysite.wsgi:application --bind 0.0.0.0:8080
