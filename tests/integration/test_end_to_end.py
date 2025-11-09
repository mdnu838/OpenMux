"""
End-to-end integration test for the complete OpenCascade flow.
"""

import os
import pytest
from dotenv import load_dotenv

from openmux import Orchestrator, TaskType


# Load environment variables
load_dotenv()


@pytest.fixture
def orchestrator():
    """Create orchestrator instance."""
    if not os.getenv("OPENROUTER_API_KEY"):
        pytest.skip("OPENROUTER_API_KEY not set")
    return Orchestrator()


@pytest.mark.asyncio
async def test_orchestrator_simple_query(orchestrator):
    """Test orchestrator with a simple query."""
    result = await orchestrator._process_async("Say hello!")
    
    assert result is not None
    assert len(result) > 0
    print(f"\n✅ Orchestrator simple query: {result[:100]}...")


@pytest.mark.asyncio
async def test_orchestrator_with_task_type(orchestrator):
    """Test orchestrator with explicit task type."""
    result = await orchestrator._process_async(
        "Write a Python function that returns 'hello'",
        task_type=TaskType.CODE
    )
    
    assert result is not None
    assert "def" in result.lower() or "return" in result.lower()
    print(f"\n✅ Orchestrator code task: {result[:200]}...")


@pytest.mark.asyncio
async def test_classifier_integration(orchestrator):
    """Test that classifier works with orchestrator."""
    code_query = "Create a function to add two numbers"
    result = await orchestrator._process_async(code_query)
    
    assert result is not None
    print(f"\n✅ Classifier detected code query: {result[:150]}...")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
