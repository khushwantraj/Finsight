# Developer Quick Reference

## Running the Application

### Using Docker Compose (Recommended)
```bash
# Start all services
docker compose up --build

# Start in background
docker compose up -d --build

# Stop services
docker compose down

# View logs
docker compose logs -f

# Rebuild a specific service
docker compose build backend
docker compose build frontend
```

### Running Backend Locally
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Frontend Locally
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Base URL
- Local: `http://localhost:8000`
- Docker: `http://localhost:8000`

### Available Endpoints

#### Health Check
```bash
GET /health
# Response: {"status": "healthy"}
```

#### Root
```bash
GET /
# Response: {"message": "Welcome to Finsight API"}
```

#### Dashboard Statistics
```bash
GET /api/dashboard
# Response (camelCase):
{
  "totalIncome": 5800.0,
  "totalExpenses": 606.0,
  "netSavings": 5194.0,
  "accountBalance": 12500.0
}
```

#### List Transactions
```bash
GET /api/transactions?limit=10&offset=0
# Query Parameters:
# - limit: number of transactions (1-100, default 10)
# - offset: skip N transactions (default 0)

# Response (camelCase array):
[
  {
    "id": 1,
    "transactionDate": "2024-01-15T10:30:00",
    "description": "Salary Deposit",
    "amount": 5000.0,
    "category": "Income",
    "accountType": "Checking"
  },
  ...
]
```

#### Get Single Transaction
```bash
GET /api/transactions/{id}
# Example: GET /api/transactions/1

# Response (camelCase):
{
  "id": 1,
  "transactionDate": "2024-01-15T10:30:00",
  "description": "Salary Deposit",
  "amount": 5000.0,
  "category": "Income",
  "accountType": "Checking"
}
```

## Testing the API

### Using curl
```bash
# Test health
curl http://localhost:8000/health

# Get dashboard stats
curl http://localhost:8000/api/dashboard

# Get transactions (pretty print)
curl http://localhost:8000/api/transactions?limit=5 | python3 -m json.tool

# Get specific transaction
curl http://localhost:8000/api/transactions/1
```

### Using Interactive API Documentation
Visit `http://localhost:8000/docs` for Swagger UI with interactive API testing.

## Frontend Development

### API Service Location
`frontend/src/services/api.ts` - Contains all API client methods

### TypeScript Types
`frontend/src/types.ts` - Matches backend camelCase responses

### Components
- `Dashboard.tsx` - Displays financial statistics
- `TransactionList.tsx` - Shows transaction table

### Styling
- `App.css` - Main application styles
- `index.css` - Global styles

## Adding New Features

### Adding a New API Endpoint

1. **Create/Update Model** (`backend/app/models/`)
```python
from pydantic import BaseModel, Field

class NewModel(BaseModel):
    field_name: str = Field(..., serialization_alias="fieldName")
```

2. **Create Router** (`backend/app/routers/`)
```python
from fastapi import APIRouter
from app.models import NewModel

router = APIRouter(prefix="/api/new", tags=["new"])

@router.get("", response_model=NewModel)
async def get_new():
    return NewModel(field_name="value")
```

3. **Register Router** (`backend/app/main.py`)
```python
from app.routers import new_router
app.include_router(new_router)
```

### Adding a New Frontend Component

1. **Create Type** (`frontend/src/types.ts`)
```typescript
export interface NewType {
  fieldName: string; // camelCase to match API
}
```

2. **Create Component** (`frontend/src/components/NewComponent.tsx`)
```typescript
import React from 'react';
import { NewType } from '../types';

export const NewComponent: React.FC = () => {
  // Component logic
};
```

## Important Notes

### Data Naming Convention
- **Backend Python Code**: Use `snake_case`
- **API JSON Responses**: Automatically converted to `camelCase`
- **Frontend TypeScript**: Use `camelCase`

Example:
```python
# Python model
class Transaction(BaseModel):
    transaction_date: datetime = Field(..., serialization_alias="transactionDate")

# Creates JSON
{"transactionDate": "2024-01-15T10:30:00"}

# TypeScript type
interface Transaction {
  transactionDate: string;
}
```

### CORS Configuration
Backend allows requests from:
- `http://localhost:3000`
- `http://frontend:3000`

Update `backend/app/main.py` to add more origins if needed.

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# or
netstat -tulpn | grep 8000

# Kill the process
kill -9 <PID>
```

### Docker Build Issues
```bash
# Clean up Docker
docker compose down
docker system prune -a

# Rebuild from scratch
docker compose build --no-cache
```

### Backend Issues
```bash
# Check backend logs
docker compose logs backend

# Access backend container
docker compose exec backend bash
```

### Frontend Issues
```bash
# Check frontend logs
docker compose logs frontend

# Access frontend container
docker compose exec frontend sh
```

## Environment Variables

### Backend
- `PYTHONUNBUFFERED=1` - Ensures logs appear immediately

### Frontend
- `REACT_APP_API_URL` - Backend API URL (default: `http://localhost:8000`)

To override, create `.env.local` in frontend directory:
```
REACT_APP_API_URL=http://your-api-url:8000
```
