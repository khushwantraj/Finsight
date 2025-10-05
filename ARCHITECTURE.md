# Finsight Architecture

## Overview

Finsight is a modular financial institution connector framework built with Python, designed to integrate with various financial data providers including banks, stock trading platforms, and cryptocurrency exchanges.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  (Web Apps, Mobile Apps, CLI Tools, Third-party Services)   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTP/REST
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      API Layer (FastAPI)                     │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────┐      │
│  │  Webhooks  │  │   OAuth    │  │  Health Check    │      │
│  │  Handlers  │  │ Callbacks  │  │   Endpoints      │      │
│  └────────────┘  └────────────┘  └──────────────────┘      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    Core Business Logic                       │
│  ┌────────────────────────────────────────────────────┐     │
│  │            Connector Factory                        │     │
│  │  Creates and manages connector instances           │     │
│  └────────────┬───────────────────────────────────────┘     │
│               │                                              │
│  ┌────────────▼────────────────────────────────────────┐    │
│  │         Base Connector Interface                    │    │
│  │  - authenticate()                                   │    │
│  │  - get_accounts()                                   │    │
│  │  - get_transactions()                               │    │
│  │  - get_balances()                                   │    │
│  └────────────┬────────────────────────────────────────┘    │
│               │                                              │
│  ┌────────────▼───────────┬────────────┬──────────────┐     │
│  │   PlaidConnector      │   Kite     │AlphaVantage  │     │
│  │   (Banking)           │ Connector  │  Connector   │     │
│  │                       │ (Stocks)   │ (Market Data)│     │
│  └───────────────────────┴────────────┴──────────────┘     │
│  ┌────────────────────────────────────────────────────┐     │
│  │          CCXTConnector (Crypto Exchanges)          │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   Background Workers                         │
│  ┌────────────────────────────────────────────────────┐     │
│  │              Celery Workers                        │     │
│  │  - sync_accounts                                   │     │
│  │  - sync_transactions                               │     │
│  │  - sync_balances                                   │     │
│  │  - periodic_sync                                   │     │
│  │  - refresh_token                                   │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   Infrastructure Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Redis   │  │ Database │  │ External │  │   Logs   │   │
│  │ (Broker) │  │(Storage) │  │   APIs   │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. API Layer

**Technology**: FastAPI with Uvicorn

**Components**:
- **Main Application** (`api/app.py`): Central FastAPI application
- **Webhook Handlers** (`api/webhooks.py`): Receive real-time updates from providers
- **OAuth Callbacks** (`api/oauth.py`): Handle OAuth flows and token exchanges

**Responsibilities**:
- Request routing and validation
- Authentication and authorization
- API documentation (OpenAPI/Swagger)
- Error handling and response formatting

### 2. Core Business Logic

#### Connector System

**Base Connector** (`connectors/base.py`):
- Abstract base class defining the connector interface
- Standardized response format (ConnectorResponse)
- Authentication types (API_KEY, OAUTH2, TOKEN)
- Status tracking (SUCCESS, ERROR, PENDING, EXPIRED)

**Connector Implementations**:

1. **PlaidConnector** (`connectors/plaid_connector.py`)
   - Banking and financial institution integration
   - OAuth 2.0 flow with link token creation
   - Account, transaction, and balance retrieval
   - Webhook support for real-time updates

2. **KiteConnector** (`connectors/kite_connector.py`)
   - Indian stock market integration (Zerodha Kite)
   - Token-based authentication
   - Trading positions, holdings, orders
   - Market data access

3. **AlphaVantageConnector** (`connectors/alphavantage_connector.py`)
   - Stock market data provider
   - API key authentication
   - Real-time quotes, historical data
   - Company fundamentals and crypto data

4. **CCXTConnector** (`connectors/ccxt_connector.py`)
   - Cryptocurrency exchange integration
   - Support for 100+ exchanges via CCXT library
   - Trading, balances, order book access
   - Unified API across exchanges

**Connector Factory** (`connectors/factory.py`):
- Factory pattern for connector instantiation
- Provider registration and discovery
- Extensible design for adding new connectors

#### Security Layer

**Credential Manager** (`core/credentials.py`):
- Fernet symmetric encryption for credentials
- Key generation and management
- Secure encryption/decryption operations

**Token Store** (`core/credentials.py`):
- In-memory encrypted token storage
- Provider-specific token management
- CRUD operations for tokens

**Configuration** (`core/config.py`):
- Pydantic settings management
- Environment variable loading
- Type-safe configuration

### 3. Background Workers

**Technology**: Celery with Redis broker

**Tasks** (`workers/tasks.py`):

1. **sync_accounts**: Fetch account data from providers
2. **sync_transactions**: Retrieve transaction history
3. **sync_balances**: Get current balance information
4. **periodic_sync**: Scheduled full data synchronization
5. **refresh_token**: Automatic token refresh

