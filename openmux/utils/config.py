"""Configuration management for OpenCascade."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import json
import keyring
from cryptography.fernet import Fernet

class ConfigurationError(Exception):
    """Configuration related errors."""
    pass

class Config:
    """Secure configuration management."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_path = Path(config_path) if config_path else self._default_config_path()
        self._ensure_config_dir()
        self._init_encryption()
    
    @staticmethod
    def _default_config_path() -> Path:
        """Get default configuration path."""
        return Path.home() / ".openmux" / "config.json"
    
    def _ensure_config_dir(self) -> None:
        """Ensure configuration directory exists."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _init_encryption(self) -> None:
        """Initialize encryption key."""
        key = keyring.get_password("openmux", "encryption_key")
        if not key:
            key = Fernet.generate_key().decode()
            keyring.set_password("openmux", "encryption_key", key)
        self.fernet = Fernet(key.encode())
    
    def load(self) -> Dict[str, Any]:
        """Load configuration securely."""
        if not self.config_path.exists():
            return {}
            
        try:
            encrypted_data = self.config_path.read_bytes()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {str(e)}")
    
    def save(self, config: Dict[str, Any]) -> None:
        """Save configuration securely."""
        try:
            json_data = json.dumps(config, indent=2)
            encrypted_data = self.fernet.encrypt(json_data.encode())
            self.config_path.write_bytes(encrypted_data)
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {str(e)}")
    
    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """Get configuration for specific provider."""
        config = self.load()
        return config.get("providers", {}).get(provider_name, {})
    
    def update_provider_config(
        self,
        provider_name: str,
        provider_config: Dict[str, Any]
    ) -> None:
        """Update configuration for specific provider."""
        config = self.load()
        if "providers" not in config:
            config["providers"] = {}
        config["providers"][provider_name] = provider_config
        self.save(config)
    
    def get_fallback_config(self) -> Dict[str, Any]:
        """Get fallback configuration."""
        config = self.load()
        return config.get("fallback", {})
    
    def get_model_registry(self) -> Dict[str, Any]:
        """Get model registry configuration."""
        config = self.load()
        return config.get("model_registry", {})