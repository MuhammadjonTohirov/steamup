# SteamUp Platform Backend

A Django REST API backend for the SteamUp educational platform.

## Features

- Custom user model with email-based authentication
- JWT authentication using Simple JWT
- OTP-based email verification and password reset
- User onboarding flow with profile creation
- Configuration API for theming and app settings
- Standardized API response format: `{"data": ..., "error": ..., "code": ...}`
- Comprehensive test suite

## Prerequisites

- Python 3.8+
- PostgreSQL

## Setup and Installation

You can set up the project either locally or using Docker.

### Option 1: Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/steamup-platform.git
cd steamup-platform
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a PostgreSQL database

```sql
CREATE DATABASE steamup;
CREATE USER applebro WITH PASSWORD '123123';
ALTER ROLE applebro SET client_encoding TO 'utf8';
ALTER ROLE applebro SET default_transaction_isolation TO 'read committed';
ALTER ROLE applebro SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE steamup TO applebro;
```

### 5. Create a .env file

Create a `.env` file in the project root with the following contents:

```
SECRET_KEY=your-secret-key
DEBUG=True

# Database settings
DB_NAME=steamup
DB_USER=applebro
DB_PASSWORD=123123
DB_HOST=localhost
DB_PORT=5432

# Email settings for production
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
```

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

The initial data (learning domains and app configuration) will be created automatically.

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

### Option 2: Docker Setup

1. Make sure you have Docker and Docker Compose installed.

2. Create a `.env` file as described above in step 5.

3. Build and start the containers:

```bash
docker-compose up -d
```

This will:
- Start a PostgreSQL database
- Run migrations
- Create a superuser (admin@mail.uz / 123) if it doesn't exist
- Start the Django application

4. Access the application at http://localhost:8000

## API Documentation

API documentation is available at `/api/docs/` when the server is running.

## Testing

Run the test suite with:

```bash
python manage.py test
```

## API Endpoints

### Authentication

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login with email/password
- `POST /api/auth/token/refresh/` - Refresh access token

### Email Verification

- `POST /api/auth/request-otp/` - Request OTP for email verification
- `POST /api/auth/verify-otp/` - Verify OTP and activate account

### Password Reset

- `POST /api/auth/forgot-password/` - Send OTP for password reset
- `POST /api/auth/verify-reset-otp/` - Verify password reset OTP
- `POST /api/auth/reset-password/` - Set new password

### User Profile

- `GET /api/profile/` - Get user profile
- `POST /api/profile/` - Create user profile
- `PUT /api/profile/` - Update user profile

### Onboarding

- `GET /api/onboarding/options/` - Get onboarding options (domains, etc.)

### Configuration

- `GET /api/config/theme/` - Get theming configuration
