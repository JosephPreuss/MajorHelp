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

# Function to run Selenium Side Runner for .side files
run_selenium_tests() {
    local path=$1

    # Resolve the path name for display
    local pathName
    if [ "$path" = "." ]; then
        pathName="current directory"
    else
        pathName="$path"
    fi

    echo "Running Selenium tests in $pathName..."

    # Search for .side files recursively
    local found=false
    while IFS= read -r -d '' file; do
        echo "Running $file..."
        node_modules/.bin/selenium-side-runner -c "browserName=firefox" "$file"
        found=true
    done < <(find "$path" -type f -name "*.side" -print0)

    if [ "$found" = false ]; then
        echo "No .side files found in $pathName, skipping..."
    fi
}

# Function to run Python tests using pytest
run_unit_tests() {
    local path=$1

    local pathName
    if [ "$path" = "." ]; then
        pathName="current directory"
    else
        pathName="$path"
    fi

    echo "Running unit tests in $pathName..."
    pytest "$path" 
}




# Parse options using get opt
TEMP=$(getopt -o crh --long clean,run-test-server,help -n "$0" -- "$@")

# check if getopt was successful
if [ $? != 0 ]; then
    echo "Error parsing options." >&2
    ex
# Reorder arguments as parsed by getopt
it 1
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

# Check if selenium side-runner is installed
# at node_modules/.bin/selenium-side-runner
runBehavioralTests=
if [ ! -f "node_modules/.bin/selenium-side-runner" ]; then
    printf "\033[1;33m" # Red text

    printf "WARN: selenium-side-runner not found at \n\n"

    printf "\033[0m" # Reset formatting
    printf "\t./node_modules/.bin/selenium-side-runner \n\n"
    printf "\033[1;33m" # Red text

    printf "Please install it to run behavioral tests.\n\n"
    printf "HINT: npm install selenium-side-runner\n\n"

    printf "\033[0m" # Reset formatting

    runBehavioralTests=false
    sleep 1
else
    runBehavioralTests=true
fi


# Shift processed options
shift $((OPTIND - 1))
TEST_PATH=${1:-.} # Default to current directory if no path is provided

# Activate the virtual environment
activate_venv


# Set up the test database
echo "Applying migrations to set up the test database..."
python manage.py migrate --settings=pestopanini.test_settings &&

sleep 2


# Start the server in the background, suppressing output
echo "Starting the server in the background..." &&
python manage.py runserver --settings=pestopanini.test_settings &> /dev/null &
SERVER_PID=$!


# set up trap to kill the server and deactivate the virtual environment
# in case of unexpected exit
trap "kill $SERVER_PID; unset DJANGO_TEST_ENV; deactivate" EXIT

sleep 2

# Run the unit tests
echo "Running unit tests..."

# Run unit tests
run_unit_tests "$TEST_PATH"



# Run Selenium tests for .side files
if [[ "$runBehavioralTests" == "true" ]]; then
    echo "Running behavioral tests..."
    run_selenium_tests "$TEST_PATH"
else
    echo "Skipping behavioral tests."
fi



# Kill the server process
echo "Stopping the server..."
pkill -f "manage.py runserver"


if [[ "$runBehavioralTests" == "false" ]]; then
    echo "NOTE:Behavioral tests were skipped. Due to missing selenium-side-runner."
fi