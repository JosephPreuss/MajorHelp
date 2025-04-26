# MajorHelp

MajorHelp is a web application that helps students find universities, majors, and related information to assist them in making informed decisions. It includes features like user reviews, tuition calculators, and saved colleges for a personalized experience. For detailed descriptions and design decisions, refer to our [wiki pages](https://github.com/SCCapstone/pestopanini/wiki).

# Installation

> [!NOTE]
> It is highly recommended to run MajorHelp with a [Python Virtual Environment](https://docs.python.org/3/library/venv.html), or **venv** so that dependencies for this project are kept local and not system wide. 
> This guide was written with virtual environments in mind, so some commands may have to be run while venv is activated.

> [!Important]
> This project uses Git Large File Storage (Git LFS) to handle large files such as the db.sqlite3 database.
> You must install Git LFS before cloning or pulling the repository. Otherwise, large files like the database will fail to download properly.

<!--
Step 1: Install Git LFS
Install Git LFS on your system:

Windows (via Chocolatey):

bash
Copy
Edit
choco install git-lfs
macOS (via Homebrew):

bash
Copy
Edit
brew install git-lfs
Linux (Debian/Ubuntu):

bash
Copy
Edit
sudo apt-get install git-lfs
Step 2: Initialize Git LFS
After installing, run this once to enable Git LFS globally:

bash
Copy
Edit
git lfs install
Step 3: Clone the Repository (if you haven’t already)
bash
Copy
Edit
git clone https://github.com/SCCapstone/pestopanini.git
cd pestopanini
Already Cloned It?
If you cloned the repo before installing Git LFS, make sure to fetch large files manually:

bash
Copy
Edit
git lfs pull
-->

## Windows
<details>
<summary>Windows Installation Guide</summary>

### Setting up Git LFS

Windows (via Chocolatey):

```powershell copy
choco install git-lfs
```

After installing, run this once to enable Git LFS globally:

```powershell copy
git lfs install
```

#### Already Cloned It?

If you cloned the repo before installing Git LFS, make sure to fetch large files manually:

```bash Copy
git lfs pull
```

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

### Setting up Git LFS

Linux (Debian/Ubuntu):

```bash copy
sudo apt-get install git-lfs
```

After installing, run this once to enable Git LFS globally:

```
git lfs install
```

#### Already Cloned It?

If you cloned the repo before installing Git LFS, make sure to fetch large files manually:

```bash Copy
git lfs pull
```



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


## Linux
<details>
<summary> Linux Guide </summary>

### Helper Script (bash)

A helper script has been provided for running the unit and behavioral tests for MajorHelp.
Tests will be run in a test database.
```bash copy
./run_tests.sh
```

The script can also accept a path argument to source tests from, by default it uses the working directory.

```bash copy
./run_tests.sh ./path/to/tests.py ./path/to/tests.side
```


To facilitate creating new tests, or to run the server in the test environment, use the ``-r`` flag or ``--run-test-server``.
```bash copy
./run_tests.sh --run-test-server
```

When you are finished, run the script run with the ``-c`` flag or ``--clean`` to remove the test database and clean any cache.
```bash copy
./run_test --clean
```
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
Placeholder data and descriptions are acquired from IPEDS