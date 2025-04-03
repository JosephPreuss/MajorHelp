#!/bin/bash

# Function to clean the working directory
clean_directory() {
    echo "Cleaning the working directory..."
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type d -name ".pytest_cache" -exec rm -rf {} +
    if [ -f "test_behavioral_db.sqlite3" ]; then
        rm test_behavioral_db.sqlite3
        echo "Removed test database: test_behavioral_db.sqlite3"
    fi
    echo "Clean complete."
}

# Check for the --clean option
if [ "$1" == "--clean" ]; then
    clean_directory
    exit 0
fi

# Activate the virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Please set up the virtual environment first."
    exit 1
fi

# Set the environment variable for the test environment
export DJANGO_TEST_ENV=true

# Set up the test database
echo "Applying migrations to set up the test database..."
python manage.py migrate --settings=pestopanini.test_settings

# Start the server in the background, suppressing output
echo "Starting the server in the background..."
python manage.py runserver --settings=pestopanini.test_settings &> /dev/null &
SERVER_PID=$!

# Run the tests
echo "Running tests..."
pytest

# Kill the server process
echo "Stopping the server..."
kill $SERVER_PID

# Clear the DJANGO_TEST_ENV environment variable
unset DJANGO_TEST_ENV

# Deactivate the virtual environment
deactivate

echo "All tests completed successfully."