# Data Model Consistency Solution

This document explains how the Finsight application solves the snake_case vs camelCase inconsistency between backend and frontend.

## Problem

- **Backend (Python)**: Uses snake_case convention (e.g., `total_income`, `transaction_date`)
- **Frontend (TypeScript/JavaScript)**: Expects camelCase convention (e.g., `totalIncome`, `transactionDate`)

## Solution

### Backend - Pydantic Serialization Aliases

We use Pydantic v2's `serialization_alias` feature to automatically convert field names when serializing to JSON:

```python
from pydantic import BaseModel, Field

class DashboardStats(BaseModel):
    total_income: float = Field(..., serialization_alias="totalIncome")
    total_expenses: float = Field(..., serialization_alias="totalExpenses")
    net_savings: float = Field(..., serialization_alias="netSavings")
    account_balance: float = Field(..., serialization_alias="accountBalance")
```

**Key Points:**
- Python code uses snake_case internally: `stats.total_income`
- JSON responses use camelCase automatically: `{"totalIncome": 5800.0}`
- No manual conversion needed in API endpoints
- Type-safe on both ends

### Example Transaction Model

```python
class Transaction(BaseModel):
    id: int = Field(..., serialization_alias="id")
    transaction_date: datetime = Field(..., serialization_alias="transactionDate")
    description: str = Field(..., serialization_alias="description")
    amount: float = Field(..., serialization_alias="amount")
    category: str = Field(..., serialization_alias="category")
    account_type: str = Field(..., serialization_alias="accountType")
```

### Frontend TypeScript Types

Frontend types match the camelCase format:

```typescript
export interface DashboardStats {
  totalIncome: number;
  totalExpenses: number;
  netSavings: number;
  accountBalance: number;
}

export interface Transaction {
  id: number;
  transactionDate: string;
  description: string;
  amount: number;
  category: string;
  accountType: string;
}
```

## Benefits

1. **No Runtime Conversion**: Automatic conversion at serialization time
2. **Type Safety**: Both Python and TypeScript maintain their conventions
3. **Clean Code**: Python code follows PEP 8, JavaScript follows standard conventions
4. **Maintainable**: Changes to field names are centralized in the model definitions
5. **Performance**: No overhead from runtime field name mapping

## Testing

You can verify the camelCase conversion by calling the API:

```bash
# Dashboard endpoint
curl http://localhost:8000/api/dashboard

# Response (camelCase):
{
  "totalIncome": 5800.0,
  "totalExpenses": 606.0,
  "netSavings": 5194.0,
  "accountBalance": 12500.0
}

# Transactions endpoint
curl http://localhost:8000/api/transactions?limit=1

# Response (camelCase):
[
  {
    "id": 1,
    "transactionDate": "2024-01-15T10:30:00",
    "description": "Salary Deposit",
    "amount": 5000.0,
    "category": "Income",
    "accountType": "Checking"
  }
]
```

## Sample Data

Sample data is defined using Python's snake_case convention:

```python
Transaction(
    id=1,
    transaction_date=datetime(2024, 1, 15, 10, 30, 0),
    description="Salary Deposit",
    amount=5000.00,
    category="Income",
    account_type="Checking"
)
```

When serialized to JSON, it automatically becomes camelCase for frontend consumption.
