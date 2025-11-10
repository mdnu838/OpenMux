"""Fallback handler for provider failures."""

import logging
from typing import Optional

from ..providers.base import BaseProvider
from ..utils.exceptions import ProviderError, ProviderUnavailableError


logger = logging.getLogger(__name__)


class FallbackHandler:
    """Handles fallback to alternative providers when primary providers fail."""
    
    def __init__(self, ollama_provider: Optional[BaseProvider] = None):
        """Initialize fallback handler.
        
        Args:
            ollama_provider: Ollama provider for offline fallback
        """
        self.ollama_provider = ollama_provider
        logger.info("FallbackHandler initialized")
    
    def has_fallback(self) -> bool:
        """Check if fallback is available.
        
        Returns:
            True if fallback provider is available
        """
        return self.ollama_provider is not None
    
    async def fallback(self, query: str, **kwargs) -> str:
        """Execute fallback query.
        
        Args:
            query: Query string
            **kwargs: Additional parameters
            
        Returns:
            Response from fallback provider
            
        Raises:
            Exception: If no fallback available or fallback fails
        """
        if not self.has_fallback():
            logger.error("No fallback provider available")
            raise ProviderUnavailableError(
                "Fallback",
                "No fallback provider configured (Ollama not available)"
            )
        
        logger.info("Attempting fallback to Ollama")
        
        try:
            response = await self.ollama_provider.generate(query, **kwargs)
            logger.info("Fallback successful")
            return response
        except Exception as e:
            logger.error(f"Fallback failed: {e}")
            if isinstance(e, ProviderError):
                raise
            raise ProviderError("Ollama", f"Fallback failed: {str(e)}")
