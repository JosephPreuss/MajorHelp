# MajorHelp

MajorHelp is a web application that helps students find universities, majors, and related information to assist them in making informed decisions. It includes features like user reviews, tuition calculators, and saved colleges for a personalized experience. For detailed descriptions and design decisions, refer to our [wiki pages](https://github.com/SCCapstone/pestopanini/wiki).

# Installation

> [!NOTE]
> It is highly recommended to run MajorHelp with a [Python Virtual Environment](https://docs.python.org/3/library/venv.html), or **venv** so that dependencies for this project are kept local and not system wide. 
> This guide was written with virtual environments in mind, so some commands may have to be run while venv is activated.

## Windows
<details>
<summary>Windows Installation Guide</summary>

### Setting up venv and installing dependencies
To set up the virtual environment and install dependencies, run this code in powershell

```powershell copy
python -m venv venv\
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

<details>
<summary> (Using cmd?) </summary>

```cmd copy
py -m venv venv\
venv\Scripts\activate.bat
py -m pip install -r requirements.txt
```

</details>

<details>
<summary> (Execution policy error?) </summary>

If you're having issues executing ``venv\Scripts\activate.bat``, then you might have to update your execution policy

THIS CHANGE IS PERMAMENT AND AFFECTS SYSTEM GLOBALLY 

```powershell copy
set-executionpolicy remotesigned
```
Run this command as administrator 


Reset the execution policy with this

```powershell copy
set-executionpolicy restricted
```

</details>

<br>

This will create the virtual environment and place your shell inside it. 

### Running a local instance of MajorHelp

While **inside of the virtual environment**, run 

```powershell copy
python manage.py runserver
```

Exit the server by pressing Ctrl + C while in the shell.

<details>
<summary> (Using cmd?) </summary>

```cmd copy
py manage.py runserver
```

</details>



<br>

To host MajorHelp on a non local enviornment, see [Deployment](#deployment)

### Activating Venv

```powershell copy
venv\Scripts\Activate.ps1
```

<details>
<summary> (Using cmd?) </summary>

```cmd copy
venv\Scripts\activate.bat
```

</details>

### Exiting Venv

Simply run

```powershell copy
deactivate
```
</details>

## Linux
<details>
<summary>Linux Installation Guide</summary>

### Setting up venv and installing dependencies
To set up the virtual environment and install dependencies, run this code in your shell


```bash copy
python -m venv venv/
source venv/bin/activate
python -m pip install -r requirements.txt
```

<br>

This will create the virtual environment and place your shell inside it. 

<br>

<details>
<summary>(Not using bash?)</summary>

<table>
<tr><th> Shell </th><th> Command </th></tr>

<tr>
<td>
fish
</td>
<td>

```fish copy
python -m venv venv/
source venv/bin/activate.fish
python -m pip install -r requirements.txt
```

</td>
</tr>

<tr>
<td>
csh/tcsh
</td>
<td>

```csh copy
python -m venv venv/
source venv/bin/activate.csh
python -m pip install -r requirements.txt
```

</td>
</tr>


<tr>
<td>
pwsh
</td>
<td>

```powershell copy
python -m venv venv/
venv/bin/Activate.ps1
python -m pip install -r requirements.txt
```

</td>
</tr>

</table>


</details>


### Running a local instance of MajorHelp

While **inside of the virtual environment**, run 

``` copy
python manage.py runserver
```

Exit the server by pressing Ctrl + C while in the shell.

To host MajorHelp on a non local enviornment, see [Deployment](#deployment)

### Activating Venv

```bash copy
source venv/bin/activate
```

<details> 
<summary> (Not using bash?) </summary>

<table>
<tr><th> Shell </th><th> Command </th></tr>

<tr>
<td>
fish
</td>
<td>

```fish copy
source venv/bin/activate.fish
```

</td>
</tr>

<tr>
<td>
csh/tcsh
</td>
<td>

```csh copy
source venv/bin/activate.csh
```

</td>
</tr>


<tr>
<td>
pwsh
</td>
<td>

```pwsh copy
venv/bin/Activate.ps1
```

</td>
</tr>

</table>

</details>

### Exiting Venv

Simply run

```bash copy
deactivate
```

</details>

<br>

# Deployment
For deployment, choose a hosting provider like Heroku, AWS, or DigitalOcean. Set up environment variables such as DJANGO_SECRET_KEY, DATABASE_URL, and other production-related variables. Migrate the database with python manage.py migrate --noinput, and collect static files using python manage.py collectstatic --noinput. Follow your hosting provider’s deployment steps, ensuring that sensitive credentials like passwords are not pushed to your Git repository.

# Testing

> [!NOTE]
> Currently testing isn't supported on Windows devices. WSL may be a decent workaround, however behavioral tests can return false positives if the Linux Subsystem's browser does not load correctly.

<details>
See issue #190.
</details>

> [!NOTE]
> The following methods rely on ``pytest`` to handle the behavioral tests, however, pytest can occasionally return a false negative for a test in a non-deterministic way. As a fallback, tests are also stored in ``MajorHelp/behaviortests/selenium.side`` and can be run with the [Selenium IDE](https://www.selenium.dev/selenium-ide/)

<details>
See issue #191
</details>


## Linux
<details>
<summary> Linux Guide </summary>

### Method 1 - Helper Script (Bash)

A helper script has been provided for running the unit and behavioral tests for MajorHelp.
Tests will be run in a test database.
```bash copy
./run_tests.sh
```

The script can also accept a path argument to source tests from, by default it uses the working directory.

```bash copy
./run_tests.sh ./path/to/tests.py
```


To facilitate creating new tests, or to run the server in the test environment, use the ``-r`` flag or ``--run-test-server``.
```bash copy
./run_tests.sh --run-test-server
```

When you are finished, run the script run with the ``-c`` flag or ``--clean`` to remove the test database and clean any cache.
```bash copy
./run_test --clean
```

### Method 2 - Manual
<details>

#### Prerequisites

First, start by activating the virtual environment if you haven't already

```bash copy
source venv/bin/activate
```

Then, set up the test environment
```bash copy
python manage.py migrate --settings=pestopanini.test_settings
```

Next, make sure you have a local instance of the server running, preferably in another terminal
(Make sure you're activated)

```bash copy
python manage.py runserver --settings=pestopanini.test_settings
```


#### Running the tests

While the server is running, simply run 

```bash copy
pytest
```

and both the unit and behavioral tests will run.
</details>



</details>

<br>


# Credits



## Authors
- Alex Phakdy - aphakdy@email.sc.edu 
- Brandon - boriley@email.sc.edu
- Corey - coreysr@email.sc.edu 
- Druv - druv@email.sc.edu
- Joseph jpreuss@email.sc.edu

This project uses [Django](https://www.djangoproject.com/). <br>
Placeholder data and descriptions are acquired from usnews.com