#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# 1. Collect static files
python manage.py collectstatic --no-input

# 2. Hard Reset: Clear migration history for the 'quiz' app
# (This fixes the "No migrations to apply" while the DB is empty)
python manage.py migrate --fake-initial

# 3. The "Force" Command
python manage.py migrate --run-syncdb

# 4. Final sync
python manage.py migrate

# 5. Create the admin user
python create_admin.py