#!/bin/bash

echo "Waiting for PostgreSQL..."

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "Connected to PostgreSQL"

# apply database migrations
python manage.py migrate

# collect static files
python manage.py collectstatic --no-input --clear

exec "$@"
