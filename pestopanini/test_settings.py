# filepath: your_project/test_settings.py
from .settings import *  # Import all default settings
from django.db.models.signals import post_migrate
from django.apps import apps
import os

# Override the database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite for simplicity
        'NAME': 'test_behavioral_db.sqlite3',  # Name of the test database
    }
}

# Optional: Disable debug mode for behavioral tests
DEBUG = True  # (Going to keep it true for now)


def init(sender, **kwargs):
    create_test_user(sender, **kwargs)
    populate_database(sender, **kwargs)


# Function to create a test user
def create_test_user(sender, **kwargs):
    # Get the custom user model dynamically
    User = apps.get_model('MajorHelp', 'CustomUser')  # Replace 'MajorHelp' with the app name containing CustomUser
    # Try to retrieve the user if it already exists
    user = User.objects.filter(username="testuser", email="email@example.com").first()
    
    # If the user doesn't exist, create it
    if not user:
        user = User.objects.create_user(
            username="testuser",
            password="password",
            email="email@example.com",
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role="alumni"
        )
        print(f"Test user created: {user.username}")


def populate_database(sender, **kwargs):
    # "runtime" imports
    FinancialAid = apps.get_model('MajorHelp', 'FinancialAid')
    University = apps.get_model('MajorHelp', 'University')
    Major = apps.get_model('MajorHelp', 'Major')

    # Check to see if the info already exists
    uni = University.objects.filter(name="exampleUni").first()

    # Create if it doesn't already exist
    if not uni:
        exampleAid = FinancialAid.objects.create(name="exampleAid") 
        exampleUni = University.objects.create(name="exampleUni", slug="exampleUni", location="nowhere")

        exampleUni.applicableAids.add(exampleAid)

        Major.objects.create(
            major_name="exampleMajor", slug="exampleMajor", university=exampleUni,
            department='Humanities and Social Sciences'
        )



        MercuryU = University.objects.create(name="MercuryU", location="Borealis Plantia")

        Major.objects.create(
            major_name="Solar Engineering", university=MercuryU,
            department='Engineering and Technology'
        )

        FinancialAid.objects.create(name="Martian LIFE")

        MarsU = University.objects.create(name="MarsU", location="Olympus Mons")

        Major.objects.create(
            major_name="Lowland Terraforming", university=MarsU,
            department="Agriculture and Environmental Studies"
        )

        print("Test database ready.")


# Connect the function to the post_migrate signal
post_migrate.connect(init)