# Timetracker

**Timetracker** is a web application for tracking time that you spend on projects and tasks.
Its design follows Redmine's concept of issues and tasks.

The backend API is built with Flask, and the frontend client is a Vue.js single-page application.

## Running

To start Timetracker, you need Docker and Docker Compose. In the root directory, run:

```bash
docker-compose up
```

The app should be available at http://localhost:3000.
The `/backend` directory is mounted as a volume on start-up, and the application data is stored in the SQLite-managed `timetracker.db`
file.

## Tests

The API is covered with tests that use the Flask test client. In order to run the tests locally,

1. Go to `/backend` directory:

```bash
cd backend
```

2. Activate the virtualenv and install dependencies:

```
pipenv shell
pipenv install --dev
```

3. Run all tests:

```
pytest tests -v
```
