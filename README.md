# News-App
Midnight Times News App - README.md
This document provides instructions for setting up and running the Midnight Times News App, a web application that allows users to search for news articles from around the world and view their search history.

Prerequisites:

Python 3.9 (https://www.python.org/downloads/)
pip (package installer for Python) - usually comes bundled with Python
A code editor or IDE (e.g., Visual Studio Code, PyCharm)
Installation:

Clone the repository:


git clone https://<https://github.com/akshay13127/News-App.git>

Install dependencies:


cd Midnight-Times-News-App
pip install -r requirements.txt

This will install all the necessary Python libraries listed in the requirements.txt file.

Database Setup:

The application uses Django and requires a database to store search history (optional) and user data (if implementing authentication). Here's a basic setup for a development environment using SQLite:

Edit settings.py in the project directory:
Set DATABASES settings to configure your database connection. By default, it's set to use an in-memory SQLite database suitable for development.
If you prefer a different database like PostgreSQL or MySQL, refer to their official documentation for configuration details.
Running the Application:

Migrate database schema (if applicable):


python manage.py migrate
This creates the necessary tables in your database based on the models defined in the application.

Setup Environment Variables:

Create a .env file in the project root directory.
Add the following environment variables:
makefile
Copy code
NEWS_API_KEY=<your_news_api_key>
SECRET_KEY=<your_django_secret_key>
DEBUG=True
export DJANGO_SETTINGS_MODULE=news_search.settings
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/0

Start Celery worker and beat:
celery -A news_project worker --loglevel=info
celery -A news_project beat --loglevel=info


Run the development server:
python manage.py runserver

This will start the Django development server, typically accessible at http://127.0.0.1:8000/ in your web browser.

Usage:

1. Open http://127.0.0.1:8000/ in your web browser.
2. You should see the search page where you can enter a keyword and submit your search.
3. The application will use the News API to fetch relevant articles and display them on the results page.
4. Additional functionalities like search history and user management depend on the implemented features. Refer to the application's code for details.


Notes:
This README provides a basic setup guide. Refer to Django documentation (https://docs.djangoproject.com/en/4.2/) for advanced configuration options.
Remember to replace <your_github_repo_url> with the actual URL of your repository when cloning it.
For production deployment, additional configuration and security considerations are required.


Additional Resources:
Django Documentation: https://docs.djangoproject.com/en/4.2/
News API: https://newsapi.org/
(Optional) django-allauth (for user authentication): https://django-allauth.readthedocs.io/en/latest/

Time Spent and Experience:

The project was completed over 3 days/2 hours.