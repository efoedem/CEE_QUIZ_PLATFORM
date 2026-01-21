#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Force create tables if they are missing
python manage.py migrate --run-syncdb

# Create the admin user
python create_admin.py