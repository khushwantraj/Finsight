"""Tests for Celery tasks."""

import pytest
from unittest.mock import Mock, patch
from finsight.workers.tasks import (
    sync_accounts,
    sync_transactions,
    sync_balances,
    periodic_sync,
    refresh_token
)
from finsight.connectors.base import ConnectorResponse, ConnectorStatus


class TestWorkerTasks:
    """Test Celery worker tasks."""
    
    @patch('finsight.workers.tasks.ConnectorFactory.create')
    def test_sync_accounts(self, mock_create, mock_plaid_credentials):
        """Test sync_accounts task."""
        mock_connector = Mock()
        mock_connector.get_accounts.return_value = ConnectorResponse(
            status=ConnectorStatus.SUCCESS,
            data={'accounts': [{'account_id': '123'}]}
        )
        mock_create.return_value = mock_connector
        
        result = sync_accounts('plaid', 'user123', mock_plaid_credentials)
        
        assert result['status'] == 'success'
        assert 'accounts' in result['data']
        mock_connector.get_accounts.assert_called_once()
    
    @patch('finsight.workers.tasks.ConnectorFactory.create')
    def test_sync_transactions(self, mock_create, mock_plaid_credentials):
        """Test sync_transactions task."""
        mock_connector = Mock()
        mock_connector.get_transactions.return_value = ConnectorResponse(
            status=ConnectorStatus.SUCCESS,
            data={'transactions': []}
        )
        mock_create.return_value = mock_connector
        
        result = sync_transactions(
            'plaid', 'user123', mock_plaid_credentials, 'account123'
        )
        
        assert result['status'] == 'success'
        assert 'transactions' in result['data']
        mock_connector.get_transactions.assert_called_once()
    
    @patch('finsight.workers.tasks.ConnectorFactory.create')
    def test_sync_balances(self, mock_create, mock_plaid_credentials):
        """Test sync_balances task."""
        mock_connector = Mock()
        mock_connector.get_balances.return_value = ConnectorResponse(
            status=ConnectorStatus.SUCCESS,
            data={'balance': 1000}
        )
        mock_create.return_value = mock_connector
        
        result = sync_balances(
            'plaid', 'user123', mock_plaid_credentials, 'account123'
        )
        
        assert result['status'] == 'success'
        assert 'balance' in result['data']
        mock_connector.get_balances.assert_called_once()
    
    @patch('finsight.workers.tasks.sync_accounts')
    def test_periodic_sync(self, mock_sync_accounts, mock_plaid_credentials):
        """Test periodic_sync task."""
        mock_sync_accounts.return_value = {
            'status': 'success',
            'data': {
                'accounts': [
                    {'account_id': 'acc1'},
                    {'account_id': 'acc2'}
                ]
            }
        }
        
        result = periodic_sync('plaid', 'user123', mock_plaid_credentials)
        
        assert result['accounts'] is not None
        assert isinstance(result['transactions'], list)
        assert isinstance(result['balances'], list)
    
    @patch('finsight.workers.tasks.ConnectorFactory.create')
    def test_refresh_token(self, mock_create, mock_plaid_credentials):
        """Test refresh_token task."""
        mock_connector = Mock()
        mock_connector.refresh_token.return_value = ConnectorResponse(
            status=ConnectorStatus.SUCCESS,
            data={'token': 'new_token'}
        )
        mock_create.return_value = mock_connector
        
        result = refresh_token('plaid', 'user123', mock_plaid_credentials)
        
        assert result['status'] == 'success'
        mock_connector.refresh_token.assert_called_once()
    
    @patch('finsight.workers.tasks.ConnectorFactory.create')
    def test_sync_accounts_error(self, mock_create, mock_plaid_credentials):
        """Test sync_accounts task with error."""
        mock_create.side_effect = Exception("Connection error")
        
        result = sync_accounts('plaid', 'user123', mock_plaid_credentials)
        
        assert result['status'] == 'error'
        assert 'error' in result
