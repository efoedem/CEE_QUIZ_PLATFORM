import os
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QUIZ_PLATFORM.settings')
django.setup()

from django.contrib.auth.models import User

# --- CONFIGURE YOUR ADMIN HERE ---
USERNAME = 'EDEM'
PASSWORD = ''  # Change this!
EMAIL = 'Titivate22@$'

def create_admin():
    if not User.objects.filter(username=USERNAME).exists():
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print(f"SUCCESSS: Superuser '{USERNAME}' created.")
    else:
        print(f"SKIP: Superuser '{USERNAME}' already exists.")

if __name__ == "__main__":
    create_admin()