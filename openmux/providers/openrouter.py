"""OpenRouter provider implementation."""

import os
from typing import Dict, Any, List, Optional
import aiohttp
import json
from datetime import datetime

from .base import BaseProvider
from ..utils.exceptions import ConfigurationError, APIError


class OpenRouterProvider(BaseProvider):
    """Provider implementation for OpenRouter free tier."""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize OpenRouter provider.
        
        Args:
            api_key: OpenRouter API key (or use OPENROUTER_API_KEY env var)
            config: Optional configuration dictionary
        """
        super().__init__(name="OpenRouter")
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.config = config or {}
        self.base_url = "https://openrouter.ai/api/v1"
        self._capabilities = None
        self._last_health_check = None
        self._session: Optional[aiohttp.ClientSession] = None
    
    def is_available(self) -> bool:
        """Check if OpenRouter is available."""
        return self.api_key is not None
    
    def supports_task(self, task_type) -> bool:
        """Check if provider supports the task type."""
        from ..classifier.task_types import TaskType
        # OpenRouter supports chat and code
        return task_type in [TaskType.CHAT, TaskType.CODE]
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def generate(self, prompt: str, task_type=None, **kwargs) -> str:
        """Generate a response using OpenRouter.
        
        Args:
            prompt: Input prompt
            task_type: Task type (optional)
            **kwargs: Additional parameters
            
        Returns:
            Generated response
        """
        if not self.api_key:
            raise ConfigurationError(
                "OpenRouter API key not configured",
                "Set OPENROUTER_API_KEY in your .env file or run 'openmux init'"
            )
        
        # Use a working free model - try google/gemma-2-9b-it:free or mistralai/mistral-7b-instruct:free
        model = kwargs.get("model", "mistralai/mistral-7b-instruct:free")
        
        session = await self._get_session()
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 512)
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/mdnu838/openmux",
            "X-Title": "OpenCascade"
        }
        
        async with session.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers=headers
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                raise APIError(
                    "OpenRouter",
                    status_code=response.status,
                    response_text=error_text
                )
                
            result = await response.json()
            
            # Extract response from OpenRouter format
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            
            return str(result)
    
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
