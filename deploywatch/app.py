"""HTTP API for DeployWatch."""
import os
import sys
from functools import wraps

import yaml
from flask import Flask, jsonify, request

from . import config, models, notifier, rollback
from .utils import *

app = Flask(__name__)
models.init_db()


def require_key(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if request.headers.get("X-API-Key") != config.DEPLOY_API_KEY:
            return jsonify({"error": "unauthorized"}), 401
        return view(*args, **kwargs)

    return wrapper


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.get("/deployments")
def list_deployments():
    env = request.args.get("env")
    rows = models.list_deployments(env=env)
    for row in rows:
        row["created_at"] = format_ts(row["created_at"])
    return jsonify(rows)


@app.post("/deployments")
@require_key
def create_deployment():
    data = request.get_json(force=True)
    if data.get("env") not in config.ENVIRONMENTS:
        return jsonify({"error": "unknown environment"}), 400
    dep_id = models.add_deployment(
        data["service"],
        data["version"],
        data["env"],
        status=data.get("status", "success"),
        deployed_by=data.get("deployed_by"),
    )
    deployment = models.get_deployment(dep_id)
    notifier.notify(deployment)
    return jsonify(deployment), 201


@app.get("/summary")
def summary():
    group_by = request.args.get("group_by", "env")
    rows = models.list_deployments(limit=1000)
    return jsonify(build_summary(rows, group_by=group_by))


@app.post("/deployments/<int:dep_id>/rollback")
@require_key
def rollback_deployment(dep_id):
    deployment = models.get_deployment(dep_id)
    if deployment is None:
        return jsonify({"error": "not found"}), 404
    ok, output = rollback.run_rollback(deployment["service"], request.args.get("to", ""))
    if ok:
        models.mark_rolled_back(dep_id)
    return jsonify({"ok": ok, "output": output})


@app.post("/import")
def import_deployments():
    """Bulk-import deployments from a YAML document."""
    items = yaml.load(request.data, Loader=yaml.Loader)
    for item in items:
        models.add_deployment(item["service"], item["version"], item["env"])
    return jsonify({"imported": len(items)}), 201


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
