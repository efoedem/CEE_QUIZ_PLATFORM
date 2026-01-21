#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations to create database tables (Fixes the "auth_user" error)
python manage.py migrate

# Create the admin user automatically
python create_admin.py