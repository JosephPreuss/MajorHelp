#!/bin/bash

# Function to print help statement
help() {
    printf "Usage $0 [OPTION] [PATH]\nA helper script for running the unit and behavioral tests for MajorHelp.\n"
    printf "Tests will be run in a test database, it and any cache can be cleaned with $0 --clean.\n"
    printf "\nOptional Flags:\n\t-c, --clean\t\tCleans up pycache and test database.\n"
    printf "\t-r, --run-test-server\tRuns the server with the test database, without any testing.\n"
    printf "\t-h, --help\t\tDisplays this message.\n"
    printf "\nOptional Positional Argument:\n"
    printf "\t[PATH]\t Specify where to look for tests (default: current directory).\n"
    
    printf "\nScript and testing by Joseph Preuss.\n"
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
    
    # Set up the test database
    echo "Applying migrations to set up the test database..."
    python manage.py migrate --settings=pestopanini.test_settings && 

    # Start the server in the background
    echo "Starting the server..." &&
    python manage.py runserver --settings=pestopanini.test_settings


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

# Parse options using get opt
TEMP=$(getopt -o crh --long clean,run-test-server,help -n "$0" -- "$@")

# check if getopt was successful
if [ $? != 0 ]; then
    echo "Error parsing options." >&2
    exit 1
fi

# Reorder arguments as parsed by getopt
eval set -- "$TEMP"

# Process
while true; do
    case $1 in
        -c|--clean)
            clean_directory
            exit 0
            ;;
        
        -r|--run-test-server)

            run_test_server
            exit 0
            ;;

        -h|--help)
            help
            exit 0
            ;;
        
        --)
            shift
            break
            ;;

        *)
            echo -e "Unrecognized option, -$1.\n\n" >&2
            help
            exit 1
            ;;
    esac
done


# Default Behavior, run tests.

# Shift processed options
shift $((OPTIND - 1))

# Activate the virtual environment
activate_venv

# Set up the test database
echo "Applying migrations to set up the test database..."
python manage.py migrate --settings=pestopanini.test_settings &&

# Start the server in the background, suppressing output
echo "Starting the server in the background..." &&
python manage.py runserver --settings=pestopanini.test_settings &> /dev/null &
SERVER_PID=$!

trap "kill $SERVER_PID; unset DJANGO_TEST_ENV; deactivate" EXIT

# Run the tests
echo "Running tests..."

# if $1 is given, then it will run pytest at that directory
pytest $1

# Kill the server process
echo "Stopping the server..."
pkill -f "manage.py runserver"

# Deactivate the virtual environment
deactivate

echo "All tests completed successfully."