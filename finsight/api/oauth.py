"""OAuth callback handlers for financial providers."""

from fastapi import APIRouter, HTTPException, Query
from finsight.connectors.factory import ConnectorFactory
from finsight.core.credentials import TokenStore

router = APIRouter(prefix="/oauth", tags=["oauth"])

# Initialize token store
token_store = TokenStore()


@router.get("/plaid/callback")
async def plaid_callback(
    public_token: str = Query(...),
    user_id: str = Query(...)
):
    """
    Handle Plaid OAuth callback.
    
    Args:
        public_token: Public token from Plaid Link
        user_id: User identifier
        
    Returns:
        Success response with access token
    """
    try:
        credentials = {'public_token': public_token}
        connector = ConnectorFactory.create('plaid', credentials)
        
        # Exchange public token for access token
        result = connector.exchange_public_token(public_token)
        
        if result.status.value == 'success':
            access_token = result.data.get('access_token')
            
            # Store access token securely
            token_store.store_token('plaid', user_id, access_token)
            
            return {
                'status': 'success',
                'message': 'Plaid account linked successfully'
            }
        else:
            raise HTTPException(status_code=400, detail=result.error)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kite/callback")
async def kite_callback(
    request_token: str = Query(...),
    user_id: str = Query(...),
    api_key: str = Query(...),
    api_secret: str = Query(...)
):
    """
    Handle Kite Connect OAuth callback.
    
    Args:
        request_token: Request token from Kite
        user_id: User identifier
        api_key: Kite API key
        api_secret: Kite API secret
        
    Returns:
        Success response with access token
    """
    try:
        credentials = {
            'api_key': api_key,
            'api_secret': api_secret
        }
        connector = ConnectorFactory.create('kite', credentials)
        
        # Generate session and get access token
        result = connector.generate_session(request_token)
        
        if result.status.value == 'success':
            access_token = result.data.get('access_token')
            
            # Store access token securely
            token_store.store_token('kite', user_id, access_token)
            
            return {
                'status': 'success',
                'message': 'Kite account linked successfully',
                'user_info': result.data
            }
        else:
            raise HTTPException(status_code=400, detail=result.error)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/redirect")
async def generic_oauth_redirect(
    code: str = Query(None),
    state: str = Query(None),
    error: str = Query(None)
):
    """
    Generic OAuth redirect handler.
    
    Args:
        code: Authorization code
        state: State parameter for CSRF protection
        error: Error message if OAuth failed
        
    Returns:
        Success or error response
    """
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code missing")
    
    # Process the authorization code
    # State should be validated against stored state
    
    return {
        'status': 'success',
        'message': 'OAuth flow completed',
        'code': code
    }
