#!/usr/bin/env sh
set -eu

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python manage.py collectstatic --noinput

if [ "${DJANGO_CREATE_SUPERUSER:-false}" = "true" ]; then
    python manage.py createsuperuser --noinput
fi

exec gunicorn multitenantsaas.wsgi:application --bind 0.0.0.0:${PORT:-8585} --workers "${GUNICORN_WORKERS:-3}" --threads "${GUNICORN_THREADS:-2}" --timeout "${GUNICORN_TIMEOUT:-60}"
