# Render Preflight

## Goal

This checklist is for the final review right before creating the Render service.

## App assumptions

- The app is currently designed for one running web instance.
- SQLite is acceptable for the first hosted version.
- Persistent disk storage is required.
- Live reporting should use `traffic_type = 'live'`.

## Required files already in repo

- `render.yaml`
- `Procfile`
- `requirements.txt`
- `run.py`
- `docs/render_deployment_runbook.md`

## Environment values

Expected Render environment variables:

- `SECRET_KEY`
- `DATABASE_PATH=/var/data/app.db`
- `FLASK_DEBUG=0`

## Risks to remember

- SQLite is not a good long-term fit for horizontal scaling.
- Render persistent disks disable zero-downtime deploys.
- Synthetic seeded traffic exists in the current local database.
- Mixed-traffic reporting is unsafe unless queries filter by `traffic_type`.

## Recommended launch decision

Launch on Render if all of these are true:

- you want real traffic collection now
- a single-instance app is acceptable
- SQLite plus persistent disk is acceptable for the first phase
- you are comfortable migrating to Postgres later if usage grows

## Immediate follow-up after launch

1. Submit one newsletter test.
2. Submit one consultation test.
3. Verify live rows are labeled `traffic_type = 'live'`.
4. Create the first post-launch live-only report after a small amount of real traffic accumulates.
