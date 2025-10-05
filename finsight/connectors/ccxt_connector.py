"""CCXT connector for cryptocurrency exchanges."""

from typing import Dict, Optional, List
import ccxt

from finsight.connectors.base import (
    BaseConnector,
    AuthType,
    ConnectorResponse,
    ConnectorStatus
)
from finsight.core.config import settings


class CCXTConnector(BaseConnector):
    """Connector for cryptocurrency exchanges via CCXT."""
    
    def __init__(self, credentials: Dict[str, str]):
        """
        Initialize CCXT connector.
        
        Args:
            credentials: Dictionary with 'exchange', 'api_key', 'api_secret'
        """
        super().__init__(credentials)
        
        exchange_id = credentials.get('exchange', settings.ccxt_exchange)
        api_key = credentials.get('api_key', settings.ccxt_api_key)
        api_secret = credentials.get('api_secret', settings.ccxt_api_secret)
        
        # Dynamically create exchange instance
        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })
    
    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return f"ccxt_{self.exchange.id}"
    
    @property
    def auth_type(self) -> AuthType:
        """Return authentication type."""
        return AuthType.API_KEY
    
    def _validate_credentials(self) -> None:
        """Validate required credentials."""
        exchange_id = self.credentials.get('exchange', settings.ccxt_exchange)
        if not exchange_id:
            raise ValueError("Exchange ID is required")
        if exchange_id not in ccxt.exchanges:
            raise ValueError(f"Unsupported exchange: {exchange_id}")
    
    def authenticate(self) -> ConnectorResponse:
        """
        Authenticate with the exchange (verify API key).
        
        Returns:
            ConnectorResponse with authentication result
        """
        try:
            # Try to fetch balance to verify credentials
            balance = self.exchange.fetch_balance()
            
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
        Retrieve exchange account information.
        
        Returns:
            ConnectorResponse containing account data
        """
        try:
            balance = self.exchange.fetch_balance()
            
            # Get non-zero balances
            accounts = []
            for currency, amount in balance['total'].items():
                if amount and amount > 0:
                    accounts.append({
                        "currency": currency,
                        "total": amount,
                        "free": balance['free'].get(currency, 0),
                        "used": balance['used'].get(currency, 0)
                    })
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"accounts": accounts}
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
        Retrieve transactions (trades) for a symbol.
        
        Args:
            account_id: Symbol/pair to get trades for (e.g., 'BTC/USD')
            start_date: Start timestamp in milliseconds
            end_date: End timestamp in milliseconds
            
        Returns:
            ConnectorResponse containing transaction data
        """
        try:
            since = int(start_date) if start_date else None
            trades = self.exchange.fetch_my_trades(account_id, since=since)
            
            # Filter by end_date if provided
            if end_date:
                end_ts = int(end_date)
                trades = [t for t in trades if t['timestamp'] <= end_ts]
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"trades": trades}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_balances(self, account_id: str) -> ConnectorResponse:
        """
        Retrieve balance for a specific currency.
        
        Args:
            account_id: Currency symbol (e.g., 'BTC', 'USD')
            
        Returns:
            ConnectorResponse containing balance data
        """
        try:
            balance = self.exchange.fetch_balance()
            
            if account_id in balance['total']:
                balance_data = {
                    "currency": account_id,
                    "total": balance['total'][account_id],
                    "free": balance['free'].get(account_id, 0),
                    "used": balance['used'].get(account_id, 0)
                }
                
                return ConnectorResponse(
                    status=ConnectorStatus.SUCCESS,
                    data=balance_data
                )
            else:
                return ConnectorResponse(
                    status=ConnectorStatus.ERROR,
                    error=f"Currency {account_id} not found"
                )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_ticker(self, symbol: str) -> ConnectorResponse:
        """
        Get ticker information for a symbol.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTC/USD')
            
        Returns:
            ConnectorResponse with ticker data
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"ticker": ticker}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_order_book(self, symbol: str, limit: int = 20) -> ConnectorResponse:
        """
        Get order book for a symbol.
        
        Args:
            symbol: Trading pair symbol
            limit: Number of orders to retrieve
            
        Returns:
            ConnectorResponse with order book data
        """
        try:
            order_book = self.exchange.fetch_order_book(symbol, limit=limit)
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"order_book": order_book}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_open_orders(self, symbol: Optional[str] = None) -> ConnectorResponse:
        """
        Get open orders.
        
        Args:
            symbol: Trading pair symbol (optional)
            
        Returns:
            ConnectorResponse with open orders
        """
        try:
            orders = self.exchange.fetch_open_orders(symbol)
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"orders": orders}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    @staticmethod
    def get_supported_exchanges() -> List[str]:
        """
        Get list of supported exchanges.
        
        Returns:
            List of exchange IDs
        """
        return ccxt.exchanges
