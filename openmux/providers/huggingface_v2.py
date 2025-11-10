"""
Updated HuggingFace provider using official huggingface_hub library.

The old Inference API (api-inference.huggingface.co) has been deprecated.
This implementation uses the official `huggingface_hub` Python library
which handles the new API endpoints automatically.

Installation: pip install huggingface-hub
"""

import os
from typing import Optional, Dict, Any
from huggingface_hub import InferenceClient
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .base import BaseProvider
from ..classifier.task_types import TaskType
from ..utils.logging import setup_logger


logger = setup_logger(__name__)


class HuggingFaceProviderV2(BaseProvider):
    """Updated HuggingFace provider using official huggingface_hub library."""
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        model_id: Optional[str] = None
    ):
        """Initialize HuggingFace provider.
        
        Args:
            api_token: HuggingFace API token (or use HF_TOKEN env var)
            model_id: Default model ID to use
        """
        super().__init__(name="HuggingFace")
        
        self.api_token = api_token or os.getenv("HF_TOKEN")
        
        # Default models for different task types (using available models)
        self.default_models = {
            TaskType.CHAT: "microsoft/DialoGPT-medium",
            TaskType.CODE: "Salesforce/codegen-350M-mono",
            TaskType.EMBEDDINGS: "sentence-transformers/all-MiniLM-L6-v2"
        }
        
        self.model_id = model_id
        self.client: Optional[InferenceClient] = None
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def is_available(self) -> bool:
        """Check if HuggingFace API is available."""
        return self.api_token is not None
    
    def supports_task(self, task_type: TaskType) -> bool:
        """Check if provider supports the task type."""
        return task_type in self.default_models
    
    def _get_client(self) -> InferenceClient:
        """Get or create inference client."""
        if self.client is None:
            self.client = InferenceClient(token=self.api_token)
        return self.client
    
    async def generate(
        self,
        query: str,
        task_type: TaskType = TaskType.CHAT,
        **kwargs
    ) -> str:
        """Generate response using HuggingFace.
        
        Args:
            query: Input query
            task_type: Type of task
            **kwargs: Additional parameters
            
        Returns:
            Generated response
        """
        # Get model for task type
        model = self.model_id or self.default_models.get(task_type)
        
        if not model:
            raise ValueError(f"No model available for task type: {task_type}")
        
        logger.info(f"Using HuggingFace model: {model}")
        
        try:
            client = self._get_client()
            
            # Get event loop
            loop = asyncio.get_event_loop()
            
            if task_type == TaskType.EMBEDDINGS:
                # Feature extraction for embeddings
                def extract_features():
                    return client.feature_extraction(query, model=model)
                
                response = await loop.run_in_executor(self.executor, extract_features)
                return str(response)
            else:
                # Text generation for chat/code
                def generate_text():
                    return client.text_generation(
                        query,
                        model=model,
                        max_new_tokens=kwargs.get('max_new_tokens', 100),
                        temperature=kwargs.get('temperature', 0.7),
                        top_p=kwargs.get('top_p', 0.9),
                        return_full_text=False
                    )
                
                response = await loop.run_in_executor(self.executor, generate_text)
                return response
            
        except Exception as e:
            logger.error(f"HuggingFace API error: {e}")
            raise
    
    async def close(self):
        """Clean up resources."""
        # Shutdown executor
        if self.executor:
            self.executor.shutdown(wait=False)
        self.client = None
