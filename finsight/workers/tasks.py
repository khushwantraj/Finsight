"""Data ingestion tasks for financial connectors."""

from typing import Dict, Optional
from celery import Task
from finsight.workers.celery_app import celery_app
from finsight.connectors.factory import ConnectorFactory
from finsight.core.credentials import TokenStore


class ConnectorTask(Task):
    """Base task class for connector operations."""
    
    _token_store = None
    
    @property
    def token_store(self) -> TokenStore:
        if self._token_store is None:
            self._token_store = TokenStore()
        return self._token_store


@celery_app.task(base=ConnectorTask, name='finsight.sync_accounts')
def sync_accounts(provider: str, user_id: str, credentials: Dict[str, str]) -> Dict:
    """
    Sync accounts from a financial provider.
    
    Args:
        provider: Provider name
        user_id: User identifier
        credentials: Provider credentials
        
    Returns:
        Dictionary with sync results
    """
    try:
        connector = ConnectorFactory.create(provider, credentials)
        result = connector.get_accounts()
        
        return {
            'status': result.status.value,
            'data': result.data,
            'error': result.error
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


@celery_app.task(base=ConnectorTask, name='finsight.sync_transactions')
def sync_transactions(
    provider: str,
    user_id: str,
    credentials: Dict[str, str],
    account_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict:
    """
    Sync transactions from a financial provider.
    
    Args:
        provider: Provider name
        user_id: User identifier
        credentials: Provider credentials
        account_id: Account identifier
        start_date: Start date for transactions
        end_date: End date for transactions
        
    Returns:
        Dictionary with sync results
    """
    try:
        connector = ConnectorFactory.create(provider, credentials)
        result = connector.get_transactions(account_id, start_date, end_date)
        
        return {
            'status': result.status.value,
            'data': result.data,
            'error': result.error
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


@celery_app.task(base=ConnectorTask, name='finsight.sync_balances')
def sync_balances(
    provider: str,
    user_id: str,
    credentials: Dict[str, str],
    account_id: str
) -> Dict:
    """
    Sync balances from a financial provider.
    
    Args:
        provider: Provider name
        user_id: User identifier
        credentials: Provider credentials
        account_id: Account identifier
        
    Returns:
        Dictionary with sync results
    """
    try:
        connector = ConnectorFactory.create(provider, credentials)
        result = connector.get_balances(account_id)
        
        return {
            'status': result.status.value,
            'data': result.data,
            'error': result.error
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


@celery_app.task(name='finsight.periodic_sync')
def periodic_sync(provider: str, user_id: str, credentials: Dict[str, str]) -> Dict:
    """
    Periodic sync task for all account data.
    
    Args:
        provider: Provider name
        user_id: User identifier
        credentials: Provider credentials
        
    Returns:
        Dictionary with sync results
    """
    results = {
        'accounts': None,
        'transactions': [],
        'balances': []
    }
    
    try:
        # Sync accounts
        accounts_result = sync_accounts(provider, user_id, credentials)
        results['accounts'] = accounts_result
        
        # If accounts sync succeeded, sync transactions and balances for each account
        if accounts_result['status'] == 'success' and accounts_result['data']:
            accounts = accounts_result['data'].get('accounts', [])
            
            for account in accounts:
                account_id = account.get('account_id') or account.get('currency')
                
                if account_id:
                    # Sync transactions
                    txn_result = sync_transactions(provider, user_id, credentials, account_id)
                    results['transactions'].append({
                        'account_id': account_id,
                        'result': txn_result
                    })
                    
                    # Sync balances
                    bal_result = sync_balances(provider, user_id, credentials, account_id)
                    results['balances'].append({
                        'account_id': account_id,
                        'result': bal_result
                    })
        
        return results
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


@celery_app.task(name='finsight.refresh_token')
def refresh_token(provider: str, user_id: str, credentials: Dict[str, str]) -> Dict:
    """
    Refresh authentication token for a provider.
    
    Args:
        provider: Provider name
        user_id: User identifier
        credentials: Provider credentials
        
    Returns:
        Dictionary with refresh results
    """
    try:
        connector = ConnectorFactory.create(provider, credentials)
        result = connector.refresh_token()
        
        return {
            'status': result.status.value,
            'data': result.data,
            'error': result.error
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }
