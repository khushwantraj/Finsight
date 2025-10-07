from typing import List
from fastapi import APIRouter, Query
from app.models import Transaction
from app.sample_data import sample_transactions

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("", response_model=List[Transaction])
async def get_transactions(
    limit: int = Query(default=10, ge=1, le=100, description="Number of transactions to return"),
    offset: int = Query(default=0, ge=0, description="Number of transactions to skip")
):
    """
    Get list of transactions with pagination support.
    Returns data in camelCase format for frontend consumption.
    """
    return sample_transactions[offset:offset + limit]


@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int):
    """
    Get a specific transaction by ID.
    Returns data in camelCase format for frontend consumption.
    """
    for transaction in sample_transactions:
        if transaction.id == transaction_id:
            return transaction
    return None
