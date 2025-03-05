# MajorHelp

MajorHelp is a web application that helps students find universities, majors, and related information to assist them in making informed decisions. It includes features like user reviews, tuition calculators, and saved colleges for a personalized experience. For detailed descriptions and design decisions, refer to our [wiki pages](https://github.com/SCCapstone/pestopanini/wiki).

## Installation

> [!NOTE]
> It is highly recommended to run MajorHelp with a [Python Virtual Environment](https://docs.python.org/3/library/venv.html) so that dependencies for this project are kept local and not system wide. 
> This guide was written with virtual environments in mind, so some commands may have to be run while inside the environment

{% Windows %}
    Hello World!

{% endWindows %}

{% Linux %}
    Goodbye!
{% endLinux %}


## Deployment
For deployment, choose a hosting provider like Heroku, AWS, or DigitalOcean. Set up environment variables such as DJANGO_SECRET_KEY, DATABASE_URL, and other production-related variables. Migrate the database with python manage.py migrate --noinput, and collect static files using python manage.py collectstatic --noinput. Follow your hosting provider’s deployment steps, ensuring that sensitive credentials like passwords are not pushed to your Git repository.

## Testing



To run the behavioral tests, move to that folder location and use the command:
py -m pytest .\test_clickLogIn.py
py -m pytest .\test_searchwithnothing.py
py -m pytest .\test_testcontactandabout.py
py -m pytest .\test_calcminimum.py

The test files are located in the base MajorHelp directory, specifically in MajorHelp/tests.py.
To run all the unit tests, use the command:

```bash
python manage.py test
```

## Credits

### Authors
- Alex Phakdy - aphakdy@email.sc.edu 
- Brandon - boriley@email.sc.edu
- Corey - coreysr@email.sc.edu 
- Druv - druv@email.sc.edu
- Joseph jpreuss@email.sc.edu


Placeholder data and descriptions are acquired from usnews.com