#!/bin/bash

./wait-for-it.sh db:5432 -- echo "Apply database migrations"
python manage.py migrate

#Start server
echo "Starting server"
apache2ctl -D FOREGROUND