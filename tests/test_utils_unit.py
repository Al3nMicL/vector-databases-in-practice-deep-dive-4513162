import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Ensure project root is in sys.path for utils import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import connect_to_demo_db, connect_to_my_db

@patch("utils.weaviate.connect_to_wcs")
def test_connect_to_my_db_success(mock_connect):
    mock_client = MagicMock()
    mock_connect.return_value = mock_client
    os.environ["GOOGLE_API_KEY"] = "fake_key"
    os.environ["WEAVIATE_CLUSTER_URL"] = "fake_url"
    os.environ["WEAVIATE_API_KEY"] = "fake_api_key"
    client = connect_to_my_db()
    mock_connect.assert_called_once()
    assert client == mock_client

@patch("utils.weaviate.connect_to_wcs")
def test_connect_to_my_db_missing_key(mock_connect):
    if "GOOGLE_API_KEY" in os.environ:
        del os.environ["GOOGLE_API_KEY"]
    os.environ["WEAVIATE_CLUSTER_URL"] = "fake_url"
    os.environ["WEAVIATE_API_KEY"] = "fake_api_key"
    client = connect_to_my_db()
    mock_connect.assert_called_once()
    assert client == mock_connect.return_value

@patch("utils.weaviate.connect_to_wcs")
def test_connect_to_demo_db_success(mock_connect):
    mock_client = MagicMock()
    mock_connect.return_value = mock_client
    os.environ["GOOGLE_API_KEY"] = "fake_key"
    os.environ["DEMO_WEAVIATE_URL"] = "demo_url"
    os.environ["DEMO_WEAVIATE_RO_KEY"] = "demo_ro_key"
    client = connect_to_demo_db()
    mock_connect.assert_called_once()
    assert client == mock_client
