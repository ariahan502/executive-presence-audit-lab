# Deployment Notes

## Current state

The app is fully runnable locally and now has the minimum production hooks needed for a simple hosted deployment:

- `SECRET_KEY` can be provided through environment variables
- `DATABASE_PATH` can be provided through environment variables
- `gunicorn` is included in `requirements.txt`
- `Procfile` is present for platforms that support it

## What is still true

- This project still uses SQLite
- The current tracking and analytics flow writes directly to the app database
- There is no hosting provider configuration in the repo yet

## Recommended first deployment shape

Use a simple Python host first, then upgrade infra only if needed.

Suggested setup:
- one Flask web process using `gunicorn`
- persistent disk or volume for the SQLite file
- environment variables for `SECRET_KEY` and `DATABASE_PATH`

## Before deploying publicly

- choose a host such as Render, Railway, or Fly.io
- point `DATABASE_PATH` at persistent storage, not ephemeral disk
- rotate `SECRET_KEY`
- decide whether test/sample rows in `instance/app.db` should be removed
- confirm whether local SQLite is enough or whether you want Postgres
