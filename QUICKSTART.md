# Quick Start Guide

This guide will help you get Finsight up and running quickly.

## Prerequisites

- Python 3.9 or higher
- Redis (for Celery)
- PostgreSQL (optional, can use SQLite for development)

## Installation

### 1. Clone and Setup

```bash
git clone https://github.com/khushwantraj/Finsight.git
cd Finsight
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API credentials
```

### 3. Generate Encryption Key

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Add the generated key to `.env` as `ENCRYPTION_KEY`.

## Running the Application

### Start Redis (if not already running)

```bash
# macOS
brew services start redis

# Linux
sudo systemctl start redis

# Docker
docker run -d -p 6379:6379 redis:7-alpine
```

### Start the API Server

```bash
uvicorn finsight.api.app:app --reload
```

The API will be available at http://localhost:8000

### Start Celery Worker

In a new terminal:

```bash
celery -A finsight.workers.celery_app worker --loglevel=info
```

## Quick Examples

### Using Plaid Connector

```python
from finsight.connectors.factory import ConnectorFactory

credentials = {
    'client_id': 'your_client_id',
    'secret': 'your_secret'
}

plaid = ConnectorFactory.create('plaid', credentials)
result = plaid.create_link_token(user_id='user123')
print(result.data)
```

### Using AlphaVantage Connector

```python
from finsight.connectors.factory import ConnectorFactory

credentials = {'api_key': 'your_api_key'}
av = ConnectorFactory.create('alphavantage', credentials)

# Get stock quote
quote = av.get_quote('AAPL')
print(quote.data)
```

### Scheduling Background Tasks

```python
from finsight.workers.tasks import sync_accounts

# Queue a task
result = sync_accounts.delay('plaid', 'user123', credentials)
print(f"Task ID: {result.id}")
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=finsight
```

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [examples/](examples/) for more code examples
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Getting API Keys

### Plaid
1. Sign up at https://plaid.com
2. Create a new application
3. Get your client_id and secret

### Kite Connect
1. Sign up at https://kite.trade
2. Subscribe to Kite Connect
3. Get your API key and secret

### AlphaVantage
1. Sign up at https://www.alphavantage.co
2. Get your free API key

### CCXT (Crypto Exchanges)
1. Create an account on your chosen exchange
2. Generate API keys in account settings
3. Enable required permissions

## Troubleshooting

### Redis connection error
- Ensure Redis is running: `redis-cli ping`
- Check REDIS_URL in .env

### Module import errors
- Ensure virtual environment is activated
- Reinstall: `pip install -e .`

### API authentication errors
- Verify credentials in .env
- Check API key permissions

## Support

For issues and questions:
- GitHub Issues: https://github.com/khushwantraj/Finsight/issues
- Documentation: See README.md
