#!/bin/sh
sleep 15
python3 ./spikesystem/manage.py makemigrations &&
python3 ./spikesystem/manage.py migrate &&
python3 ./spikesystem/manage.py makemigrations account &&
python3 ./spikesystem/manage.py migrate --fake account zero &&
python3 ./spikesystem/manage.py migrate account &&
python3 ./spikesystem/manage.py makemigrations order &&
python3 ./spikesystem/manage.py migrate --fake order zero &&
python3 ./spikesystem/manage.py migrate order &&
python3 ./spikesystem/manage.py loaddata ./spikesystem/fixture.json &&
python3 ./spikesystem/manage.py runserver 0.0.0.0:8000
