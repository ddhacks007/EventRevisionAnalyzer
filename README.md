# EventRevisionAnalyzer

A basic boilerplate Django project prepped with poetry and Rollup. It uses the Django project default database SQLite.

## Setup

For history's sake, this setup was based off of the instructions here: https://builtwithdjango.com/blog/basic-django-setup.

1. We only test and develop this base project with Python 3.12 (specified in pyproject.toml). If you can't or don't want to install this version of Python, you can change the version requirement in pyproject.toml. While we can't guarantee other versions' compatibility, it is quite unlikely that recent versions will encounter any issues. You can install the [latest version of Python here](https://www.python.org/downloads/).

2. Install [poetry](https://python-poetry.org/docs/#installation). This allows us to run our project in a virtual environment and will handle the installation of Django and other python libraries.

3. Run `poetry install` to install dependencies.

4. Rename `myproject` to whatever you'd like your project to be named. You will want to change the name in `pyproject.toml`, the Django project directory name `myproject/`, `manage.py`, and `settings.py`.

5. Change `TIME_ZONE` in `settings.py` to your timezone.

6. Run `poetry run python manage.py migrate` to initialize your local database.

7. Create a superuser for your local Django instance. Run `poetry run python manage.py createsuperuser`. Be sure to save your username and password in a responsible location.

8. Install [node](https://nodejs.org/en).

9. Run `npm install`.

10. Run `npm run build`.

## Running the server

Run `poetry run python manage.py runserver`.

## Running other Django commands

See Django documentation for other commands, such as generating and applying migrations. Commands can be used as normal, preceded by `poetry run`. For example, see "Running the server" above.

## Running tests

To run python tests, use `poetry run pytest`.
To run TS/JS tests, use `npm run test`.
