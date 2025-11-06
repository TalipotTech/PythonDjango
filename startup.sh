#!/bin/bash

# Azure App Service startup script for Django
# This script runs when the container starts

echo "Starting Ensate Django Backend..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements_production.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate --noinput

# Create superuser if not exists (optional)
# python manage.py createsuperuser --noinput || true

# Start Gunicorn
gunicorn questionnaire_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info
