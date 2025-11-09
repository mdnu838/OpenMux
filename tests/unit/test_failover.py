"""
Unit tests for failover and retry logic.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio

from openmux.core.router import Router
from openmux.core.selector import ModelSelector
from openmux.classifier.task_types import TaskType


@pytest.fixture
def router():
    """Create router instance for testing."""
    return Router(timeout=5.0, max_retries=3)


@pytest.fixture
def mock_providers():
    """Create mock providers for testing."""
    provider1 = MagicMock()
    provider1.name = "Provider1"
    provider1.supports_task.return_value = True
    provider1.generate = AsyncMock(side_effect=Exception("Provider1 failed"))
    
    provider2 = MagicMock()
    provider2.name = "Provider2"
    provider2.supports_task.return_value = True
    provider2.generate = AsyncMock(return_value="Response from Provider2")
    
    provider3 = MagicMock()
    provider3.name = "Provider3"
    provider3.supports_task.return_value = True
    provider3.generate = AsyncMock(return_value="Response from Provider3")
    
    return [provider1, provider2, provider3]


class TestRouterFailover:
    """Test router failover functionality."""
    
    @pytest.mark.asyncio
    async def test_route_with_failover_success_on_second_provider(
        self, router, mock_providers
    ):
        """Test failover succeeds on second provider."""
        response, provider_name = await router.route_with_failover(
            mock_providers,
            "Test query"
        )
        
        assert response == "Response from Provider2"
        assert provider_name == "Provider2"
        
        # Verify Provider1 was tried (with retries, so 3 times)
        assert mock_providers[0].generate.call_count == 3
        # Verify Provider2 was tried (succeeded on first try)
        mock_providers[1].generate.assert_called_once()
        # Verify Provider3 was NOT tried (failover stopped at Provider2)
        mock_providers[2].generate.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_route_with_failover_all_providers_fail(self, router):
        """Test failover when all providers fail."""
        failing_provider1 = MagicMock()
        failing_provider1.name = "FailProvider1"
        failing_provider1.generate = AsyncMock(side_effect=Exception("Failed 1"))
        
        failing_provider2 = MagicMock()
        failing_provider2.name = "FailProvider2"
        failing_provider2.generate = AsyncMock(side_effect=Exception("Failed 2"))
        
        providers = [failing_provider1, failing_provider2]
        
        with pytest.raises(Exception, match="All 2 providers failed"):
            await router.route_with_failover(providers, "Test query")
        
        # Verify both providers were tried
        failing_provider1.generate.assert_called()
        failing_provider2.generate.assert_called()
    
    @pytest.mark.asyncio
    async def test_route_with_failover_first_provider_succeeds(self, router):
        """Test failover when first provider succeeds."""
        working_provider = MagicMock()
        working_provider.name = "WorkingProvider"
        working_provider.generate = AsyncMock(return_value="Success")
        
        backup_provider = MagicMock()
        backup_provider.name = "BackupProvider"
        backup_provider.generate = AsyncMock(return_value="Backup response")
        
        providers = [working_provider, backup_provider]
        
        response, provider_name = await router.route_with_failover(
            providers,
            "Test query"
        )
        
        assert response == "Success"
        assert provider_name == "WorkingProvider"
        
        # Backup provider should NOT be called
        backup_provider.generate.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_route_single_retries_with_exponential_backoff(self, router):
        """Test single route retries with exponential backoff."""
        provider = MagicMock()
        provider.name = "FlakeyProvider"
        
        # Fail twice, then succeed
        provider.generate = AsyncMock(
            side_effect=[
                Exception("Fail 1"),
                Exception("Fail 2"),
                "Success on third try"
            ]
        )
        
        response = await router.route_single(provider, "Test query")
        
        assert response == "Success on third try"
        assert provider.generate.call_count == 3


class TestSelectorFailover:
    """Test selector failover provider selection."""
    
    def test_select_with_fallbacks_returns_multiple_providers(self):
        """Test select_with_fallbacks returns primary + fallbacks."""
        provider1 = MagicMock()
        provider1.name = "Provider1"
        provider1.supports_task.return_value = True
        
        provider2 = MagicMock()
        provider2.name = "Provider2"
        provider2.supports_task.return_value = True
        
        provider3 = MagicMock()
        provider3.name = "Provider3"
        provider3.supports_task.return_value = True
        
        selector = ModelSelector([provider1, provider2, provider3])
        
        providers = selector.select_with_fallbacks(
            TaskType.CHAT,
            max_fallbacks=2
        )
        
        assert len(providers) == 3  # 1 primary + 2 fallbacks
        assert providers[0].name == "Provider1"
        assert providers[1].name == "Provider2"
        assert providers[2].name == "Provider3"
    
    def test_select_with_fallbacks_respects_max_fallbacks(self):
        """Test max_fallbacks parameter is respected."""
        providers_list = []
        for i in range(5):
            provider = MagicMock()
            provider.name = f"Provider{i}"
            provider.supports_task.return_value = True
            providers_list.append(provider)
        
        selector = ModelSelector(providers_list)
        
        selected = selector.select_with_fallbacks(
            TaskType.CHAT,
            max_fallbacks=1  # Only 1 fallback
        )
        
        assert len(selected) == 2  # 1 primary + 1 fallback
    
    def test_select_with_fallbacks_handles_preferences(self):
        """Test preferences are prioritized in fallback selection."""
        provider1 = MagicMock()
        provider1.name = "OpenRouter"
        provider1.supports_task.return_value = True
        
        provider2 = MagicMock()
        provider2.name = "HuggingFace"
        provider2.supports_task.return_value = True
        
        provider3 = MagicMock()
        provider3.name = "Ollama"
        provider3.supports_task.return_value = True
        
        selector = ModelSelector([provider1, provider2, provider3])
        
        selected = selector.select_with_fallbacks(
            TaskType.CHAT,
            max_fallbacks=2,
            preferences=["HuggingFace", "OpenRouter"]
        )
        
        # Preferred providers should come first (in preference order)
        preferred_names = {selected[0].name, selected[1].name}
        assert "HuggingFace" in preferred_names
        assert "OpenRouter" in preferred_names
        # Non-preferred should be last
        assert selected[2].name == "Ollama"
    
    def test_select_with_fallbacks_no_suitable_providers(self):
        """Test returns empty list when no providers support task."""
        provider = MagicMock()
        provider.name = "UnsupportedProvider"
        provider.supports_task.return_value = False
        
        selector = ModelSelector([provider])
        
        selected = selector.select_with_fallbacks(TaskType.CHAT, max_fallbacks=2)
        
        assert len(selected) == 0


class TestRetryLogic:
    """Test retry logic with exponential backoff."""
    
    @pytest.mark.asyncio
    async def test_exponential_backoff_timing(self, router):
        """Test exponential backoff wait times."""
        provider = MagicMock()
        provider.name = "SlowProvider"
        provider.generate = AsyncMock(side_effect=Exception("Always fails"))
        
        start_time = asyncio.get_event_loop().time()
        
        with pytest.raises(Exception):
            await router.route_single(provider, "Test query")
        
        end_time = asyncio.get_event_loop().time()
        elapsed = end_time - start_time
        
        # Should wait: 0s (1st try) + 1s + 2s = ~3s minimum
        # (2^0 + 2^1 = 3 seconds of waiting)
        assert elapsed >= 3.0
        assert elapsed < 5.0  # Should not be too long
    
    @pytest.mark.asyncio
    async def test_timeout_error_retries(self, router):
        """Test timeout errors trigger retries."""
        provider = MagicMock()
        provider.name = "TimeoutProvider"
        
        # Timeout twice, then succeed
        provider.generate = AsyncMock(
            side_effect=[
                asyncio.TimeoutError(),
                asyncio.TimeoutError(),
                "Success after timeouts"
            ]
        )
        
        response = await router.route_single(provider, "Test query")
        
        assert response == "Success after timeouts"
        assert provider.generate.call_count == 3
