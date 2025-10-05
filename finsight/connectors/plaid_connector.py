"""Plaid connector for banking data."""

from typing import Dict, Optional
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from finsight.connectors.base import (
    BaseConnector,
    AuthType,
    ConnectorResponse,
    ConnectorStatus
)
from finsight.core.config import settings


class PlaidConnector(BaseConnector):
    """Connector for Plaid banking API."""
    
    def __init__(self, credentials: Dict[str, str]):
        """
        Initialize Plaid connector.
        
        Args:
            credentials: Dictionary with 'client_id', 'secret', 'access_token' (optional)
        """
        super().__init__(credentials)
        
        # Set up Plaid client
        configuration = plaid.Configuration(
            host=self._get_plaid_host(),
            api_key={
                'clientId': credentials.get('client_id', settings.plaid_client_id),
                'secret': credentials.get('secret', settings.plaid_secret),
            }
        )
        
        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)
        self.access_token = credentials.get('access_token')
    
    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "plaid"
    
    @property
    def auth_type(self) -> AuthType:
        """Return authentication type."""
        return AuthType.OAUTH2
    
    def _get_plaid_host(self) -> str:
        """Get Plaid API host based on environment."""
        env = settings.plaid_env.lower()
        if env == "production":
            return plaid.Environment.Production
        elif env == "development":
            return plaid.Environment.Development
        return plaid.Environment.Sandbox
    
    def _validate_credentials(self) -> None:
        """Validate required credentials."""
        if not self.credentials.get('client_id') and not settings.plaid_client_id:
            raise ValueError("Plaid client_id is required")
        if not self.credentials.get('secret') and not settings.plaid_secret:
            raise ValueError("Plaid secret is required")
    
    def create_link_token(self, user_id: str, redirect_uri: Optional[str] = None) -> ConnectorResponse:
        """
        Create a link token for Plaid Link initialization.
        
        Args:
            user_id: Unique user identifier
            redirect_uri: OAuth redirect URI
            
        Returns:
            ConnectorResponse with link token
        """
        try:
            request = LinkTokenCreateRequest(
                user=LinkTokenCreateRequestUser(client_user_id=user_id),
                client_name="Finsight",
                products=[Products("transactions")],
                country_codes=[CountryCode("US")],
                language="en",
            )
            
            if redirect_uri:
                request.redirect_uri = redirect_uri
            
            response = self.client.link_token_create(request)
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"link_token": response.link_token},
                metadata={"expiration": response.expiration}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def exchange_public_token(self, public_token: str) -> ConnectorResponse:
        """
        Exchange a public token for an access token.
        
        Args:
            public_token: Public token from Plaid Link
            
        Returns:
            ConnectorResponse with access token
        """
        try:
            request = ItemPublicTokenExchangeRequest(public_token=public_token)
            response = self.client.item_public_token_exchange(request)
            
            self.access_token = response.access_token
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={
                    "access_token": response.access_token,
                    "item_id": response.item_id
                }
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def authenticate(self) -> ConnectorResponse:
        """
        Authenticate with Plaid (verify access token).
        
        Returns:
            ConnectorResponse with authentication result
        """
        if not self.access_token:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error="No access token available. Use create_link_token and exchange_public_token first."
            )
        
        # Try to get accounts as authentication check
        return self.get_accounts()
    
    def get_accounts(self) -> ConnectorResponse:
        """
        Retrieve list of accounts.
        
        Returns:
            ConnectorResponse containing account data
        """
        if not self.access_token:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error="Access token required"
            )
        
        try:
            request = AccountsGetRequest(access_token=self.access_token)
            response = self.client.accounts_get(request)
            
            accounts = [
                {
                    "account_id": account.account_id,
                    "name": account.name,
                    "type": account.type,
                    "subtype": account.subtype,
                    "mask": account.mask
                }
                for account in response.accounts
            ]
            
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
        Retrieve transactions for an account.
        
        Args:
            account_id: Account identifier
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            ConnectorResponse containing transaction data
        """
        if not self.access_token:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error="Access token required"
            )
        
        if not start_date or not end_date:
            from datetime import datetime, timedelta
            end = datetime.now()
            start = end - timedelta(days=30)
            start_date = start.strftime("%Y-%m-%d")
            end_date = end.strftime("%Y-%m-%d")
        
        try:
            request = TransactionsGetRequest(
                access_token=self.access_token,
                start_date=start_date,
                end_date=end_date,
            )
            response = self.client.transactions_get(request)
            
            # Filter transactions by account_id
            transactions = [
                {
                    "transaction_id": txn.transaction_id,
                    "account_id": txn.account_id,
                    "amount": txn.amount,
                    "date": txn.date,
                    "name": txn.name,
                    "category": txn.category,
                }
                for txn in response.transactions
                if txn.account_id == account_id
            ]
            
            return ConnectorResponse(
                status=ConnectorStatus.SUCCESS,
                data={"transactions": transactions}
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
    
    def get_balances(self, account_id: str) -> ConnectorResponse:
        """
        Retrieve balance information for an account.
        
        Args:
            account_id: Account identifier
            
        Returns:
            ConnectorResponse containing balance data
        """
        if not self.access_token:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error="Access token required"
            )
        
        try:
            request = AccountsGetRequest(access_token=self.access_token)
            response = self.client.accounts_get(request)
            
            for account in response.accounts:
                if account.account_id == account_id:
                    balance_data = {
                        "account_id": account.account_id,
                        "current": account.balances.current,
                        "available": account.balances.available,
                        "limit": account.balances.limit,
                        "currency": account.balances.iso_currency_code
                    }
                    
                    return ConnectorResponse(
                        status=ConnectorStatus.SUCCESS,
                        data=balance_data
                    )
            
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=f"Account {account_id} not found"
            )
        except Exception as e:
            return ConnectorResponse(
                status=ConnectorStatus.ERROR,
                error=str(e)
            )
