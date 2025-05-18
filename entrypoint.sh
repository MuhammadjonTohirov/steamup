#!/bin/bash

# Exit on error
set -e

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Checking if superuser exists..."
python << END
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'steamup_platform.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(email='admin@mail.uz').exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin@mail.uz', '123', is_verified=True)
    print("Superuser created.")
else:
    print("Superuser already exists.")
END

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "Starting server..."
exec "$@"
