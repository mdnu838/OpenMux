"""Query router for sending requests to providers."""

import asyncio
import logging
from typing import List, Optional, Tuple

from ..providers.base import BaseProvider
from ..utils.exceptions import ProviderError, FailoverError, TimeoutError as OpenMuxTimeoutError


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
                    raise OpenMuxTimeoutError(
                        f"Request to {provider.name}",
                        self.timeout
                    )
                    
            except Exception as e:
                logger.error(
                    f"Error on attempt {attempt + 1}/{self.max_retries} "
                    f"for provider {provider.name}: {e}"
                )
                if attempt == self.max_retries - 1:
                    if isinstance(e, ProviderError):
                        raise
                    raise ProviderError(provider.name, str(e))
                    
            # Wait before retry (exponential backoff)
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt
                logger.debug(f"Waiting {wait_time}s before retry")
                await asyncio.sleep(wait_time)
        
        # Should never reach here, but just in case
        raise ProviderError(provider.name, "All retry attempts exhausted")
    
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
    
    async def route_with_failover(
        self,
        providers: List[BaseProvider],
        query: str,
        **kwargs
    ) -> Tuple[str, str]:
        """Route query to providers with automatic failover.
        
        Tries providers in sequence until one succeeds. Uses exponential
        backoff between provider switches.
        
        Args:
            providers: List of providers to try (in order)
            query: Query string
            **kwargs: Additional parameters for providers
            
        Returns:
            Tuple of (response, provider_name) on success
            
        Raises:
            Exception: If all providers fail
        """
        logger.info(f"Attempting failover across {len(providers)} providers")
        
        last_error = None
        
        for idx, provider in enumerate(providers):
            try:
                logger.info(f"Trying provider {idx + 1}/{len(providers)}: {provider.name}")
                
                # Try this provider with retries
                response = await self.route_single(provider, query, **kwargs)
                
                logger.info(f"✓ Success with provider: {provider.name}")
                return response, provider.name
                
            except Exception as e:
                last_error = e
                logger.warning(
                    f"✗ Provider {provider.name} failed: {str(e)[:100]}"
                )
                
                # Wait before trying next provider (exponential backoff)
                if idx < len(providers) - 1:
                    wait_time = 2 ** idx
                    logger.debug(f"Waiting {wait_time}s before trying next provider")
                    await asyncio.sleep(wait_time)
        
        # All providers failed
        provider_names = [p.name for p in providers]
        logger.error(f"All {len(providers)} providers failed")
        raise FailoverError(provider_names, last_error)
