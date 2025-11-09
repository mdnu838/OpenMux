"""Base provider interface for OpenCascade."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class BaseProvider(ABC):
    """Base class for all model providers."""
    
    def __init__(self, name: str):
        """Initialize base provider.
        
        Args:
            name: Provider name
        """
        self._name = name
    
    @property
    def name(self) -> str:
        """Get provider name."""
        return self._name
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available."""
        pass
    
    @abstractmethod
    def supports_task(self, task_type) -> bool:
        """Check if provider supports the given task type."""
        pass
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response for the given prompt."""
        pass
