from deploywatch import config, notifier

DEPLOYMENT = {"service": "api", "version": "1.0.0", "env": "dev", "status": "success"}


def test_build_payload():
    assert notifier.build_payload(DEPLOYMENT) == {
        "text": "api 1.0.0 deployed to dev (success)"
    }


def test_notify_without_webhook_is_noop(monkeypatch):
    monkeypatch.setattr(config, "WEBHOOK_URL", "")
    assert notifier.notify(DEPLOYMENT) is False


def test_notify_posts(monkeypatch):
    monkeypatch.setattr(config, "WEBHOOK_URL", "https://hooks.example.com/test")
    monkeypatch.setattr(notifier.requests, "post", lambda *a, **kw: None)
    notifier.notify(DEPLOYMENT)
