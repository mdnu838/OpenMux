"""
Integration tests for HuggingFace provider with real API.

⚠️  IMPORTANT: HuggingFace Inference API has changed!
Old endpoint (deprecated): https://api-inference.huggingface.co
New endpoint: https://router.huggingface.co/hf-inference
Status: Endpoint migration in progress - tests currently failing with HTTP 410

These tests require HF_TOKEN to be set in .env file.
Get your token from: https://huggingface.co/settings/tokens

TODO: Update provider to new API format once documentation is available
"""

import os
import pytest
from dotenv import load_dotenv

from openmux.providers.huggingface import HuggingFaceProvider
from openmux.classifier.task_types import TaskType


# Load environment variables
load_dotenv()

# Skip all tests in this module until HuggingFace API migration is complete
pytestmark = pytest.mark.skip(
    reason="HuggingFace migrated to new API endpoint (router.huggingface.co). "
           "Awaiting official documentation. See: HTTP 410 from api-inference.huggingface.co"
)


@pytest.fixture
def huggingface():
    """Create HuggingFace provider instance."""
    api_token = os.getenv("HF_TOKEN")
    if not api_token:
        pytest.skip("HF_TOKEN not set in .env")
    return HuggingFaceProvider(api_token=api_token)


@pytest.mark.asyncio
async def test_huggingface_chat_generation(huggingface):
    """Test chat generation with HuggingFace."""
    query = "What is Python? Answer in one sentence."
    
    response = await huggingface.generate(query, task_type=TaskType.CHAT)
    
    assert response is not None
    assert len(response) > 0
    assert isinstance(response, str)
    print(f"\n✅ HuggingFace Chat Response: {response[:200]}...")


@pytest.mark.asyncio
async def test_huggingface_code_generation(huggingface):
    """Test code generation with HuggingFace."""
    query = "Write a Python function to calculate factorial. Just code, no explanation."
    
    response = await huggingface.generate(query, task_type=TaskType.CODE)
    
    assert response is not None
    assert len(response) > 0
    # Check for code-like content
    assert any(keyword in response.lower() for keyword in ["def", "return", "function"])
    print(f"\n✅ HuggingFace Code Response: {response[:200]}...")


@pytest.mark.asyncio
async def test_huggingface_embeddings(huggingface):
    """Test embeddings generation with HuggingFace."""
    query = "This is a test sentence for embeddings."
    
    response = await huggingface.generate(query, task_type=TaskType.EMBEDDINGS)
    
    assert response is not None
    assert len(response) > 0
    # Embeddings should be a list-like string representation
    assert "[" in response or "embedding" in response.lower()
    print(f"\n✅ HuggingFace Embeddings Response: {response[:200]}...")


@pytest.mark.asyncio
async def test_huggingface_custom_model(huggingface):
    """Test with a custom model."""
    # Use a small, fast model for testing
    custom_provider = HuggingFaceProvider(
        api_token=os.getenv("HF_TOKEN"),
        model_id="gpt2"  # Small, fast model
    )
    
    query = "Hello"
    response = await custom_provider.generate(query, task_type=TaskType.CHAT)
    
    assert response is not None
    assert len(response) > 0
    print(f"\n✅ HuggingFace Custom Model (gpt2) Response: {response[:200]}...")


@pytest.mark.asyncio
async def test_huggingface_custom_parameters(huggingface):
    """Test generation with custom parameters."""
    query = "Count from 1 to 3."
    
    response = await huggingface.generate(
        query,
        task_type=TaskType.CHAT,
        max_new_tokens=50,
        temperature=0.7,
        top_p=0.9
    )
    
    assert response is not None
    assert len(response) > 0
    print(f"\n✅ HuggingFace Custom Parameters Response: {response[:200]}...")


@pytest.mark.asyncio
async def test_huggingface_error_invalid_token():
    """Test error handling with invalid token."""
    invalid_provider = HuggingFaceProvider(api_token="invalid_token_12345")
    
    with pytest.raises(Exception):  # Should raise an error
        await invalid_provider.generate("Test query", task_type=TaskType.CHAT)


@pytest.mark.asyncio
async def test_huggingface_session_cleanup(huggingface):
    """Test that session cleanup works properly."""
    # Generate a response
    await huggingface.generate("Test", task_type=TaskType.CHAT)
    
    # Close the provider
    await huggingface.close()
    
    # Session should be closed
    assert huggingface._session is None or huggingface._session.closed


@pytest.mark.asyncio
async def test_huggingface_context_manager():
    """Test using provider as async context manager."""
    api_token = os.getenv("HF_TOKEN")
    if not api_token:
        pytest.skip("HF_TOKEN not set")
    
    async with HuggingFaceProvider(api_token=api_token) as provider:
        response = await provider.generate("Hi", task_type=TaskType.CHAT)
        assert response is not None
    
    # Session should be auto-closed after context


@pytest.mark.asyncio
async def test_huggingface_empty_query(huggingface):
    """Test handling of empty query."""
    response = await huggingface.generate("", task_type=TaskType.CHAT)
    
    # Should handle empty query gracefully (might return empty or default response)
    assert response is not None


@pytest.mark.asyncio
async def test_huggingface_long_query(huggingface):
    """Test with a reasonably long query."""
    query = " ".join(["This is sentence number {}.".format(i) for i in range(20)])
    
    response = await huggingface.generate(query, task_type=TaskType.CHAT)
    
    assert response is not None
    assert len(response) > 0
    print(f"\n✅ HuggingFace Long Query Response Length: {len(response)}")


@pytest.mark.asyncio
async def test_huggingface_special_characters(huggingface):
    """Test query with special characters."""
    query = "What is 2 + 2? Explain with symbols: ∑, ∫, √."
    
    response = await huggingface.generate(query, task_type=TaskType.CHAT)
    
    assert response is not None
    assert len(response) > 0
    print(f"\n✅ HuggingFace Special Chars Response: {response[:200]}...")


@pytest.mark.asyncio
async def test_huggingface_response_consistency(huggingface):
    """Test that similar queries produce responses (not exact match due to randomness)."""
    query = "Say hello"
    
    response1 = await huggingface.generate(query, task_type=TaskType.CHAT)
    response2 = await huggingface.generate(query, task_type=TaskType.CHAT)
    
    # Both should produce valid responses
    assert response1 is not None and len(response1) > 0
    assert response2 is not None and len(response2) > 0
    # Responses might differ due to temperature, but both should be valid
    print(f"\n✅ Response 1: {response1[:100]}...")
    print(f"✅ Response 2: {response2[:100]}...")
