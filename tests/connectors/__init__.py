"""Tests for base connector functionality."""

import pytest
from finsight.connectors.base import (
    BaseConnector,
    AuthType,
    ConnectorResponse,
    ConnectorStatus
)


class MockConnector(BaseConnector):
    """Mock connector for testing."""
    
    @property
    def provider_name(self) -> str:
        return "mock"
    
    @property
    def auth_type(self) -> AuthType:
        return AuthType.API_KEY
    
    def _validate_credentials(self) -> None:
        if 'api_key' not in self.credentials:
            raise ValueError("api_key required")
    
    def authenticate(self) -> ConnectorResponse:
        return ConnectorResponse(status=ConnectorStatus.SUCCESS)
    
    def get_accounts(self) -> ConnectorResponse:
        return ConnectorResponse(
            status=ConnectorStatus.SUCCESS,
            data={'accounts': []}
        )
    
    def get_transactions(self, account_id, start_date=None, end_date=None) -> ConnectorResponse:
        return ConnectorResponse(
            status=ConnectorStatus.SUCCESS,
            data={'transactions': []}
        )
    
    def get_balances(self, account_id) -> ConnectorResponse:
        return ConnectorResponse(
            status=ConnectorStatus.SUCCESS,
            data={'balance': 0}
        )


class TestBaseConnector:
    """Test BaseConnector functionality."""
    
    def test_connector_initialization(self):
        """Test connector initialization."""
        credentials = {'api_key': 'test_key'}
        connector = MockConnector(credentials)
        
        assert connector.credentials == credentials
        assert connector.provider_name == "mock"
        assert connector.auth_type == AuthType.API_KEY
    
    def test_credential_validation(self):
        """Test credential validation."""
        with pytest.raises(ValueError, match="api_key required"):
            MockConnector({})
    
    def test_authenticate(self):
        """Test authentication."""
        connector = MockConnector({'api_key': 'test_key'})
        result = connector.authenticate()
        
        assert result.status == ConnectorStatus.SUCCESS
    
    def test_get_accounts(self):
        """Test getting accounts."""
        connector = MockConnector({'api_key': 'test_key'})
        result = connector.get_accounts()
        
        assert result.status == ConnectorStatus.SUCCESS
        assert 'accounts' in result.data
    
    def test_get_transactions(self):
        """Test getting transactions."""
        connector = MockConnector({'api_key': 'test_key'})
        result = connector.get_transactions('account_123')
        
        assert result.status == ConnectorStatus.SUCCESS
        assert 'transactions' in result.data
    
    def test_get_balances(self):
        """Test getting balances."""
        connector = MockConnector({'api_key': 'test_key'})
        result = connector.get_balances('account_123')
        
        assert result.status == ConnectorStatus.SUCCESS
        assert 'balance' in result.data
    
    def test_refresh_token_not_implemented(self):
        """Test default refresh token behavior."""
        connector = MockConnector({'api_key': 'test_key'})
        result = connector.refresh_token()
        
        assert result.status == ConnectorStatus.ERROR
        assert "not implemented" in result.error.lower()
    
    def test_disconnect(self):
        """Test disconnect."""
        connector = MockConnector({'api_key': 'test_key'})
        result = connector.disconnect()
        
        assert result.status == ConnectorStatus.SUCCESS


class TestConnectorResponse:
    """Test ConnectorResponse model."""
    
    def test_success_response(self):
        """Test creating a success response."""
        response = ConnectorResponse(
            status=ConnectorStatus.SUCCESS,
            data={'key': 'value'}
        )
        
        assert response.status == ConnectorStatus.SUCCESS
        assert response.data == {'key': 'value'}
        assert response.error is None
    
    def test_error_response(self):
        """Test creating an error response."""
        response = ConnectorResponse(
            status=ConnectorStatus.ERROR,
            error="Something went wrong"
        )
        
        assert response.status == ConnectorStatus.ERROR
        assert response.error == "Something went wrong"
        assert response.data is None
