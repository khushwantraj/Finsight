"""Configuration management for Finsight."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Database
    database_url: str = "sqlite:///./finsight.db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Encryption
    encryption_key: str = ""
    
    # Plaid
    plaid_client_id: str = ""
    plaid_secret: str = ""
    plaid_env: str = "sandbox"
    
    # Kite
    kite_api_key: str = ""
    kite_api_secret: str = ""
    
    # AlphaVantage
    alpha_vantage_api_key: str = ""
    
    # CCXT
    ccxt_exchange: str = "binance"
    ccxt_api_key: str = ""
    ccxt_api_secret: str = ""
    
    # Webhook
    webhook_secret: str = ""
    webhook_host: str = "http://localhost:8000"


settings = Settings()
