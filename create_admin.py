import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QUIZ_PLATFORM.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    try:
        # Check if the table exists before querying
        if "auth_user" in connection.introspection.table_names():
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'YourSecurePassword123')
                print("SUCCESS: Admin user created.")
            else:
                print("SKIP: Admin user already exists.")
        else:
            print("ERROR: Tables not found. Migration might have failed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_admin()