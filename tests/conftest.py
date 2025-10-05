"""Conftest for pytest fixtures."""

import pytest
from finsight.core.credentials import CredentialManager


@pytest.fixture
def encryption_key():
    """Provide an encryption key for tests."""
    return CredentialManager.generate_key()


@pytest.fixture
def mock_plaid_credentials():
    """Provide mock Plaid credentials."""
    return {
        'client_id': 'test_client_id',
        'secret': 'test_secret',
        'access_token': 'test_access_token'
    }


@pytest.fixture
def mock_kite_credentials():
    """Provide mock Kite credentials."""
    return {
        'api_key': 'test_api_key',
        'api_secret': 'test_api_secret',
        'access_token': 'test_access_token'
    }


@pytest.fixture
def mock_alphavantage_credentials():
    """Provide mock AlphaVantage credentials."""
    return {
        'api_key': 'test_api_key'
    }


@pytest.fixture
def mock_ccxt_credentials():
    """Provide mock CCXT credentials."""
    return {
        'exchange': 'binance',
        'api_key': 'test_api_key',
        'api_secret': 'test_api_secret'
    }
