"""Query router for sending requests to providers."""

import asyncio
import logging
from typing import List, Optional

from ..providers.base import BaseProvider


logger = logging.getLogger(__name__)


class Router:
    """Routes queries to providers with retry and timeout handling."""
    
    def __init__(self, timeout: float = 30.0, max_retries: int = 3):
        """Initialize the router.
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.timeout = timeout
        self.max_retries = max_retries
        logger.info(f"Router initialized (timeout={timeout}s, retries={max_retries})")
    
    async def route_single(
        self,
        provider: BaseProvider,
        query: str,
        **kwargs
    ) -> str:
        """Route a query to a single provider.
        
        Args:
            provider: Provider to use
            query: Query string
            **kwargs: Additional parameters for the provider
            
        Returns:
            Response from the provider
            
        Raises:
            Exception: If all retry attempts fail
        """
        logger.debug(f"Routing query to {provider.name}")
        
        for attempt in range(self.max_retries):
            try:
                response = await asyncio.wait_for(
                    provider.generate(query, **kwargs),
                    timeout=self.timeout
                )
                logger.info(f"Successfully received response from {provider.name}")
                return response
                
            except asyncio.TimeoutError:
                logger.warning(
                    f"Timeout on attempt {attempt + 1}/{self.max_retries} "
                    f"for provider {provider.name}"
                )
                if attempt == self.max_retries - 1:
                    raise
                    
            except Exception as e:
                logger.error(
                    f"Error on attempt {attempt + 1}/{self.max_retries} "
                    f"for provider {provider.name}: {e}"
                )
                if attempt == self.max_retries - 1:
                    raise
                    
            # Wait before retry (exponential backoff)
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt
                logger.debug(f"Waiting {wait_time}s before retry")
                await asyncio.sleep(wait_time)
        
        raise Exception(f"Failed to get response from {provider.name}")
    
    async def route_multiple(
        self,
        providers: List[BaseProvider],
        query: str,
        **kwargs
    ) -> List[str]:
        """Route a query to multiple providers in parallel.
        
        Args:
            providers: List of providers to use
            query: Query string
            **kwargs: Additional parameters for providers
            
        Returns:
            List of responses from providers
        """
        logger.debug(f"Routing query to {len(providers)} providers")
        
        tasks = [
            self.route_single(provider, query, **kwargs)
            for provider in providers
        ]
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log them
        valid_responses = []
        for provider, response in zip(providers, responses):
            if isinstance(response, Exception):
                logger.error(f"Error from {provider.name}: {response}")
            else:
                valid_responses.append(response)
        
        logger.info(
            f"Received {len(valid_responses)}/{len(providers)} valid responses"
        )
        
        return valid_responses
