import os
import pytest
from dotenv import load_dotenv

# Helper function to load the API key from .env
def load_api_key(dotenv_path=None):
    load_dotenv(dotenv_path=dotenv_path)
    return os.getenv("GOOGLE_API_KEY")

@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    # Ensure environment is clean before each test
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    yield
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

def test_env_key_loaded(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("GOOGLE_API_KEY=test_key_123")
    key = load_api_key(dotenv_path=str(env_file))
    assert key == "test_key_123"


def test_env_key_missing(tmp_path):
    # Use a temp directory with no .env file
    key = load_api_key(dotenv_path=str(tmp_path / ".env"))
    assert key is None


def test_env_key_malformed(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("GOOGLE_API_KEY")  # Malformed line
    key = load_api_key(dotenv_path=str(env_file))
    assert key is None
