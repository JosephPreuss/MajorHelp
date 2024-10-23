# MajorHelp

MajorHelp is a web application that helps students find universities, majors, and related information to assist them in making informed decisions. It includes features like user reviews, tuition calculators, and saved colleges for a personalized experience. For detailed descriptions and design decisions, refer to our [wiki pages](#link-to-wiki).

To run the web application locally, use `python manage.py runserver`. This will start the server at `http://127.0.0.1:8000/`.

For deployment, choose a hosting provider like Heroku, AWS, or DigitalOcean. Set up environment variables such as `DJANGO_SECRET_KEY`, `DATABASE_URL`, and other production-related variables. Migrate the database with `python manage.py migrate --noinput`, and collect static files using `python manage.py collectstatic --noinput`. Follow your hosting provider’s deployment steps, ensuring that sensitive credentials like passwords are not pushed to your Git repository.

Testing for the application is done using Django’s built-in testing framework. To run all the automated tests, use the command `python manage.py test`. This will execute the unit and integration tests within the application.

# Authors
- Alex Phakdy - aphakdy@email.sc.edu
- Brandon [add email]
- Corey [add email]
- Druv [add email]
- Joseph [add email]
