"""Webhook handlers for real-time updates from financial providers."""

from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
import hmac
import hashlib
from finsight.core.config import settings
from finsight.workers.tasks import sync_accounts, sync_transactions

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verify webhook signature.
    
    Args:
        payload: Raw request payload
        signature: Signature from request header
        secret: Webhook secret
        
    Returns:
        True if signature is valid
    """
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)


@router.post("/plaid")
async def plaid_webhook(
    request: Request,
    plaid_verification: Optional[str] = Header(None)
):
    """
    Handle Plaid webhook events.
    
    Args:
        request: FastAPI request object
        plaid_verification: Plaid verification header
        
    Returns:
        Success response
    """
    body = await request.body()
    data = await request.json()
    
    webhook_type = data.get('webhook_type')
    webhook_code = data.get('webhook_code')
    item_id = data.get('item_id')
    
    # Handle different webhook types
    if webhook_type == 'TRANSACTIONS':
        if webhook_code == 'DEFAULT_UPDATE':
            # New transactions available
            # Trigger sync task
            sync_transactions.delay(
                provider='plaid',
                user_id=item_id,
                credentials={},  # Retrieve from storage
                account_id=''
            )
    
    elif webhook_type == 'ITEM':
        if webhook_code == 'ERROR':
            # Item error - may need re-authentication
            pass
        elif webhook_code == 'PENDING_EXPIRATION':
            # Access will expire soon
            pass
    
    return {"status": "received"}


@router.post("/kite")
async def kite_webhook(
    request: Request,
    x_signature: Optional[str] = Header(None)
):
    """
    Handle Kite Connect webhook events (postbacks).
    
    Args:
        request: FastAPI request object
        x_signature: Signature header
        
    Returns:
        Success response
    """
    body = await request.body()
    
    # Verify signature if provided
    if x_signature and settings.webhook_secret:
        if not verify_webhook_signature(body, x_signature, settings.webhook_secret):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    data = await request.json()
    
    # Process Kite postback data
    # Kite sends order updates, position updates, etc.
    
    return {"status": "received"}


@router.post("/ccxt/{exchange}")
async def ccxt_webhook(
    exchange: str,
    request: Request,
    x_signature: Optional[str] = Header(None)
):
    """
    Handle webhook events from cryptocurrency exchanges.
    
    Args:
        exchange: Exchange name
        request: FastAPI request object
        x_signature: Signature header
        
    Returns:
        Success response
    """
    body = await request.body()
    
    # Verify signature if provided
    if x_signature and settings.webhook_secret:
        if not verify_webhook_signature(body, x_signature, settings.webhook_secret):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    data = await request.json()
    
    # Process exchange-specific webhook data
    # Different exchanges have different webhook formats
    
    return {"status": "received"}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
