"""Configuration management for OpenMux."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import json


class ConfigurationError(Exception):
    """Configuration related errors."""
    pass


class Config:
    """Simple configuration management using JSON files."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.
        
        Note: API keys and secrets should be stored in .env file,
        not in the config file. This is just for user preferences.
        """
        self.config_path = Path(config_path) if config_path else self._default_config_path()
        self._ensure_config_dir()
    
    @staticmethod
    def _default_config_path() -> Path:
        """Get default configuration path."""
        return Path.home() / ".openmux" / "config.json"
    
    def _ensure_config_dir(self) -> None:
        """Ensure configuration directory exists."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if not self.config_path.exists():
            return {}
            
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {str(e)}")
    
    def save(self, config: Dict[str, Any]) -> None:
        """Save configuration to JSON file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
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