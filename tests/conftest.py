"""
Shared test fixtures and configuration for pytest.
"""

import pytest
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        "timeout": 30.0,
        "max_retries": 3,
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 512
    }
