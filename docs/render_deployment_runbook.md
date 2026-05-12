# Render Deployment Runbook

## Why Render

Render is a good first host for this project because it supports:

- Python web services
- public HTTPS URLs
- persistent disks for SQLite-backed apps
- repo-based deploys with `render.yaml`

This matches the current app architecture without requiring a database migration first.

## What is configured in this repo

- `render.yaml` defines a Render web service
- the app reads `DATABASE_PATH` from environment variables
- the app reads `SECRET_KEY` from environment variables
- `run.py` now binds to `0.0.0.0` and uses the `PORT` environment variable
- the Render service is configured to mount a persistent disk at `/var/data`
- the SQLite database path is set to `/var/data/app.db`

## First deploy steps

1. Push this repo to GitHub.
2. In Render, create a new Blueprint or Web Service from the repo.
3. If using the Blueprint flow, Render should detect `render.yaml`.
4. Confirm these settings during setup:
   - plan: `starter`
   - disk mount path: `/var/data`
   - database path env var: `/var/data/app.db`
5. Create the service and wait for the first deploy to finish.
6. Open the Render URL and submit a test newsletter and consultation form.
7. If needed, open a shell and inspect `/var/data/app.db` to confirm persistence.

## Important caveats

- This app still uses SQLite, so it should run as a single-instance service.
- Render documents that services with attached persistent disks cannot be scaled horizontally.
- Render also documents that adding a persistent disk disables zero-downtime deploys.
- For larger real traffic or multi-instance needs, migrate to Postgres.

## Recommended first-production checks

- remove or clearly separate synthetic traffic before interpreting live conversion data
- rotate any old local test data if you do not want it in production
- verify that the persistent disk survives a manual redeploy
- add a `traffic_type` field if both synthetic and live traffic will coexist

## Suggested next upgrade path

If real usage starts to accumulate, the next infrastructure step should be:

1. migrate from SQLite to Postgres
2. tag synthetic vs. live traffic in analytics
3. add a small dashboard or scheduled report process
