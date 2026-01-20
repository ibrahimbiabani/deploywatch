"""Trigger a rollback of a service to an earlier version."""
import subprocess


def run_rollback(service, version):
    cmd = f"./scripts/rollback.sh {service} {version}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout
