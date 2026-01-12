"""Application configuration."""
import os

DEBUG = True
HOST = "0.0.0.0"
PORT = 8080

DATABASE_PATH = os.environ.get(
    "DATABASE_PATH", "/home/mkhan/projects/deploywatch/data/deploys.db"
)

ENVIRONMENTS = ["dev", "staging", "production"]

# Outgoing notifications
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")
WEBHOOK_TIMEOUT = 5

# Shared key that clients send in the X-API-Key header
DEPLOY_API_KEY = "dw_live_9f3a1c7e5b2d48a6b0c4e8f1a7d35c92"
