"""
OpenCascade - Main orchestration engine for free GenAI model selection and routing.
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any

from pydantic import BaseModel

from ..classifier.task_types import TaskType
from ..providers.base import BaseProvider
from ..providers.registry import ProviderRegistry
from ..utils.config import Config
from ..utils.logging import setup_logger
from ..utils.exceptions import NoProvidersAvailableError
from .selector import ModelSelector
from .router import Router
from .combiner import Combiner
from .fallback import FallbackHandler


logger = setup_logger(__name__)


class ProcessConfig(BaseModel):
    """Configuration for processing requests."""
    task_type: Optional[TaskType] = None
    provider_preference: Optional[List[str]] = None
    timeout: float = 30.0
    max_retries: int = 3
    fallback_enabled: bool = True


class Orchestrator:
    """Main orchestration engine for OpenCascade."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the orchestrator with configuration.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config = Config(config_path) if config_path else Config()
        self.logger = logger
        
        # Initialize components
        self.registry = ProviderRegistry()
        self.selector: Optional[ModelSelector] = None
        self.router = Router()
        self.combiner = Combiner()
        self.fallback: Optional[FallbackHandler] = None
        
        logger.info("Orchestrator initialized")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources."""
        self.cleanup()
        return False
    
    def cleanup(self):
        """Cleanup resources (close provider sessions)."""
        # Close all provider sessions
        for provider in self.registry.get_all_available():
            if hasattr(provider, '_session') and provider._session:
                try:
                    asyncio.run(provider._session.close())
                except Exception as e:
                    logger.warning(f"Error closing provider session: {e}")
    
    def _initialize_selector(self):
        """Initialize model selector with available providers."""
        if self.selector is None:
            providers = self.registry.get_all_available()
            self.selector = ModelSelector(providers)
    
    def _initialize_fallback(self):
        """Initialize fallback handler if Ollama is available."""
        if self.fallback is None:
            ollama = self.registry.get("ollama")
            self.fallback = FallbackHandler(ollama)
    
    def process(
        self,
        query: str,
        task_type: Optional[TaskType] = None,
        **kwargs
    ) -> str:
        """Process a query using the most suitable model.
        
        Args:
            query: The input query to process
            task_type: Optional task type override
            **kwargs: Additional configuration options
        
        Returns:
            str: The processed response
        """
        return asyncio.run(self._process_async(query, task_type, **kwargs))
    
    async def _process_async(
        self,
        query: str,
        task_type: Optional[TaskType] = None,
        **kwargs
    ) -> str:
        """Internal async processing implementation.
        
        Args:
            query: Input query
            task_type: Optional task type
            **kwargs: Additional parameters
            
        Returns:
            Processed response
        """
        self._initialize_selector()
        self._initialize_fallback()
        
        # Use provided task type or default to CHAT
        if task_type is None:
            task_type = TaskType.CHAT
            logger.info(f"No task type specified, defaulting to {task_type}")
        
        try:
            # Check if failover is enabled (default: True)
            enable_failover = kwargs.get('enable_failover', True)
            
            if enable_failover:
                # Get primary + fallback providers
                providers = self.selector.select_with_fallbacks(
                    task_type,
                    max_fallbacks=kwargs.get('max_fallbacks', 2),
                    preferences=kwargs.get('provider_preference')
                )
                
                if not providers:
                    available = [p.name for p in self.registry.get_all_available()]
                    raise NoProvidersAvailableError(
                        task_type=str(task_type),
                        available_providers=available
                    )
                
                # Try providers with automatic failover
                response, provider_name = await self.router.route_with_failover(
                    providers, query, **kwargs
                )
                logger.info(f"Query processed successfully by {provider_name}")
                return response
            else:
                # Original single-provider logic
                provider = self.selector.select_single(task_type)
                
                if provider is None:
                    available = [p.name for p in self.registry.get_all_available()]
                    raise NoProvidersAvailableError(
                        task_type=str(task_type),
                        available_providers=available
                    )
                
                # Route query to provider
                response = await self.router.route_single(provider, query, **kwargs)
                
                return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            
            # Try fallback if enabled
            if kwargs.get('fallback_enabled', True) and self.fallback.has_fallback():
                logger.info("Attempting fallback")
                try:
                    return await self.fallback.fallback(query, **kwargs)
                except Exception as fallback_error:
                    logger.error(f"Fallback failed: {fallback_error}")
            
            raise
    
    def process_multi(
        self,
        query: str,
        num_models: int = 2,
        combination_method: str = "merge",
        task_type: Optional[TaskType] = None,
        **kwargs
    ) -> str:
        """Process a query using multiple models and combine their responses.
        
        Args:
            query: The input query to process
            num_models: Number of models to use
            combination_method: Method to combine responses ("merge" or "summarize")
            task_type: Optional task type override
            **kwargs: Additional configuration options
        
        Returns:
            str: The combined response
        """
        return asyncio.run(
            self._process_multi_async(
                query,
                num_models,
                combination_method,
                task_type,
                **kwargs
            )
        )
    
    async def _process_multi_async(
        self,
        query: str,
        num_models: int,
        combination_method: str,
        task_type: Optional[TaskType] = None,
        **kwargs
    ) -> str:
        """Internal async multi-processing implementation.
        
        Args:
            query: Input query
            num_models: Number of models
            combination_method: Combination method
            task_type: Optional task type
            **kwargs: Additional parameters
            
        Returns:
            Combined response
        """
        self._initialize_selector()
        
        # Use provided task type or default to CHAT
        if task_type is None:
            task_type = TaskType.CHAT
        
        # Select multiple providers
        providers = self.selector.select_multiple(task_type, num_models)
        
        if not providers:
            available = [p.name for p in self.registry.get_all_available()]
            raise NoProvidersAvailableError(
                task_type=str(task_type),
                available_providers=available
            )
        
        # Route to multiple providers
        responses = await self.router.route_multiple(providers, query, **kwargs)
        
        if not responses:
            raise NoProvidersAvailableError(
                task_type=str(task_type),
                available_providers=[p.name for p in providers]
            )
        
        # Combine responses
        if combination_method == "summarize":
            return self.combiner.summarize(responses)
        else:
            return self.combiner.merge(responses)