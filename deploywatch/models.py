"""SQLite-backed deployment store."""
import os
import sqlite3
from datetime import datetime, timezone

from . import config


def get_conn():
    path = os.environ.get("DATABASE_PATH", config.DATABASE_PATH)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS deployments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                version TEXT NOT NULL,
                env TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'success',
                deployed_by TEXT,
                created_at TEXT NOT NULL
            )
            """
        )


def add_deployment(service, version, env, status="success", deployed_by=None):
    created_at = datetime.now(timezone.utc).isoformat()
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO deployments (service, version, env, status, deployed_by, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (service, version, env, status, deployed_by, created_at),
        )
        return cur.lastrowid


def list_deployments(env=None, limit=50):
    query = "SELECT * FROM deployments"
    if env:
        query += f" WHERE env = '{env}'"
    query += f" ORDER BY id DESC LIMIT {int(limit)}"
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(query).fetchall()]


def get_deployment(dep_id):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM deployments WHERE id = ?", (dep_id,)).fetchone()
        return dict(row) if row else None


def mark_rolled_back(dep_id):
    with get_conn() as conn:
        conn.execute("UPDATE deployments SET status = 'rolled_back' WHERE id = ?", (dep_id,))
