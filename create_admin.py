import os
import django
import time
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QUIZ_PLATFORM.settings')
django.setup()

from django.contrib.auth.models import User


def create_admin():
    # Wait 5 seconds for the DB to finish indexing
    print("Waiting for database to settle...")
    time.sleep(5)

    try:
        # Check tables again
        tables = connection.introspection.table_names()
        print(f"Tables found: {tables}")

        if "auth_user" in tables:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'YourSecurePassword123')
                print("SUCCESS: Admin user created.")
            else:
                print("SKIP: Admin already exists.")
        else:
            print("CRITICAL ERROR: auth_user table still missing!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    create_admin()