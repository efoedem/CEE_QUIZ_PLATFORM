import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QUIZ_PLATFORM.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def create_admin():
    print("Waiting for database...")
    time.sleep(3)
    try:
        # get_user_model() will now correctly point to 'users.User'
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'YourSecurePassword123')
            print("SUCCESS: Admin created for Custom User Model.")
        else:
            print("SKIP: Admin already exists.")
    except Exception as e:
        print(f"Error during admin creation: {e}")

if __name__ == "__main__":
    create_admin()