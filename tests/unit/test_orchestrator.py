"""
Unit tests for Orchestrator class.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from openmux.core.orchestrator import Orchestrator
from openmux.classifier.task_types import TaskType


@pytest.fixture
def orchestrator():
    """Create orchestrator instance for testing."""
    return Orchestrator()


@pytest.mark.asyncio
async def test_orchestrator_initialization(orchestrator):
    """Test orchestrator initializes correctly."""
    assert orchestrator is not None
    assert orchestrator.config is not None
    assert orchestrator.registry is not None
    assert orchestrator.router is not None
    assert orchestrator.combiner is not None


@pytest.mark.asyncio
async def test_process_simple_query(orchestrator):
    """Test processing a simple query."""
    # Mock provider
    mock_provider = MagicMock()
    mock_provider.name = "MockProvider"
    mock_provider.supports_task.return_value = True
    mock_provider.generate = AsyncMock(return_value="Test response")
    
    # Mock selector to return list of providers (for failover)
    with patch.object(orchestrator, '_initialize_selector'):
        orchestrator.selector = MagicMock()
        orchestrator.selector.select_with_fallbacks.return_value = [mock_provider]
        
        # Mock router failover
        with patch.object(
            orchestrator.router, 
            'route_with_failover', 
            new=AsyncMock(return_value=("Test response", "MockProvider"))
        ):
            result = await orchestrator._process_async("What is Python?")
            
            assert result == "Test response"


@pytest.mark.asyncio
async def test_process_with_task_type(orchestrator):
    """Test processing with explicit task type."""
    mock_provider = MagicMock()
    mock_provider.name = "MockProvider"
    mock_provider.supports_task.return_value = True
    mock_provider.generate = AsyncMock(return_value="Code response")
    
    with patch.object(orchestrator, '_initialize_selector'):
        orchestrator.selector = MagicMock()
        orchestrator.selector.select_with_fallbacks.return_value = [mock_provider]
        
        with patch.object(
            orchestrator.router,
            'route_with_failover',
            new=AsyncMock(return_value=("Code response", "MockProvider"))
        ):
            result = await orchestrator._process_async(
                "Write a function",
                task_type=TaskType.CODE
            )
            
            assert result == "Code response"


@pytest.mark.asyncio
async def test_process_multi(orchestrator):
    """Test multi-model processing."""
    mock_provider1 = MagicMock()
    mock_provider1.name = "Provider1"
    mock_provider1.generate = AsyncMock(return_value="Response 1")
    
    mock_provider2 = MagicMock()
    mock_provider2.name = "Provider2"
    mock_provider2.generate = AsyncMock(return_value="Response 2")
    
    with patch.object(orchestrator, '_initialize_selector'):
        orchestrator.selector = MagicMock()
        orchestrator.selector.select_multiple.return_value = [mock_provider1, mock_provider2]
        
        with patch.object(orchestrator.router, 'route_multiple', new=AsyncMock(return_value=["Response 1", "Response 2"])):
            with patch.object(orchestrator.combiner, 'merge', return_value="Combined response"):
                result = await orchestrator._process_multi_async(
                    "Test query",
                    num_models=2,
                    combination_method="merge"
                )
                
                assert result == "Combined response"


@pytest.mark.asyncio
async def test_fallback_handling(orchestrator):
    """Test fallback mechanism when primary provider fails."""
    mock_provider = MagicMock()
    mock_provider.name = "FailingProvider"
    mock_provider.generate = AsyncMock(side_effect=Exception("Provider failed"))
    
    mock_fallback = MagicMock()
    mock_fallback.has_fallback.return_value = True
    mock_fallback.fallback = AsyncMock(return_value="Fallback response")
    
    with patch.object(orchestrator, '_initialize_selector'):
        orchestrator.selector = MagicMock()
        orchestrator.selector.select_single.return_value = mock_provider
        
        with patch.object(orchestrator, '_initialize_fallback'):
            orchestrator.fallback = mock_fallback
            
            with patch.object(orchestrator.router, 'route_single', new=AsyncMock(side_effect=Exception("Provider failed"))):
                result = await orchestrator._process_async("Test query", fallback_enabled=True)
                
                assert result == "Fallback response"


@pytest.mark.asyncio
async def test_no_provider_available(orchestrator):
    """Test error handling when no provider is available."""
    from openmux.utils.exceptions import NoProvidersAvailableError
    
    with patch.object(orchestrator, '_initialize_selector'):
        orchestrator.selector = MagicMock()
        orchestrator.selector.select_with_fallbacks.return_value = []
        orchestrator._initialize_fallback()
        orchestrator.fallback = None  # Disable fallback for this test
        
        with pytest.raises(NoProvidersAvailableError, match="No providers available"):
            await orchestrator._process_async("Test query")
