#!/bin/sh
sleep 15
cd spikesystem
python3 manage.py makemigrations &&
python3 manage.py migrate &&
python3 manage.py makemigrations account &&
python3 manage.py migrate --fake account zero &&
python3 manage.py migrate account &&
python3 manage.py makemigrations order &&
python3 manage.py migrate --fake order zero &&
python3 manage.py migrate order &&
python3 manage.py loaddata fixture.json &&
python3 manage.py runserver 0.0.0.0:8000
