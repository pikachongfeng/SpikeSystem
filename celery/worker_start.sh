#!/bin/sh
sleep 10
cd spikesystem
celery -A spikesystem worker -l info