**Configuration** (`workers/celery_app.py`):
- Task serialization (JSON)
- Worker configuration
- Rate limiting and timeout settings

### 4. Infrastructure

**Redis**:
- Celery message broker
- Task queue management
- Result backend

**Database** (optional):
- PostgreSQL for production
- SQLite for development
- SQLAlchemy ORM support
- Alembic for migrations

**External APIs**:
- Plaid API (banking)
- Kite Connect API (stocks)
- AlphaVantage API (market data)
- CCXT-supported exchanges (crypto)

## Data Flow

### 1. OAuth Authentication Flow

```
User → Frontend → API (/oauth/plaid/callback)
                   ↓
          Create Connector
                   ↓
          Exchange Tokens
                   ↓
          Encrypt & Store Token
                   ↓
          Return Success
```

### 2. Data Synchronization Flow

```
Schedule Task → Celery Queue → Worker Picks Task
                                      ↓
                              Create Connector
                                      ↓
                              Authenticate
                                      ↓
                              Fetch Data
                                      ↓
                              Transform & Store
                                      ↓
                              Return Result
```

### 3. Webhook Processing Flow

```
Provider → Webhook Endpoint → Verify Signature
                                     ↓
                              Parse Event
                                     ↓
                              Queue Background Task
                                     ↓
                              Return Acknowledgment
```

## Scalability Considerations

### Horizontal Scaling

1. **API Layer**: Deploy multiple Uvicorn instances behind load balancer
2. **Workers**: Scale Celery workers based on queue depth
3. **Redis**: Redis Cluster for high availability
4. **Database**: Read replicas for query load distribution

### Performance Optimization

1. **Caching**: Redis for frequently accessed data
2. **Connection Pooling**: Reuse database connections
3. **Async Operations**: Utilize FastAPI's async capabilities
4. **Rate Limiting**: Respect provider API limits

### Monitoring

1. **Health Checks**: Built-in endpoints for monitoring
2. **Logging**: Structured logging for debugging
3. **Metrics**: Task success/failure rates
4. **Alerts**: Notify on critical failures

## Security Architecture

### Defense in Depth

1. **Transport Security**: HTTPS/TLS for all communications
2. **Data Encryption**: Fernet encryption for credentials at rest
3. **Webhook Verification**: HMAC signature verification
4. **Input Validation**: Pydantic models for request validation
5. **Environment Isolation**: Separate configs for dev/staging/prod

### Credential Management

1. **Never commit secrets**: Use environment variables
2. **Key rotation**: Support for credential updates
3. **Minimal permissions**: Provider API keys with least privilege
4. **Token expiration**: Automatic refresh mechanisms

## Extension Points

### Adding New Connectors

1. Extend `BaseConnector` class
2. Implement required methods
3. Register with `ConnectorFactory`
4. Add tests and documentation

### Custom Authentication

1. Extend `AuthType` enum
2. Implement authentication logic in connector
3. Update OAuth handlers if needed

### Additional Background Tasks

1. Define task in `workers/tasks.py`
2. Configure Celery task settings
3. Add task scheduling if needed

## Testing Strategy

### Unit Tests

- Connector functionality
- Credential encryption/decryption
- Task execution logic
- Factory pattern

### Integration Tests

- API endpoints
- OAuth flows
- Webhook processing
- End-to-end scenarios

### Test Coverage

- Current: 52%
- Target: 80%+
- Focus areas: Core business logic, security components

## Deployment Architecture

### Docker Deployment

```
┌──────────────────────────────────────┐
│         Load Balancer (nginx)        │
└────────────┬─────────────────────────┘
             │
     ┌───────┴────────┐
     │                │
     ▼                ▼
┌─────────┐      ┌─────────┐
│  API 1  │      │  API 2  │
└─────────┘      └─────────┘
     │                │
     └────────┬───────┘
              │
     ┌────────▼────────┐
     │     Redis       │
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │   PostgreSQL    │
     └─────────────────┘

┌─────────────────────────────────────┐
│     Celery Workers (3+ instances)   │
└─────────────────────────────────────┘
```

### Cloud Deployment Options

1. **AWS**: ECS/Fargate, RDS, ElastiCache
2. **GCP**: Cloud Run, Cloud SQL, Memorystore
3. **Azure**: Container Instances, Azure Database, Azure Cache
4. **Kubernetes**: Deployments, Services, ConfigMaps

## Future Enhancements

1. GraphQL API support
2. WebSocket connections for real-time updates
3. Data analytics and insights
4. Admin dashboard
5. Audit logging
6. Multi-tenancy support
7. Rate limiting per provider
8. Circuit breaker pattern for resilience
