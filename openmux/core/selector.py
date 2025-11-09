"""Model selector for choosing the best provider for a task."""

from typing import List, Optional, Dict, Any
import logging

from ..providers.base import BaseProvider
from ..classifier.task_types import TaskType


logger = logging.getLogger(__name__)


class ModelSelector:
    """Selects the most suitable model/provider for a given task."""
    
    def __init__(self, providers: List[BaseProvider]):
        """Initialize the selector with available providers.
        
        Args:
            providers: List of available provider instances
        """
        self.providers = providers
        logger.info(f"ModelSelector initialized with {len(providers)} providers")
    
    def select_single(
        self,
        task_type: TaskType,
        preferences: Optional[List[str]] = None
    ) -> Optional[BaseProvider]:
        """Select the best single provider for a task.
        
        Args:
            task_type: The type of task to perform
            preferences: Optional list of preferred provider names
            
        Returns:
            Best provider for the task, or None if no suitable provider found
        """
        logger.debug(f"Selecting provider for task: {task_type}")
        
        # Filter providers that support the task
        suitable_providers = [
            p for p in self.providers
            if p.supports_task(task_type)
        ]
        
        if not suitable_providers:
            logger.warning(f"No providers found for task type: {task_type}")
            return None
        
        # Apply preferences if specified
        if preferences:
            preferred = [p for p in suitable_providers if p.name in preferences]
            if preferred:
                suitable_providers = preferred
        
        # For MVP: simple selection - return first available provider
        # TODO: Implement ranking based on performance metrics
        selected = suitable_providers[0]
        logger.info(f"Selected provider: {selected.name} for task: {task_type}")
        
        return selected
    
    def select_multiple(
        self,
        task_type: TaskType,
        count: int = 2
    ) -> List[BaseProvider]:
        """Select multiple providers for a task.
        
        Args:
            task_type: The type of task to perform
            count: Number of providers to select
            
        Returns:
            List of providers for the task
        """
        logger.debug(f"Selecting {count} providers for task: {task_type}")
        
        # Filter providers that support the task
        suitable_providers = [
            p for p in self.providers
            if p.supports_task(task_type)
        ]
        
        # Return up to 'count' providers
        selected = suitable_providers[:count]
        logger.info(
            f"Selected {len(selected)} providers: "
            f"{[p.name for p in selected]} for task: {task_type}"
        )
        
        return selected
    
    def select_with_fallbacks(
        self,
        task_type: TaskType,
        max_fallbacks: int = 2,
        preferences: Optional[List[str]] = None
    ) -> List[BaseProvider]:
        """Select provider with fallback options.
        
        Returns primary provider plus fallback alternatives.
        
        Args:
            task_type: The type of task to perform
            max_fallbacks: Maximum number of fallback providers
            preferences: Optional list of preferred provider names
            
        Returns:
            List of providers (primary + fallbacks)
        """
        logger.debug(
            f"Selecting provider with {max_fallbacks} fallbacks for task: {task_type}"
        )
        
        # Filter providers that support the task
        suitable_providers = [
            p for p in self.providers
            if p.supports_task(task_type)
        ]
        
        if not suitable_providers:
            logger.warning(f"No providers found for task type: {task_type}")
            return []
        
        # Apply preferences if specified
        if preferences:
            preferred = [p for p in suitable_providers if p.name in preferences]
            non_preferred = [p for p in suitable_providers if p.name not in preferences]
            # Preferred providers first, then others
            suitable_providers = preferred + non_preferred
        
        # Return primary + up to max_fallbacks providers
        count = min(len(suitable_providers), max_fallbacks + 1)
        selected = suitable_providers[:count]
        
        logger.info(
            f"Selected {len(selected)} providers (1 primary + {len(selected)-1} fallbacks): "
            f"{[p.name for p in selected]} for task: {task_type}"
        )
        
        return selected
