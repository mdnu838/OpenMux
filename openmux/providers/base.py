"""Base provider interface for OpenCascade."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import time
import asyncio


class ProviderHealth:
    """Health status for a provider."""
    
    def __init__(self):
        self.is_healthy = True
        self.last_check = 0.0
        self.response_time = 0.0
        self.error_count = 0
        self.success_count = 0
        self.last_error: Optional[str] = None
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        total = self.success_count + self.error_count
        if total == 0:
            return 1.0
        return self.success_count / total
    
    @property
    def avg_response_time(self) -> float:
        """Get average response time."""
        return self.response_time


class BaseProvider(ABC):
    """Base class for all model providers."""
    
    def __init__(self, name: str):
        """Initialize base provider.
        
        Args:
            name: Provider name
        """
        self._name = name
        self._health = ProviderHealth()
    
    @property
    def name(self) -> str:
        """Get provider name."""
        return self._name
    
    @property
    def health(self) -> ProviderHealth:
        """Get provider health status."""
        return self._health
    
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
    
    async def health_check(self, timeout: float = 5.0) -> bool:
        """Perform a health check on the provider.
        
        Args:
            timeout: Timeout for health check in seconds
            
        Returns:
            True if provider is healthy, False otherwise
        """
        start_time = time.time()
        
        try:
            # Simple test query
            test_prompt = "Hello"
            
            # Run with timeout
            response = await asyncio.wait_for(
                self.generate(test_prompt, max_tokens=5),
                timeout=timeout
            )
            
            # Update health metrics
            self._health.is_healthy = True
            self._health.last_check = time.time()
            self._health.response_time = time.time() - start_time
            self._health.success_count += 1
            self._health.last_error = None
            
            return True
            
        except asyncio.TimeoutError:
            self._health.is_healthy = False
            self._health.last_check = time.time()
            self._health.error_count += 1
            self._health.last_error = f"Health check timeout after {timeout}s"
            return False
            
        except Exception as e:
            self._health.is_healthy = False
            self._health.last_check = time.time()
            self._health.error_count += 1
            self._health.last_error = str(e)
            return False
