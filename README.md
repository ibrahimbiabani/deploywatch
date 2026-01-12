# DeployWatch

DeployWatch is a small service that records deployments across `dev`, `staging` and
`production`, exposes them over a REST API, and posts a message to a webhook whenever
something new ships.

## Features

- Record and query deployments (`/deployments`)
- Per-environment / per-service summaries (`/summary`)
- Webhook notifications on every new deployment
- Rollback trigger for a deployed service
- Minimal browser dashboard in `dashboard/`

## Getting started

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m deploywatch.app
```

The API listens on port 8080. Configuration lives in `deploywatch/config.py`; copy
`.env.example` to `.env` to override the database location and webhook URL.

### Docker

```bash
make build
docker run -p 8080:8080 deploywatch
```

### Dashboard

```bash
cd dashboard
npm install
npm run build
```

## API

| Method | Path                          | Description                       |
| ------ | ----------------------------- | --------------------------------- |
| GET    | `/health`                     | Liveness check                    |
| GET    | `/deployments?env=<env>`      | List recent deployments           |
| POST   | `/deployments`                | Record a deployment (needs key)   |
| GET    | `/summary?group_by=<field>`   | Aggregate counts                  |
| POST   | `/deployments/<id>/rollback`  | Roll a service back (needs key)   |
| POST   | `/import`                     | Bulk import from a YAML document  |

Authenticated endpoints expect the shared key in the `X-API-Key` header.

## Development

```bash
make install
make lint
make test
```

Open pull requests against `main`. See [docs/architecture.md](docs/architecture.md) for an
overview of how the pieces fit together.
