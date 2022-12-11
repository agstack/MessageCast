#!/bin/bash
python3.9 manage.py search_index --rebuild -y
python3.9 manage.py makemigrations
python3.9 manage.py migrate
python3.9 manage.py createsuperuser
gunicorn --bind 0.0.0.0:8000 AgStackRegistry.wsgi:application
