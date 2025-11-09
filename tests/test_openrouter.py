"""Tests for OpenRouter provider."""

import pytest
import asyncio
from openmux.providers.openrouter import OpenRouterProvider

@pytest.mark.asyncio
async def test_openrouter_initialization():
    provider = OpenRouterProvider()
    assert provider.name == "openrouter"
    assert await provider.supported_tasks() == []  # Empty when no connection

@pytest.mark.asyncio
async def test_openrouter_health_check():
    provider = OpenRouterProvider()
    health = await provider.health_check()
    assert "status" in health
    assert "timestamp" in health

@pytest.mark.asyncio
async def test_openrouter_capabilities():
    provider = OpenRouterProvider()
    capabilities = await provider.get_capabilities()
    assert isinstance(capabilities, dict)

@pytest.mark.asyncio
async def test_openrouter_availability():
    provider = OpenRouterProvider()
    is_available = await provider.is_available()
    assert isinstance(is_available, bool)

@pytest.mark.asyncio
async def test_openrouter_generation():
    provider = OpenRouterProvider()
    with pytest.raises(Exception):  # Should fail without API key
        await provider.generate("Test prompt")