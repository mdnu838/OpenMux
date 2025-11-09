"""
Ollama local provider implementation for offline AI.
"""

import os
from typing import Optional, Dict, Any
import aiohttp

from .base import BaseProvider
from ..classifier.task_types import TaskType
from ..utils.logging import setup_logger


logger = setup_logger(__name__)


class OllamaProvider(BaseProvider):
    """Provider for Ollama local models."""
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        """Initialize Ollama provider.
        
        Args:
            base_url: Ollama API base URL (default: http://localhost:11434)
            model: Default model name (default: llama2)
        """
        super().__init__(name="Ollama")
        
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama2")
        self._session: Optional[aiohttp.ClientSession] = None
        self._available: Optional[bool] = None
    
    def is_available(self) -> bool:
        """Check if Ollama is available.
        
        Returns:
            True if Ollama server is running
        """
        if self._available is not None:
            return self._available
        
        # Simple sync check - will be refined with async check on first use
        import requests
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            self._available = response.status_code == 200
        except:
            self._available = False
        
        return self._available
    
    def supports_task(self, task_type: TaskType) -> bool:
        """Check if provider supports the task type.
        
        Args:
            task_type: Task type to check
            
        Returns:
            True if supported
        """
        # Ollama primarily supports chat and code
        return task_type in [TaskType.CHAT, TaskType.CODE]
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session.
        
        Returns:
            Client session
        """
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def _check_availability(self) -> bool:
        """Async check for Ollama availability.
        
        Returns:
            True if available
        """
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/api/tags", timeout=aiohttp.ClientTimeout(total=2)) as response:
                self._available = response.status == 200
                return self._available
        except:
            self._available = False
            return False
    
    async def generate(
        self,
        query: str,
        task_type: Optional[TaskType] = None,
        **kwargs
    ) -> str:
        """Generate response using Ollama.
        
        Args:
            query: Input query
            task_type: Task type (optional)
            **kwargs: Additional parameters
            
        Returns:
            Generated response
        """
        # Check availability
        if not await self._check_availability():
            raise Exception("Ollama provider not available: server not running")
        
        logger.info(f"Using Ollama model: {self.model}")
        
        # Build request
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": kwargs.get("model", self.model),
            "prompt": query,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9)
            }
        }
        
        if "max_tokens" in kwargs:
            payload["options"]["num_predict"] = kwargs["max_tokens"]
        
        try:
            session = await self._get_session()
            async with session.post(url, json=payload) as response:
                response.raise_for_status()
                result = await response.json()
                
                if "response" in result:
                    return result["response"]
                
                return str(result)
                
        except aiohttp.ClientError as e:
            logger.error(f"Ollama API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generating with Ollama: {e}")
            raise
    
    async def close(self):
        """Close the provider session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
