#!/bin/bash

# Function to print help statement
help() {
    printf "Usage $0 [OPTION]\nA helper script for running the unit and behavioral tests for MajorHelp.\nTests will be run in a test database, it and any cache can be cleaned with $0 --clean.\n\nOptional Flags:\n\t-c, --clean\t\tCleans up pycache and test database.\n\t-r, --run-test-server\tRuns the server with the test database, without any testing.\n\t-h, --help\t\tDisplays this message.\n\nScript and testing by Joseph Preuss.\n"
}


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

# Function to run the test server without testing.
run_test_server() {

    # Activate the virtual environment
    activate_venv
    
    # Set the environment variable for the test environment
    export DJANGO_TEST_ENV=true

    # Set up the test database
    echo "Applying migrations to set up the test database..."
    python manage.py migrate --settings=pestopanini.test_settings && 

    # Start the server in the background
    echo "Starting the server..." &&
    python manage.py runserver --settings=pestopanini.test_settings

    # Clear the DJANGO_TEST_ENV environment variable
    unset DJANGO_TEST_ENV

    # Deactivate the virtual environment
    deactivate
}


activate_venv() {
    # check if the venv exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "Error: Virtual environment not found. Please set up the virtual environment first."
        echo "HINT: python -m venv venv/"
        exit 1
    fi
}

# Check for the --clean option
if [ "$1" == "-c" ] || [ "$1" == "--clean" ]; then
    clean_directory
    exit 0
fi

# Check for the run server option
if [ "$1" == "-r" ] || [ "$1" == "--run-test-server" ]; then
    run_test_server
    exit 0
fi

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    help
    exit 0
fi

if [ "$1" != '' ]; then
    echo -e "Unrecognized option, $1.\n\n"
    help
    exit 1
fi

# Activate the virtual environment
activate_venv

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