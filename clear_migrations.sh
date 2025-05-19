#!/bin/bash

# clear migrations on apps
echo "Clearing migrations..."

# Clear users app migrations
find ./users/migrations -type f -not -name '__init__.py' -delete

# Clear core app migrations
find ./core/migrations -type f -not -name '__init__.py' -delete

echo "Migrations cleared successfully!"
