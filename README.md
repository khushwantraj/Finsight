# Finsight

A comprehensive financial institution connector framework for integrating with banking, stock trading, and cryptocurrency platforms.

## Features

- **Multiple Connectors**: Out-of-the-box support for Plaid (banking), Kite Connect (Indian stocks), AlphaVantage (market data), and CCXT (crypto exchanges)
- **Secure Credential Storage**: Encrypted credential management with Fernet encryption
- **OAuth Flow Handling**: Built-in support for OAuth 2.0 and token-based authentication
- **Data Ingestion**: Celery-based background workers for periodic data synchronization
- **Webhook Support**: Real-time updates via webhook handlers
- **Modular Design**: Easy to extend with new providers
- **Type-Safe**: Pydantic models for data validation
- **Well-Tested**: Comprehensive unit test coverage

## Architecture

```
finsight/
├── connectors/          # Connector implementations
│   ├── base.py         # Base connector interface
│   ├── plaid_connector.py
│   ├── kite_connector.py
│   ├── alphavantage_connector.py
│   ├── ccxt_connector.py
│   └── factory.py      # Connector factory
├── core/               # Core utilities
│   ├── config.py       # Configuration management
│   └── credentials.py  # Secure credential storage
├── workers/            # Celery workers
│   ├── celery_app.py   # Celery configuration
│   └── tasks.py        # Background tasks
└── api/                # FastAPI endpoints
    ├── app.py          # Main application
    ├── oauth.py        # OAuth callbacks
    └── webhooks.py     # Webhook handlers
```

## Installation

### Prerequisites

- Python 3.9+
- Redis (for Celery broker)
- PostgreSQL (optional, for production)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/khushwantraj/Finsight.git
cd Finsight
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. Generate encryption key:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Add the generated key to your `.env` file as `ENCRYPTION_KEY`.

## Configuration

### Environment Variables

Configure the following in your `.env` file:

#### Database
- `DATABASE_URL`: PostgreSQL connection string (default: SQLite)

#### Redis
- `REDIS_URL`: Redis connection string for Celery

#### Encryption
- `ENCRYPTION_KEY`: Fernet encryption key for credential storage

#### Plaid Configuration
- `PLAID_CLIENT_ID`: Your Plaid client ID
- `PLAID_SECRET`: Your Plaid secret
- `PLAID_ENV`: Environment (sandbox/development/production)

#### Kite Connect Configuration
- `KITE_API_KEY`: Your Kite Connect API key
- `KITE_API_SECRET`: Your Kite Connect API secret

#### AlphaVantage Configuration
- `ALPHA_VANTAGE_API_KEY`: Your AlphaVantage API key

#### CCXT Configuration
- `CCXT_EXCHANGE`: Exchange name (e.g., binance, coinbase)
- `CCXT_API_KEY`: Exchange API key
- `CCXT_API_SECRET`: Exchange API secret

#### Webhook Configuration
- `WEBHOOK_SECRET`: Secret for webhook signature verification
- `WEBHOOK_HOST`: Your application host URL

## Usage

### Starting the API Server

```bash
# Development
uvicorn finsight.api.app:app --reload

# Production
uvicorn finsight.api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Starting Celery Workers

```bash
# Start worker
celery -A finsight.workers.celery_app worker --loglevel=info

# Start with beat scheduler (for periodic tasks)
celery -A finsight.workers.celery_app worker --beat --loglevel=info
```

### Using Connectors

#### Plaid Example

```python
from finsight.connectors.factory import ConnectorFactory

# Create connector
credentials = {
    'client_id': 'your_client_id',
    'secret': 'your_secret'
}
plaid = ConnectorFactory.create('plaid', credentials)

# Create link token for user
result = plaid.create_link_token(user_id='user123')
link_token = result.data['link_token']

# After user completes Plaid Link, exchange public token
result = plaid.exchange_public_token(public_token)
access_token = result.data['access_token']

# Use access token to get accounts
credentials['access_token'] = access_token
plaid = ConnectorFactory.create('plaid', credentials)
accounts = plaid.get_accounts()
```

#### Kite Connect Example

```python
from finsight.connectors.factory import ConnectorFactory

credentials = {
    'api_key': 'your_api_key',
    'api_secret': 'your_api_secret'
}
kite = ConnectorFactory.create('kite', credentials)

