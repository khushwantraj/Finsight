from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Transaction(BaseModel):
    id: int = Field(..., serialization_alias="id")
    transaction_date: datetime = Field(..., serialization_alias="transactionDate")
    description: str = Field(..., serialization_alias="description")
    amount: float = Field(..., serialization_alias="amount")
    category: str = Field(..., serialization_alias="category")
    account_type: str = Field(..., serialization_alias="accountType")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "transaction_date": "2024-01-15T10:30:00",
                "description": "Grocery Store",
                "amount": -85.50,
                "category": "Food",
                "account_type": "Checking"
            }
        }
