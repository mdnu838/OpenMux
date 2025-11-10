"""Tests for OpenRouter provider."""

import pytest
from unittest.mock import patch
from openmux.providers.openrouter import OpenRouterProvider
from openmux.classifier.task_types import TaskType


def test_openrouter_initialization():
    """Test OpenRouter provider initialization."""
    provider = OpenRouterProvider()
    assert provider.name == "OpenRouter"  # Capital O and R
    assert provider.base_url == "https://openrouter.ai/api/v1"


@patch.dict('os.environ', {}, clear=True)
def test_openrouter_availability_without_key():
    """Test availability check without API key."""
    provider = OpenRouterProvider(api_key=None)
    assert provider.is_available() is False


def test_openrouter_availability_with_key():
    """Test availability check with API key."""
    provider = OpenRouterProvider(api_key="test-key")
    assert provider.is_available() is True


def test_openrouter_task_support():
    """Test task type support."""
    provider = OpenRouterProvider()
    assert provider.supports_task(TaskType.CHAT) is True
    assert provider.supports_task(TaskType.CODE) is True
    assert provider.supports_task(TaskType.EMBEDDINGS) is False


@pytest.mark.asyncio
async def test_openrouter_generation_without_key():
    """Test that generation fails without API key."""
    with patch.dict('os.environ', {}, clear=True):
        provider = OpenRouterProvider(api_key=None)
        with pytest.raises(Exception):  # Should raise ConfigurationError
            await provider.generate("test query")