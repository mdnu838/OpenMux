"""
Provider registry for managing available GenAI providers.
"""

import logging
from typing import Dict, List, Optional

from .base import BaseProvider
from .openrouter import OpenRouterProvider
from .huggingface import HuggingFaceProvider
from .ollama import OllamaProvider
from ..utils.logging import setup_logger


logger = setup_logger(__name__)


class ProviderRegistry:
    """Registry for managing and accessing GenAI providers."""
    
    def __init__(self):
        """Initialize the provider registry."""
        self._providers: Dict[str, BaseProvider] = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available providers."""
        # OpenRouter
        try:
            openrouter = OpenRouterProvider()
            if openrouter.is_available():
                self._providers["openrouter"] = openrouter
                logger.info("OpenRouter provider registered")
        except Exception as e:
            logger.warning(f"Failed to initialize OpenRouter: {e}")
        
        # HuggingFace
        try:
            huggingface = HuggingFaceProvider()
            if huggingface.is_available():
                self._providers["huggingface"] = huggingface
                logger.info("HuggingFace provider registered")
        except Exception as e:
            logger.warning(f"Failed to initialize HuggingFace: {e}")
        
        # Ollama
        try:
            ollama = OllamaProvider()
            if ollama.is_available():
                self._providers["ollama"] = ollama
                logger.info("Ollama provider registered")
        except Exception as e:
            logger.warning(f"Failed to initialize Ollama: {e}")
    
    def get(self, name: str) -> Optional[BaseProvider]:
        """Get a provider by name.
        
        Args:
            name: Provider name (e.g., "openrouter", "huggingface", "ollama")
            
        Returns:
            Provider instance or None if not found
        """
        return self._providers.get(name.lower())
    
    def get_all(self) -> Dict[str, BaseProvider]:
        """Get all registered providers.
        
        Returns:
            Dictionary of provider name -> provider instance
        """
        return self._providers.copy()
    
    def get_all_available(self) -> List[BaseProvider]:
        """Get all available providers as a list.
        
        Returns:
            List of provider instances
        """
        return list(self._providers.values())
    
    def is_available(self, name: str) -> bool:
        """Check if a provider is available.
        
        Args:
            name: Provider name
            
        Returns:
            True if provider is registered and available
        """
        provider = self.get(name)
        return provider is not None and provider.is_available()
