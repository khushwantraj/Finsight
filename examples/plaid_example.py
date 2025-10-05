"""Example usage of Plaid connector."""

import os
from dotenv import load_dotenv
from finsight.connectors.factory import ConnectorFactory

# Load environment variables
load_dotenv()


def main():
    """Demonstrate Plaid connector usage."""
    
    # Create Plaid connector
    credentials = {
        'client_id': os.getenv('PLAID_CLIENT_ID'),
        'secret': os.getenv('PLAID_SECRET')
    }
    
    plaid = ConnectorFactory.create('plaid', credentials)
    
    # Step 1: Create link token for user
    print("Creating link token...")
    result = plaid.create_link_token(user_id='user123', redirect_uri='http://localhost:8000/oauth/plaid/callback')
    
    if result.status.value == 'success':
        link_token = result.data['link_token']
        print(f"Link token created: {link_token[:20]}...")
        print(f"Expiration: {result.metadata.get('expiration')}")
        
        # In a real application, you would:
        # 1. Send link_token to frontend
        # 2. Initialize Plaid Link with the token
        # 3. User completes authentication
        # 4. Receive public_token in callback
        
        # For demonstration, assuming we have a public_token
        # public_token = "public-sandbox-xxx"
        
        # Step 2: Exchange public token for access token
        # result = plaid.exchange_public_token(public_token)
        # if result.status.value == 'success':
        #     access_token = result.data['access_token']
        #     print(f"Access token: {access_token[:20]}...")
        #     
        #     # Step 3: Use access token to get data
        #     credentials['access_token'] = access_token
        #     plaid = ConnectorFactory.create('plaid', credentials)
        #     
        #     # Get accounts
        #     accounts = plaid.get_accounts()
        #     print(f"\nAccounts: {accounts.data}")
        #     
        #     # Get transactions
        #     if accounts.data and accounts.data.get('accounts'):
        #         account_id = accounts.data['accounts'][0]['account_id']
        #         transactions = plaid.get_transactions(account_id)
        #         print(f"\nTransactions: {transactions.data}")
    else:
        print(f"Error: {result.error}")


if __name__ == '__main__':
    main()
