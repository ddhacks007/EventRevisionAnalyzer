# EventRevisionAnalyzer

Event-Triggered Wikipedia Edits Analyzer for the Solar Industry

## Configuration Parameters

- **Use:** Used by Two Scripts for creating entries for Wiki titles and Events.  
  **Location:** Present in `.env` file.
- **Use:** Specifies the port number of the server.  
  **Location:** Present in `.env` file. Default value is `8000`.
- **Use:** Used by `CreateEventsOfInterest` script to create event entries in the database.  
  **Location:** Present in `.env` file. Points to the `events_data.csv` file, default location is the `doc` folder.
- **Use:** Used by `CreateTitlesOfInterest` script to create title entries.  
  **Location:** Present in `.env` file.
- **Use:** Provides the `RevisionManager` limit to the date range from the event-date.  
  **Location:** Present in `settings.py` file.

Steps to run this project

1. Run `poetry install` to install dependencies.

2. Run `poetry run python3 manage.py makemigrations` to generate the migrations

3. Run `poetry run python3 manage.py migrate` to apply migrations to the database

Before staring the process please run the tests and see if the test cases are passed

4. RUN `poetry run python3 manage.py test --settings=eventrevisionanalyzer.test_settings tests`

## Run the Async Workers (Django-q)

5.) Run `poetry run python3 manage.py qcluster`.

## Run the server

6.) Run `poetry run python3 manage.py runserver`.

## Run the script responsible for storing some Wiki Titles (Please refer to the Configuration Section to run for your own titles)

7.) Run `poetry run python3 CreateTitlesOfInterest.py`.

## Run the script responsible for storing the events from event_data.csv (Please refer to the Configuration Section to run for your own set of Events)

8.) Run `poetry run python3 CreateEventsOfInterest.py`.
