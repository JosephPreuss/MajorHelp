# filepath: your_project/test_settings.py
from .settings import *  # Import all default settings
from django.db.models.signals import post_migrate
from django.apps import apps
from django.core.management import call_command
import os
import shutil
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the paths for the main and test databases
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level to the project root
MAIN_DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
TEST_DB_PATH = os.path.join(BASE_DIR, 'test_behavioral_db.sqlite3')

# Copy the main database to the test database only if it doesn't already exist
if not os.path.exists(TEST_DB_PATH):
    if os.path.exists(MAIN_DB_PATH):
        shutil.copy(MAIN_DB_PATH, TEST_DB_PATH)
        logger.info(f"Copied main database from {MAIN_DB_PATH} to {TEST_DB_PATH}")
    else:
        logger.warning(f"Main database not found at {MAIN_DB_PATH}. Test database will be empty.")
else:
    logger.info(f"Test database already exists at {TEST_DB_PATH}. Skipping copy.")

# Override the database settings to use the test database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite for simplicity
        'NAME': TEST_DB_PATH,  # Name of the test database
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
        logger.info(f"Test user created: {user.username}")


def populate_database(sender, **kwargs):
    # "runtime" imports
    FinancialAid = apps.get_model('MajorHelp', 'FinancialAid')
    University = apps.get_model('MajorHelp', 'University')
    Major = apps.get_model('MajorHelp', 'Major')

    # Check to see if the info already exists
    uni = University.objects.filter(name="exampleUni").first()
    # Check to see if the info already exists

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

        logger.info("Test database ready.")


# Connect the function to the post_migrate signal
post_migrate.connect(init)