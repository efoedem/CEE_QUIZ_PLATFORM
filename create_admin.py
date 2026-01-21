import os
import django
import time
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QUIZ_PLATFORM.settings')
django.setup()

# This automatically finds your User model, even if it's custom!
from django.contrib.auth import get_user_model

User = get_user_model()


def create_admin():
    print("Waiting for database to settle...")
    time.sleep(5)

    try:
        tables = connection.introspection.table_names()
        print(f"Tables found: {tables}")

        # Check for your custom user table 'users_user'
        if "users_user" in tables or "auth_user" in tables:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'YourSecurePassword123')
                print("SUCCESS: Admin user created in Custom User Table.")
            else:
                print("SKIP: Admin user already exists.")
        else:
            print("CRITICAL ERROR: No user table found at all!")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    create_admin()