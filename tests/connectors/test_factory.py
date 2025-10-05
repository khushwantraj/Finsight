"""Tests for connector factory."""

import pytest
from finsight.connectors.factory import ConnectorFactory
from finsight.connectors.plaid_connector import PlaidConnector
from finsight.connectors.kite_connector import KiteConnector
from finsight.connectors.alphavantage_connector import AlphaVantageConnector
from finsight.connectors.ccxt_connector import CCXTConnector


class TestConnectorFactory:
    """Test ConnectorFactory functionality."""
    
    def test_create_plaid_connector(self, mock_plaid_credentials):
        """Test creating Plaid connector."""
        connector = ConnectorFactory.create('plaid', mock_plaid_credentials)
        assert isinstance(connector, PlaidConnector)
        assert connector.provider_name == 'plaid'
    
    def test_create_kite_connector(self, mock_kite_credentials):
        """Test creating Kite connector."""
        connector = ConnectorFactory.create('kite', mock_kite_credentials)
        assert isinstance(connector, KiteConnector)
        assert connector.provider_name == 'kite'
    
    def test_create_alphavantage_connector(self, mock_alphavantage_credentials):
        """Test creating AlphaVantage connector."""
        connector = ConnectorFactory.create('alphavantage', mock_alphavantage_credentials)
        assert isinstance(connector, AlphaVantageConnector)
        assert connector.provider_name == 'alphavantage'
    
    def test_create_ccxt_connector(self, mock_ccxt_credentials):
        """Test creating CCXT connector."""
        connector = ConnectorFactory.create('ccxt', mock_ccxt_credentials)
        assert isinstance(connector, CCXTConnector)
    
    def test_create_unsupported_provider(self):
        """Test creating connector for unsupported provider."""
        with pytest.raises(ValueError, match="Unsupported provider"):
            ConnectorFactory.create('unsupported', {})
    
    def test_case_insensitive_provider(self, mock_plaid_credentials):
        """Test that provider name is case-insensitive."""
        connector1 = ConnectorFactory.create('PLAID', mock_plaid_credentials)
        connector2 = ConnectorFactory.create('Plaid', mock_plaid_credentials)
        connector3 = ConnectorFactory.create('plaid', mock_plaid_credentials)
        
        assert all(isinstance(c, PlaidConnector) for c in [connector1, connector2, connector3])
    
    def test_get_supported_providers(self):
        """Test getting list of supported providers."""
        providers = ConnectorFactory.get_supported_providers()
        
        assert 'plaid' in providers
        assert 'kite' in providers
        assert 'alphavantage' in providers
        assert 'ccxt' in providers
        assert len(providers) >= 4
    
    def test_register_custom_connector(self):
        """Test registering a custom connector."""
        from finsight.connectors.base import BaseConnector, AuthType, ConnectorStatus, ConnectorResponse
        
        class CustomConnector(BaseConnector):
            @property
            def provider_name(self):
                return "custom"
            
            @property
            def auth_type(self):
                return AuthType.API_KEY
            
            def _validate_credentials(self):
                pass
            
            def authenticate(self):
                return ConnectorResponse(status=ConnectorStatus.SUCCESS)
            
            def get_accounts(self):
                return ConnectorResponse(status=ConnectorStatus.SUCCESS)
            
            def get_transactions(self, account_id, start_date=None, end_date=None):
                return ConnectorResponse(status=ConnectorStatus.SUCCESS)
            
            def get_balances(self, account_id):
                return ConnectorResponse(status=ConnectorStatus.SUCCESS)
        
        ConnectorFactory.register('custom', CustomConnector)
        
        connector = ConnectorFactory.create('custom', {})
        assert isinstance(connector, CustomConnector)
        assert 'custom' in ConnectorFactory.get_supported_providers()
