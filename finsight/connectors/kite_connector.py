"""Kite Connect connector for Indian stock market data."""

from typing import Dict, Optional
from kiteconnect import KiteConnect

from finsight.connectors.base import (
    BaseConnector,
    AuthType,
    ConnectorResponse,
    ConnectorStatus
)
from finsight.core.config import settings


class KiteConnector(BaseConnector):
    """Connector for Kite Connect API."""
    
    def __init__(self, credentials: Dict[str, str]):
        """
        Initialize Kite connector.
        
        Args:
            credentials: Dictionary with 'api_key', 'api_secret', 'access_token' (optional)
        """
        super().__init__(credentials)
        
        api_key = credentials.get('api_key', settings.kite_api_key)
        self.api_secret = credentials.get('api_secret', settings.kite_api_secret)
        self.kite = KiteConnect(api_key=api_key)
        
        access_token = credentials.get('access_token')
        if access_token:
            self.kite.set_access_token(access_token)
    
    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "kite"
    
    @property
    def auth_type(self) -> AuthType:
        """Return authentication type."""
        return AuthType.TOKEN
    
    def _validate_credentials(self) -> None:
        """Validate required credentials."""
        if not self.credentials.get('api_key') and not settings.kite_api_key:
            raise ValueError("Kite API key is required")
        if not self.credentials.get('api_secret') and not settings.kite_api_secret:
            raise ValueError("Kite API secret is required")
    
    def get_login_url(self) -> str:
        """
        Get the login URL for Kite Connect OAuth flow.
        
        Returns:
            Login URL string
        """
        return self.kite.login_url()
    
    def generate_session(self, request_token: str) -> ConnectorResponse:
        """
        Generate session and access token from request token.
        
        Args:
            request_token: Request token from OAuth callback
            
        Returns:
            ConnectorResponse with access token
        """
        try:
            data = self.kite.generate_session(request_token, api_secret=self.api_secret)
            self.kite.set_access_token(data["access_token"])
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={
                    "access_token": data["access_token"],
                    "user_id": data.get("user_id"),
                    "user_type": data.get("user_type")
                }
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def authenticate(self) -> ConnectorResponse:
        """
        Authenticate with Kite (verify access token).
        
        Returns:
            ConnectorResponse with authentication result
        """
        try:
            profile = self.kite.profile()
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"profile": profile}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_accounts(self) -> ConnectorResponse:
        """
        Retrieve account/profile information.
        
        Returns:
            ConnectorResponse containing account data
        """
        try:
            profile = self.kite.profile()
            margins = self.kite.margins()
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={
                    "profile": profile,
                    "margins": margins
                }
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_transactions(
        self,
        account_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> ConnectorResponse:
        """
        Retrieve orders (transactions) for the account.
        
        Args:
            account_id: Account identifier (not used for Kite)
            start_date: Start date (not supported by Kite for orders)
            end_date: End date (not supported by Kite for orders)
            
        Returns:
            ConnectorResponse containing transaction data
        """
        try:
            orders = self.kite.orders()
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"orders": orders}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_balances(self, account_id: str) -> ConnectorResponse:
        """
        Retrieve balance information.
        
        Args:
            account_id: Account identifier (not used for Kite)
            
        Returns:
            ConnectorResponse containing balance data
        """
        try:
            margins = self.kite.margins()
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"margins": margins}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_positions(self) -> ConnectorResponse:
        """
        Get current positions.
        
        Returns:
            ConnectorResponse with positions data
        """
        try:
            positions = self.kite.positions()
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"positions": positions}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_holdings(self) -> ConnectorResponse:
        """
        Get holdings.
        
        Returns:
            ConnectorResponse with holdings data
        """
        try:
            holdings = self.kite.holdings()
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"holdings": holdings}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
