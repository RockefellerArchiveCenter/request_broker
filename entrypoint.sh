#!/bin/bash

set -e

echo "Waiting for PostgreSQL..."

# Create config.py if it doesn't exist
if [ ! -f request_broker/config.py ]; then
    echo "Creating config file"
    cp request_broker/config.py.example request_broker/config.py
fi

./wait-for-it.sh db:5432 -- echo "Apply database migrations"
python manage.py migrate

# Create default users when running locally
# If this blows up, you likely need to add a DJANGO_SUPERUSER_USERNAME to config.py
if [[ -z "${TRAVIS_CI}" ]]; then
    echo "Creating default users"
    python manage.py shell < ./create_users.py
fi

#Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:${APPLICATION_PORT}
