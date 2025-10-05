"""Base connector interface for financial institutions."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from enum import Enum
from pydantic import BaseModel


class AuthType(str, Enum):
    """Authentication types supported by connectors."""
    
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    TOKEN = "token"
    BASIC = "basic"


class ConnectorStatus(str, Enum):
    """Status of connector operations."""
    
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"
    EXPIRED = "expired"


class ConnectorResponse(BaseModel):
    """Standard response format for connector operations."""
    
    status: ConnectorStatus
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseConnector(ABC):
    """Abstract base class for all financial institution connectors."""
    
    def __init__(self, credentials: Dict[str, str]):
        """
        Initialize the connector.
        
        Args:
            credentials: Dictionary containing authentication credentials
        """
        self.credentials = credentials
        self._validate_credentials()
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the name of the provider."""
        pass
    
    @property
    @abstractmethod
    def auth_type(self) -> AuthType:
        """Return the authentication type used by this connector."""
        pass
    
    @abstractmethod
    def _validate_credentials(self) -> None:
        """
        Validate that required credentials are present.
        
        Raises:
            ValueError: If required credentials are missing
        """
        pass
    
    @abstractmethod
    def authenticate(self) -> ConnectorResponse:
        """
        Authenticate with the provider.
        
        Returns:
            ConnectorResponse with authentication result
        """
        pass
    
    @abstractmethod
    def get_accounts(self) -> ConnectorResponse:
        """
        Retrieve list of accounts.
        
        Returns:
            ConnectorResponse containing account data
        """
        pass
    
    @abstractmethod
    def get_transactions(
        self,
        account_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> ConnectorResponse:
        """
        Retrieve transactions for an account.
        
        Args:
            account_id: Account identifier
            start_date: Start date for transaction query (ISO format)
            end_date: End date for transaction query (ISO format)
            
        Returns:
            ConnectorResponse containing transaction data
        """
        pass
    
    @abstractmethod
    def get_balances(self, account_id: str) -> ConnectorResponse:
        """
        Retrieve balance information for an account.
        
        Args:
            account_id: Account identifier
            
        Returns:
            ConnectorResponse containing balance data
        """
        pass
    
    def refresh_token(self) -> ConnectorResponse:
        """
        Refresh authentication token if applicable.
        
        Returns:
            ConnectorResponse with refresh result
        """
        return ConnectorResponse(
            status=ConnectorStatus.ERROR,
            error="Token refresh not implemented for this connector"
        )
    
    def disconnect(self) -> ConnectorResponse:
        """
        Disconnect from the provider.
        
        Returns:
            ConnectorResponse with disconnection result
        """
        return ConnectorResponse(status=ConnectorStatus.SUCCESS)
