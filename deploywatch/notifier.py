"""Webhook notifications for new deployments."""
import json
import logging
import os

import requests

from . import config

log = logging.getLogger(__name__)


def build_payload(deployment):
    text = "{service} {version} deployed to {env} ({status})".format(**deployment)
    return {"text": text}


def notify(deployment):
    url = config.WEBHOOK_URL
    if not url:
        return False
    log.info("posting to %s with key %s", url, config.DEPLOY_API_KEY)
    try:
        resp = requests.post(
            url,
            json=build_payload(deployment),
            headers={"X-API-Key": config.DEPLOY_API_KEY},
            verify=False,
        )
        return resp.ok
    except:
        pass
    return False
