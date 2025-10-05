"""Tests for credential management."""

import pytest
from finsight.core.credentials import CredentialManager, TokenStore


class TestCredentialManager:
    """Test CredentialManager functionality."""
    
    def test_generate_key(self):
        """Test key generation."""
        key = CredentialManager.generate_key()
        assert key
        assert isinstance(key, str)
        assert len(key) > 0
    
    def test_encrypt_decrypt(self):
        """Test encryption and decryption."""
        key = CredentialManager.generate_key()
        manager = CredentialManager(key)
        
        original_data = "my-secret-token"
        encrypted = manager.encrypt(original_data)
        
        assert encrypted != original_data
        
        decrypted = manager.decrypt(encrypted)
        assert decrypted == original_data
    
    def test_encryption_key_required(self):
        """Test that encryption key is required."""
        with pytest.raises(ValueError, match="Encryption key must be provided"):
            CredentialManager("")


class TestTokenStore:
    """Test TokenStore functionality."""
    
    def test_store_and_get_token(self):
        """Test storing and retrieving tokens."""
        key = CredentialManager.generate_key()
        token_store = TokenStore(CredentialManager(key))
        
        provider = "plaid"
        user_id = "user123"
        token = "access-token-12345"
        
        token_store.store_token(provider, user_id, token)
        retrieved = token_store.get_token(provider, user_id)
        
        assert retrieved == token
    
    def test_get_nonexistent_token(self):
        """Test retrieving non-existent token."""
        key = CredentialManager.generate_key()
        token_store = TokenStore(CredentialManager(key))
        
        retrieved = token_store.get_token("plaid", "nonexistent")
        assert retrieved is None
    
    def test_delete_token(self):
        """Test deleting tokens."""
        key = CredentialManager.generate_key()
        token_store = TokenStore(CredentialManager(key))
        
        provider = "plaid"
        user_id = "user123"
        token = "access-token-12345"
        
        token_store.store_token(provider, user_id, token)
        assert token_store.delete_token(provider, user_id) is True
        assert token_store.get_token(provider, user_id) is None
    
    def test_delete_nonexistent_token(self):
        """Test deleting non-existent token."""
        key = CredentialManager.generate_key()
        token_store = TokenStore(CredentialManager(key))
        
        assert token_store.delete_token("plaid", "nonexistent") is False
