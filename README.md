# Timetracker

The **Timetracker** is an application to track time spent on tickers, it follows Redmine's design of issues and tasks.

API is built with Flask, and the frontend client is a Vue.js single-page application.

## Running

```bash
docker-compose up
```

The app should be available at `http://localhost:3000`.
The `/backend` directory is mounted as a volume on start-up, and the application data is stored in the SQLite-managed `timetracker.db`
file.

## Tests

In order to run API tests locally, do the following.

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
