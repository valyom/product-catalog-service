#!/bin/sh


set -e

python manage.py collectstatic --noinput

python manage.py migrate

# Execute the command passed by Docker as the main container process.
exec "$@"