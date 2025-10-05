"""Secure credential storage and encryption."""

from cryptography.fernet import Fernet
from typing import Optional
from finsight.core.config import settings


class CredentialManager:
    """Manages secure storage and retrieval of credentials."""
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize the credential manager.
        
        Args:
            encryption_key: Base64-encoded encryption key. If not provided, uses settings.
        """
        key = encryption_key or settings.encryption_key
        if not key:
            raise ValueError("Encryption key must be provided")
        self.cipher = Fernet(key.encode() if isinstance(key, str) else key)
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt sensitive data.
        
        Args:
            data: Plain text data to encrypt
            
        Returns:
            Encrypted data as base64 string
        """
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt sensitive data.
        
        Args:
            encrypted_data: Base64-encoded encrypted data
            
        Returns:
            Decrypted plain text data
        """
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    @staticmethod
    def generate_key() -> str:
        """
        Generate a new encryption key.
        
        Returns:
            Base64-encoded encryption key
        """
        return Fernet.generate_key().decode()


class TokenStore:
    """In-memory token storage with encryption."""
    
    def __init__(self, credential_manager: Optional[CredentialManager] = None):
        """
        Initialize token store.
        
        Args:
            credential_manager: CredentialManager instance for encryption
        """
        self.credential_manager = credential_manager or CredentialManager()
        self._tokens: dict[str, str] = {}
    
    def store_token(self, provider: str, user_id: str, token: str) -> None:
        """
        Store an encrypted token.
        
        Args:
            provider: Provider name (e.g., 'plaid', 'kite')
            user_id: User identifier
            token: Token to store
        """
        key = f"{provider}:{user_id}"
        encrypted_token = self.credential_manager.encrypt(token)
        self._tokens[key] = encrypted_token
    
    def get_token(self, provider: str, user_id: str) -> Optional[str]:
        """
        Retrieve and decrypt a token.
        
        Args:
            provider: Provider name
            user_id: User identifier
            
        Returns:
            Decrypted token or None if not found
        """
        key = f"{provider}:{user_id}"
        encrypted_token = self._tokens.get(key)
        if encrypted_token:
            return self.credential_manager.decrypt(encrypted_token)
        return None
    
    def delete_token(self, provider: str, user_id: str) -> bool:
        """
        Delete a stored token.
        
        Args:
            provider: Provider name
            user_id: User identifier
            
        Returns:
            True if token was deleted, False if not found
        """
        key = f"{provider}:{user_id}"
        if key in self._tokens:
            del self._tokens[key]
            return True
        return False
