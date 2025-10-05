"""AlphaVantage connector for stock market data."""

from typing import Dict, Optional
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.cryptocurrencies import CryptoCurrencies

from finsight.connectors.base import (
    BaseConnector,
    AuthType,
    ConnectorResponse,
    ConnectorStatus
)
from finsight.core.config import settings


class AlphaVantageConnector(BaseConnector):
    """Connector for AlphaVantage market data API."""
    
    def __init__(self, credentials: Dict[str, str]):
        """
        Initialize AlphaVantage connector.
        
        Args:
            credentials: Dictionary with 'api_key'
        """
        super().__init__(credentials)
        
        api_key = credentials.get('api_key', settings.alpha_vantage_api_key)
        self.ts = TimeSeries(key=api_key, output_format='json')
        self.fd = FundamentalData(key=api_key, output_format='json')
        self.cc = CryptoCurrencies(key=api_key, output_format='json')
    
    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "alphavantage"
    
    @property
    def auth_type(self) -> AuthType:
        """Return authentication type."""
        return AuthType.API_KEY
    
    def _validate_credentials(self) -> None:
        """Validate required credentials."""
        if not self.credentials.get('api_key') and not settings.alpha_vantage_api_key:
            raise ValueError("AlphaVantage API key is required")
    
    def authenticate(self) -> ConnectorResponse:
        """
        Authenticate with AlphaVantage (verify API key).
        
        Returns:
            ConnectorResponse with authentication result
        """
        try:
            # Try a simple API call to verify the key
            data, _ = self.ts.get_intraday('IBM', interval='1min', outputsize='compact')
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"authenticated": True}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_accounts(self) -> ConnectorResponse:
        """
        Not applicable for AlphaVantage (market data only).
        
        Returns:
            ConnectorResponse with error
        """
        return ConnectorResponse(
            status=ConnectorStatus.ERROR,
            error="AlphaVantage does not provide account data"
        )
    
    def get_transactions(
        self,
        account_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> ConnectorResponse:
        """
        Not applicable for AlphaVantage (market data only).
        
        Returns:
            ConnectorResponse with error
        """
        return ConnectorResponse(
            status=ConnectorStatus.ERROR,
            error="AlphaVantage does not provide transaction data"
        )
    
    def get_balances(self, account_id: str) -> ConnectorResponse:
        """
        Not applicable for AlphaVantage (market data only).
        
        Returns:
            ConnectorResponse with error
        """
        return ConnectorResponse(
            status=ConnectorStatus.ERROR,
            error="AlphaVantage does not provide balance data"
        )
    
    def get_quote(self, symbol: str) -> ConnectorResponse:
        """
        Get real-time quote for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            ConnectorResponse with quote data
        """
        try:
            data, _ = self.ts.get_quote_endpoint(symbol)
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"quote": data}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_intraday(self, symbol: str, interval: str = '5min') -> ConnectorResponse:
        """
        Get intraday time series data.
        
        Args:
            symbol: Stock symbol
            interval: Time interval (1min, 5min, 15min, 30min, 60min)
            
        Returns:
            ConnectorResponse with intraday data
        """
        try:
            data, meta = self.ts.get_intraday(symbol, interval=interval, outputsize='compact')
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"data": data, "metadata": meta}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_daily(self, symbol: str) -> ConnectorResponse:
        """
        Get daily time series data.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            ConnectorResponse with daily data
        """
        try:
            data, meta = self.ts.get_daily(symbol, outputsize='compact')
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"data": data, "metadata": meta}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_company_overview(self, symbol: str) -> ConnectorResponse:
        """
        Get company overview and fundamental data.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            ConnectorResponse with company data
        """
        try:
            data, _ = self.fd.get_company_overview(symbol)
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"overview": data}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_crypto_daily(self, symbol: str, market: str = 'USD') -> ConnectorResponse:
        """
        Get daily cryptocurrency data.
        
        Args:
            symbol: Cryptocurrency symbol
            market: Market currency (default: USD)
            
        Returns:
            ConnectorResponse with crypto data
        """
        try:
            data, meta = self.cc.get_digital_currency_daily(symbol, market)
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"data": data, "metadata": meta}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