# Get login URL
login_url = kite.get_login_url()
# Redirect user to login_url

# After OAuth callback, generate session
result = kite.generate_session(request_token)
access_token = result.data['access_token']

# Get positions
positions = kite.get_positions()
```

#### AlphaVantage Example

```python
from finsight.connectors.factory import ConnectorFactory

credentials = {'api_key': 'your_api_key'}
av = ConnectorFactory.create('alphavantage', credentials)

# Get stock quote
quote = av.get_quote('AAPL')

# Get intraday data
intraday = av.get_intraday('AAPL', interval='5min')

# Get company overview
overview = av.get_company_overview('AAPL')
```

#### CCXT Example

```python
from finsight.connectors.factory import ConnectorFactory

credentials = {
    'exchange': 'binance',
    'api_key': 'your_api_key',
    'api_secret': 'your_api_secret'
}
ccxt = ConnectorFactory.create('ccxt', credentials)

# Get accounts/balances
accounts = ccxt.get_accounts()

# Get ticker
ticker = ccxt.get_ticker('BTC/USDT')

# Get open orders
orders = ccxt.get_open_orders('BTC/USDT')
```

### Background Tasks

```python
from finsight.workers.tasks import sync_accounts, periodic_sync

# Trigger account sync
result = sync_accounts.delay('plaid', 'user123', credentials)

# Schedule periodic sync
periodic_sync.apply_async(
    args=['plaid', 'user123', credentials],
    countdown=3600  # Run after 1 hour
)
```

### Webhooks

The API server exposes webhook endpoints for real-time updates:

- `POST /webhooks/plaid` - Plaid webhook events
- `POST /webhooks/kite` - Kite Connect postbacks
- `POST /webhooks/ccxt/{exchange}` - Exchange webhooks

Configure these URLs in your provider dashboards.

### OAuth Callbacks

OAuth callback endpoints:

- `GET /oauth/plaid/callback?public_token=xxx&user_id=xxx`
- `GET /oauth/kite/callback?request_token=xxx&user_id=xxx&api_key=xxx&api_secret=xxx`
- `GET /oauth/redirect?code=xxx&state=xxx` - Generic OAuth redirect

## Adding New Connectors

1. Create a new connector class extending `BaseConnector`:

```python
from finsight.connectors.base import BaseConnector, AuthType, ConnectorResponse

class MyConnector(BaseConnector):
    @property
    def provider_name(self) -> str:
        return "myprovider"
    
    @property
    def auth_type(self) -> AuthType:
        return AuthType.API_KEY
    
    def _validate_credentials(self) -> None:
        if 'api_key' not in self.credentials:
            raise ValueError("API key required")
    
    # Implement required methods...
```

2. Register the connector:

```python
from finsight.connectors.factory import ConnectorFactory

ConnectorFactory.register('myprovider', MyConnector)
```

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=finsight --cov-report=html

# Run specific test file
pytest tests/test_credentials.py

# Run with verbose output
pytest -v
```

## API Documentation

Once the server is running, access interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Security Considerations

1. **Credential Storage**: All credentials are encrypted using Fernet symmetric encryption
2. **Environment Variables**: Never commit `.env` file to version control
3. **Webhook Verification**: Verify webhook signatures before processing
4. **Token Rotation**: Implement regular token refresh for long-lived connections
5. **HTTPS**: Always use HTTPS in production
6. **Rate Limiting**: Implement rate limiting for API endpoints

## Production Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY finsight/ ./finsight/
CMD ["uvicorn", "finsight.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - redis
      - postgres
  
  worker:
    build: .
    command: celery -A finsight.workers.celery_app worker --loglevel=info
    env_file: .env
    depends_on:
      - redis
      - postgres
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: finsight
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
2. **Redis Connection**: Verify Redis is running (`redis-cli ping`)
3. **API Key Issues**: Check environment variables are loaded
4. **Webhook Delivery**: Ensure your server is publicly accessible

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/khushwantraj/Finsight/issues
- Documentation: See inline code documentation

## Roadmap

- [ ] Add support for more providers (Schwab, Interactive Brokers, etc.)
- [ ] Implement data caching layer
- [ ] Add GraphQL API
- [ ] Build admin dashboard
- [ ] Add monitoring and alerting
- [ ] Implement audit logging
- [ ] Support for international markets