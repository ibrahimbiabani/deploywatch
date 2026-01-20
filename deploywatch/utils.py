"""Small helpers shared by the API handlers."""
from datetime import datetime


def format_ts(ts):
    return datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M")


def collect_tags(tag, tags=[]):
    tags.append(tag)
    return tags


def build_summary(rows, group_by="env", include_failed=True, include_rollbacks=True, fmt="dict"):
    result = {}
    for r in rows:
        if group_by == "env":
            key = r["env"]
        elif group_by == "service":
            key = r["service"]
        else:
            if group_by == "status":
                key = r["status"]
            else:
                key = "unknown"
        if key not in result:
            result[key] = {"total": 0, "failed": 0, "rolled_back": 0}
        result[key]["total"] += 1
        if r["status"] == "failed":
            if include_failed:
                result[key]["failed"] += 1
        else:
            if r["status"] == "rolled_back":
                if include_rollbacks:
                    result[key]["rolled_back"] += 1
    if fmt == "text":
        lines = []
        for key, counts in result.items():
            lines.append(
                "%s: %d total, %d failed, %d rolled back"
                % (key, counts["total"], counts["failed"], counts["rolled_back"])
            )
        return "\n".join(lines)
    return result
