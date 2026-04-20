# Architecture

DeployWatch is a single Flask application backed by SQLite.

```text
client ──> Flask API (deploywatch/app.py)
              ├── models.py     SQLite persistence
              ├── notifier.py   outgoing webhook
              └── rollback.py   shells out to scripts/rollback.sh
```

## Request flow

1. A CI job calls `POST /deployments` with the shared API key.
2. The deployment is stored and a notification is sent to the configured webhook.
3. The dashboard polls `GET /deployments` to render the latest rows.

## Storage

All state lives in one SQLite file whose location is controlled by `DATABASE_PATH`.
