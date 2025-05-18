#!/bin/bash

# Exit on error
set -e

# Check for environment variables
FLUSH_DATABASE=${FLUSH_DATABASE:-true}
RUN_MIGRATIONS=${RUN_MIGRATIONS:-true}
export DB_HOST=${DB_HOST:-localhost}
export DB_PORT=${DB_PORT:-5432}

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Clear migrations if requested on users and core apps
if [ "$FLUSH_DATABASE" = "true" ]; then
  echo "Clearing migrations..."
  find users/migrations -path users/migrations/__init__.py -prune -o -name "*.py" -exec rm -f {} \;
  find core/migrations -path core/migrations/__init__.py -prune -o -name "*.py" -exec rm -f {} \;
  echo "Migrations cleared"
fi

# Flush database if requested
if [ "$FLUSH_DATABASE" = "true" ]; then
  echo "Flushing database..."
  # Remove all migrations
  python manage.py flush --no-input
  echo "Database flushed"
fi

# Apply database migrations if enabled
if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Applying database migrations..."
  python manage.py makemigrations
  python manage.py migrate
else
  echo "Skipping database migrations as per configuration"
fi

# Compile translations
echo "Compiling language files..."
python manage.py compilemessages

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

# Run translation setup script if locales exist
if [ -d "locale" ]; then
    echo "Setting up translations..."
    python scripts/setup_translations.py
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "Starting server..."
exec "$@"