"""
Unit tests for provider health checking.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
import asyncio

from openmux.providers.base import BaseProvider, ProviderHealth


class MockHealthyProvider(BaseProvider):
    """Mock provider that is always healthy."""
    
    def __init__(self):
        super().__init__("HealthyProvider")
        self._generate_func = AsyncMock(return_value="Test response")
    
    def is_available(self) -> bool:
        return True
    
    def supports_task(self, task_type) -> bool:
        return True
    
    async def generate(self, prompt: str, **kwargs) -> str:
        return await self._generate_func(prompt, **kwargs)


class MockUnhealthyProvider(BaseProvider):
    """Mock provider that always fails health checks."""
    
    def __init__(self):
        super().__init__("UnhealthyProvider")
        self._generate_func = AsyncMock(side_effect=Exception("Provider unavailable"))
    
    def is_available(self) -> bool:
        return True
    
    def supports_task(self, task_type) -> bool:
        return True
    
    async def generate(self, prompt: str, **kwargs) -> str:
        return await self._generate_func(prompt, **kwargs)


class MockSlowProvider(BaseProvider):
    """Mock provider that is slow to respond."""
    
    def __init__(self, delay: float = 10.0):
        super().__init__("SlowProvider")
        self.delay = delay
        
    def is_available(self) -> bool:
        return True
    
    def supports_task(self, task_type) -> bool:
        return True
    
    async def generate(self, prompt: str, **kwargs) -> str:
        await asyncio.sleep(self.delay)
        return "Slow response"


class TestProviderHealth:
    """Test ProviderHealth class."""
    
    def test_initial_health_state(self):
        """Test initial health state."""
        health = ProviderHealth()
        
        assert health.is_healthy is True
        assert health.last_check == 0.0
        assert health.response_time == 0.0
        assert health.error_count == 0
        assert health.success_count == 0
        assert health.last_error is None
    
    def test_success_rate_no_attempts(self):
        """Test success rate with no attempts."""
        health = ProviderHealth()
        assert health.success_rate == 1.0
    
    def test_success_rate_all_success(self):
        """Test success rate with all successes."""
        health = ProviderHealth()
        health.success_count = 10
        health.error_count = 0
        assert health.success_rate == 1.0
    
    def test_success_rate_mixed(self):
        """Test success rate with mixed results."""
        health = ProviderHealth()
        health.success_count = 7
        health.error_count = 3
        assert health.success_rate == 0.7
    
    def test_success_rate_all_failures(self):
        """Test success rate with all failures."""
        health = ProviderHealth()
        health.success_count = 0
        health.error_count = 5
        assert health.success_rate == 0.0


class TestHealthCheck:
    """Test health check functionality."""
    
    @pytest.mark.asyncio
    async def test_healthy_provider_passes_check(self):
        """Test that a healthy provider passes health check."""
        provider = MockHealthyProvider()
        
        is_healthy = await provider.health_check(timeout=5.0)
        
        assert is_healthy is True
        assert provider.health.is_healthy is True
        assert provider.health.success_count == 1
        assert provider.health.error_count == 0
        assert provider.health.last_error is None
        assert provider.health.response_time > 0
    
    @pytest.mark.asyncio
    async def test_unhealthy_provider_fails_check(self):
        """Test that an unhealthy provider fails health check."""
        provider = MockUnhealthyProvider()
        
        is_healthy = await provider.health_check(timeout=5.0)
        
        assert is_healthy is False
        assert provider.health.is_healthy is False
        assert provider.health.success_count == 0
        assert provider.health.error_count == 1
        assert provider.health.last_error is not None
        assert "Provider unavailable" in provider.health.last_error
    
    @pytest.mark.asyncio
    async def test_slow_provider_timeout(self):
        """Test that a slow provider times out."""
        provider = MockSlowProvider(delay=10.0)
        
        is_healthy = await provider.health_check(timeout=1.0)
        
        assert is_healthy is False
        assert provider.health.is_healthy is False
        assert provider.health.error_count == 1
        assert provider.health.last_error is not None
        assert "timeout" in provider.health.last_error.lower()
    
    @pytest.mark.asyncio
    async def test_multiple_health_checks(self):
        """Test multiple health checks update metrics correctly."""
        provider = MockHealthyProvider()
        
        # First check
        await provider.health_check()
        assert provider.health.success_count == 1
        
        # Second check
        await provider.health_check()
        assert provider.health.success_count == 2
        
        # Third check
        await provider.health_check()
        assert provider.health.success_count == 3
        assert provider.health.error_count == 0
    
    @pytest.mark.asyncio
    async def test_health_check_after_failure_recovery(self):
        """Test health check after provider recovers from failure."""
        provider = MockUnhealthyProvider()
        
        # First check - fails
        is_healthy = await provider.health_check()
        assert is_healthy is False
        assert provider.health.error_count == 1
        
        # Provider recovers
        provider._generate_func = AsyncMock(return_value="Recovered")
        
        # Second check - succeeds
        is_healthy = await provider.health_check()
        assert is_healthy is True
        assert provider.health.is_healthy is True
        assert provider.health.success_count == 1
        assert provider.health.error_count == 1
    
    @pytest.mark.asyncio
    async def test_health_check_updates_last_check_time(self):
        """Test that health check updates last_check timestamp."""
        provider = MockHealthyProvider()
        
        initial_time = provider.health.last_check
        assert initial_time == 0.0
        
        await provider.health_check()
        
        assert provider.health.last_check > initial_time
        assert provider.health.last_check > 0
    
    @pytest.mark.asyncio
    async def test_health_check_custom_timeout(self):
        """Test health check with custom timeout."""
        provider = MockSlowProvider(delay=3.0)
        
        # Should timeout with 1s
        is_healthy = await provider.health_check(timeout=1.0)
        assert is_healthy is False
        
        # Should succeed with 5s timeout
        is_healthy = await provider.health_check(timeout=5.0)
        assert is_healthy is True


class TestProviderHealthMetrics:
    """Test health metrics tracking."""
    
    @pytest.mark.asyncio
    async def test_success_rate_calculation(self):
        """Test success rate is calculated correctly over time."""
        provider = MockHealthyProvider()
        
        # 3 successes
        for _ in range(3):
            await provider.health_check()
        
        assert provider.health.success_rate == 1.0
        
        # Make provider fail
        provider._generate_func = AsyncMock(side_effect=Exception("Error"))
        
        # 2 failures
        for _ in range(2):
            await provider.health_check()
        
        # Success rate should be 3/5 = 0.6
        assert provider.health.success_rate == 0.6
    
    @pytest.mark.asyncio
    async def test_response_time_tracking(self):
        """Test that response time is tracked."""
        provider = MockHealthyProvider()
        
        await provider.health_check()
        
        # Response time should be positive
        assert provider.health.response_time > 0
        # Should be reasonably fast (< 1 second for mock)
        assert provider.health.response_time < 1.0
    
    @pytest.mark.asyncio
    async def test_error_message_tracking(self):
        """Test that error messages are tracked."""
        provider = MockUnhealthyProvider()
        
        await provider.health_check()
        
        assert provider.health.last_error is not None
        assert len(provider.health.last_error) > 0
        assert "Provider unavailable" in provider.health.last_error
