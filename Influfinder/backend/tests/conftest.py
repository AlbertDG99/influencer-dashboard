import os
import sys
import pytest

# Ensure project root is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import create_app
from backend.config import AppConfig


@pytest.fixture()
def app():
    config = AppConfig(
        secret_key="test",
        cors_origins=["http://localhost:5000"],
        log_level="DEBUG",
        enable_security_headers=False,
        flask_env="testing",
    )
    app = create_app(config)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
