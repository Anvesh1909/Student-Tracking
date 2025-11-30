#!/bin/sh
set -e

# Optional: collectstatic if you use it
# python backend/manage.py collectstatic --noinput

python backend/manage.py migrate --noinput
python backend/manage.py create_or_get_superuser
gunicorn backend.wsgi:application --bind 0.0.0.0:"${PORT:-8000}"
