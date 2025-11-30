#!/bin/sh
set -e

# Wait for Postgres to be ready and run migrations, collectstatic, then start Gunicorn
# This simple loop will try to run migrations until they succeed.

echo "Waiting for DB and applying migrations..."

MAX_TRIES=30
i=0
until python manage.py migrate --noinput; do
  i=$((i+1))
  if [ "$i" -ge "$MAX_TRIES" ]; then
    echo "Migrations failed after $MAX_TRIES attempts, exiting."
    exit 1
  fi
  echo "Database unavailable - sleeping 3s (attempt: $i/$MAX_TRIES)"
  sleep 3
done

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Creating superuser if not exists..."
python manage.py create_or_get_superuser



echo "Starting Gunicorn..."
exec gunicorn backend.wsgi:application -b 0.0.0.0:${PORT:-8000} --workers 3
