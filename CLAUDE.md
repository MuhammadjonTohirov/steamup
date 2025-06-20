# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
SteamUp Platform - Django REST API backend for an educational STEAM learning platform with multi-language support and JWT authentication.

## Development Commands

### Primary Development (Docker)
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services  
docker-compose down
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Database operations
python manage.py makemigrations
python manage.py migrate

# Run development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser
```

### Translation Management
```bash
# Generate translation files for all languages (en, uz, ru)
python manage.py makemessages -l uz -l ru -l en

# Compile translations
python manage.py compilemessages
```

### Utility Scripts
- `./clear_migrations.sh` - Clears all migration files for clean database reset
- `python initializer.py` - Populates initial data (learning domains, motivations, targets)

## Architecture

### Core Applications
- **`core/`** - Shared utilities, middlewares, and standardized API responses
- **`users/`** - User management, authentication, profiles, and onboarding
- **`steamup_platform/`** - Django project settings and configuration

### Key Architectural Patterns

**Standardized API Responses**: All API responses use the format:
```python
{"data": ..., "error": ..., "code": ...}
```
This is enforced by `core.middlewares.StandardResponseMiddleware`.

**Multi-language Support**: Uses Django Parler for model translations with language middleware (`core.middlewares.LanguageMiddleware`) that detects language from Accept-Language header.

**Authentication Flow**: 
- Email-based authentication (no usernames)
- JWT tokens via djangorestframework-simplejwt
- OTP-based email verification and password reset
- Custom User model with UUID primary keys

### Database Design
- PostgreSQL with UUID primary keys for users
- Translation tables via Django Parler
- Onboarding flow with learning domains, motivations, and targets

## API Documentation
- Swagger UI available at `/api/docs/`
- OpenAPI schema at `/api/schema/`
- Uses drf-spectacular for automatic API documentation

## Environment Setup
- Uses python-decouple for environment variables
- Docker setup includes PostgreSQL with auto-migration
- Default superuser created: admin@mail.uz / 123 (Docker only)

## File Locations
- Models: `users/models.py`, `core/models.py`
- API Views: `users/views.py`, `core/views.py`
- Serializers: `users/serializers.py`, `core/serializers.py`
- Middlewares: `core/middlewares.py`
- Translation files: `locale/*/LC_MESSAGES/django.po`