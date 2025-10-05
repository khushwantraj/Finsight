"""Factory for creating connector instances."""

from typing import Dict, Type
from finsight.connectors.base import BaseConnector
from finsight.connectors.plaid_connector import PlaidConnector
from finsight.connectors.kite_connector import KiteConnector
from finsight.connectors.alphavantage_connector import AlphaVantageConnector
from finsight.connectors.ccxt_connector import CCXTConnector


class ConnectorFactory:
    """Factory for creating financial institution connectors."""
    
    _connectors: Dict[str, Type[BaseConnector]] = {
        'plaid': PlaidConnector,
        'kite': KiteConnector,
        'alphavantage': AlphaVantageConnector,
        'ccxt': CCXTConnector,
    }
    
    @classmethod
    def create(cls, provider: str, credentials: Dict[str, str]) -> BaseConnector:
        """
        Create a connector instance for the specified provider.
        
        Args:
            provider: Provider name ('plaid', 'kite', 'alphavantage', 'ccxt')
            credentials: Provider-specific credentials
            
        Returns:
            Connector instance
            
        Raises:
            ValueError: If provider is not supported
        """
        provider_lower = provider.lower()
        
        if provider_lower not in cls._connectors:
            raise ValueError(
                f"Unsupported provider: {provider}. "
                f"Supported providers: {', '.join(cls._connectors.keys())}"
            )
        
        connector_class = cls._connectors[provider_lower]
        return connector_class(credentials)
    
    @classmethod
    def register(cls, provider: str, connector_class: Type[BaseConnector]) -> None:
        """
        Register a new connector class.
        
        Args:
            provider: Provider name
            connector_class: Connector class to register
        """
        cls._connectors[provider.lower()] = connector_class
    
    @classmethod
    def get_supported_providers(cls) -> list[str]:
        """
        Get list of supported providers.
        
        Returns:
            List of provider names
        """
        return list(cls._connectors.keys())
