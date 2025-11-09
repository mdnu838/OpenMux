"""
Integration test for OpenRouter provider with real API.
"""

import os
import pytest
from dotenv import load_dotenv

from openmux.providers.openrouter import OpenRouterProvider
from openmux.classifier.task_types import TaskType


# Load environment variables
load_dotenv()


@pytest.fixture
def openrouter():
    """Create OpenRouter provider instance."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        pytest.skip("OPENROUTER_API_KEY not set")
    return OpenRouterProvider(api_key=api_key)


@pytest.mark.asyncio
async def test_openrouter_simple_query(openrouter):
    """Test simple query to OpenRouter."""
    query = "Say 'Hello from OpenCascade!' in exactly those words."
    
    response = await openrouter.generate(query, task_type=TaskType.CHAT)
    
    assert response is not None
    assert len(response) > 0
    print(f"\n✅ OpenRouter Response: {response[:200]}...")


@pytest.mark.asyncio
async def test_openrouter_code_query(openrouter):
    """Test code generation with OpenRouter."""
    query = "Write a Python function that adds two numbers. Just the code, no explanation."
    
    response = await openrouter.generate(query, task_type=TaskType.CODE)
    
    assert response is not None
    assert "def" in response.lower() or "function" in response.lower()
    print(f"\n✅ OpenRouter Code Response:\n{response[:300]}...")


@pytest.mark.asyncio
async def test_openrouter_with_parameters(openrouter):
    """Test OpenRouter with custom parameters."""
    query = "Count from 1 to 5."
    
    response = await openrouter.generate(
        query,
        task_type=TaskType.CHAT,
        temperature=0.3,
        max_tokens=100
    )
    
    assert response is not None
    print(f"\n✅ OpenRouter with params: {response[:200]}...")


@pytest.mark.asyncio
async def test_openrouter_availability(openrouter):
    """Test OpenRouter availability check."""
    is_available = openrouter.is_available()
    
    assert is_available is True
    print("\n✅ OpenRouter is available")


@pytest.mark.asyncio
async def test_openrouter_supports_tasks(openrouter):
    """Test task support checking."""
    assert openrouter.supports_task(TaskType.CHAT)
    assert openrouter.supports_task(TaskType.CODE)
    print("\n✅ OpenRouter supports CHAT and CODE tasks")


if __name__ == "__main__":
    # Run tests with: pytest tests/integration/test_openrouter_live.py -v -s
    pytest.main([__file__, "-v", "-s"])
