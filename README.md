# Finsight

A full-stack financial insights dashboard application that helps you track income, expenses, and transactions.

## Features

- **Dashboard**: View key financial metrics including total income, expenses, net savings, and account balance
- **Transaction List**: Browse through your financial transactions with detailed information
- **API Backend**: RESTful API built with FastAPI that returns camelCase JSON responses
- **Responsive Frontend**: React TypeScript application with modern UI

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation with camelCase serialization aliases
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **CSS3**: Modern styling

## Getting Started

### Prerequisites
- Docker and Docker Compose installed on your system

### Running with Docker Compose

1. Clone the repository:
```bash
git clone https://github.com/khushwantraj/Finsight.git
cd Finsight
```

2. Start the application:
```bash
docker-compose up --build
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Running Locally

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Dashboard
- `GET /api/dashboard` - Get dashboard statistics

### Transactions
- `GET /api/transactions` - Get list of transactions (supports pagination with `limit` and `offset` query parameters)
- `GET /api/transactions/{transaction_id}` - Get specific transaction by ID

## Data Model

The backend uses Python snake_case internally but returns camelCase JSON responses for frontend consumption:

### Dashboard Stats
```json
{
  "totalIncome": 5800.00,
  "totalExpenses": 606.00,
  "netSavings": 5194.00,
  "accountBalance": 12500.00
}
```

### Transaction
```json
{
  "id": 1,
  "transactionDate": "2024-01-15T10:30:00",
  "description": "Salary Deposit",
  "amount": 5000.00,
  "category": "Income",
  "accountType": "Checking"
}
```

## Project Structure

```
Finsight/
├── backend/
│   ├── app/
│   │   ├── models/          # Pydantic models with camelCase aliases
│   │   ├── routers/         # API route handlers
│   │   ├── main.py          # FastAPI application
│   │   └── sample_data.py   # Sample data
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API client
│   │   ├── types.ts         # TypeScript types
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## License

MIT