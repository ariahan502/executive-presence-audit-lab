# Launch Checklist

## Repo

- Confirm the latest code is pushed to GitHub.
- Confirm `render.yaml` is present at the repo root.
- Confirm `requirements.txt` includes `gunicorn`.
- Confirm `run.py` binds to `0.0.0.0` and respects `PORT`.

## Render setup

- Create a new Render Blueprint or Web Service from the GitHub repo.
- Confirm the service name is correct.
- Confirm the plan is appropriate for a single-instance SQLite app.
- Confirm the persistent disk is attached.
- Confirm the disk mount path is `/var/data`.
- Confirm `DATABASE_PATH=/var/data/app.db`.
- Confirm `SECRET_KEY` is generated/set.
- Confirm `FLASK_DEBUG=0`.

## First deploy

- Wait for the first deploy to complete successfully.
- Open the public Render URL.
- Verify the home page loads.
- Verify at least one article page loads.
- Verify the newsletter page loads.
- Verify the consultation page loads.

## Functional checks

- Submit a test newsletter signup.
- Submit a test consultation request.
- Confirm both requests succeed in the UI.
- Confirm the app still loads after submissions.

## Persistence checks

- Trigger a manual redeploy or restart in Render.
- Recheck that the app still loads.
- Confirm the database file still exists on the persistent disk.
- Confirm test submissions still exist after restart.

## Reporting checks

- Rematerialize analytics if needed.
- Use `traffic_type = 'live'` for all real reporting queries.
- Keep synthetic seeded traffic out of live decision-making.

## Post-launch

- Record the public URL.
- Record the deploy date.
- Record the first live test submission date.
- Decide when to review the first live-only funnel report.
