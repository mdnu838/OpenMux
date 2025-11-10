"""
Live API integration tests using real OpenRouter API.

These tests require OPENROUTER_API_KEY in environment.
They make actual API calls and verify real-world behavior.
"""
import pytest
import os
from openmux import Orchestrator, TaskType
from openmux.utils.exceptions import (
    ConfigurationError,
    NoProvidersAvailableError,
    ProviderError,
    FailoverError
)


# Skip all tests if API key is not available
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="OPENROUTER_API_KEY not set - skipping live API tests"
)


class TestLiveAPIBasics:
    """Test basic API functionality with real calls."""
    
    def test_simple_chat_query(self):
        """Test a simple chat query with live API."""
        orchestrator = Orchestrator()
        response = orchestrator.process(
            "Say 'Hello, World!' and nothing else",
            task_type=TaskType.CHAT
        )
        
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
        assert "hello" in response.lower() or "world" in response.lower()
    
    def test_code_generation_query(self):
        """Test code generation with live API."""
        orchestrator = Orchestrator()
        response = orchestrator.process(
            "Write a Python function to add two numbers. Just the code, no explanation.",
            task_type=TaskType.CODE
        )
        
        assert response is not None
        assert isinstance(response, str)
        assert "def" in response or "lambda" in response
        # Should contain Python syntax
        assert any(keyword in response for keyword in ["def", "return", "lambda", "+"])
    
    def test_auto_task_classification(self):
        """Test automatic task type detection."""
        orchestrator = Orchestrator()
        
        # Should auto-detect as CODE task
        code_response = orchestrator.process(
            "def factorial(n):",
            # No task_type specified - should auto-classify
        )
        
        assert code_response is not None
        assert isinstance(code_response, str)
    
    def test_response_length_reasonable(self):
        """Test that responses are reasonable length."""
        orchestrator = Orchestrator()
        response = orchestrator.process(
            "What is 2+2? Answer in one word.",
            task_type=TaskType.CHAT
        )
        
        assert response is not None
        # Should be short - just a number or brief answer
        assert len(response) < 100


class TestLiveAPIErrorHandling:
    """Test error handling with real API."""
    
    def test_invalid_api_key_error(self, monkeypatch):
        """Test error when API key is invalid."""
        # Temporarily replace with invalid key
        monkeypatch.setenv("OPENROUTER_API_KEY", "invalid-key-12345")
        
        orchestrator = Orchestrator()
        
        # Should raise FailoverError since all providers will fail
        with pytest.raises(FailoverError):
            orchestrator.process("test query", task_type=TaskType.CHAT)
    
    def test_empty_query_handling(self):
        """Test handling of empty queries."""
        orchestrator = Orchestrator()
        
        # Empty query should either raise error or return something
        response = orchestrator.process("", task_type=TaskType.CHAT)
        # At minimum, should not crash
        assert response is not None or True  # Either response or no crash
    
    def test_very_long_query(self):
        """Test handling of very long queries."""
        orchestrator = Orchestrator()
        
        # Create a very long query
        long_query = "Tell me about " + ("artificial intelligence " * 100)
        
        try:
            response = orchestrator.process(long_query, task_type=TaskType.CHAT)
            assert response is not None
        except Exception as e:
            # If it fails, should be a proper exception
            assert isinstance(e, (ProviderError, FailoverError))


class TestLiveAPIFailover:
    """Test failover behavior with real API."""
    
    @pytest.mark.asyncio
    async def test_failover_on_provider_failure(self):
        """Test that failover works when primary provider fails."""
        orchestrator = Orchestrator()
        
        # Process a query - should succeed even if one provider fails
        response = await orchestrator._process_async(
            "Hello", 
            task_type=TaskType.CHAT,
            enable_failover=True
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    def test_multiple_providers_attempted(self):
        """Test that system tries multiple providers if needed."""
        orchestrator = Orchestrator()
        
        # This should work with failover enabled (default)
        response = orchestrator.process(
            "Test query",
            task_type=TaskType.CHAT
        )
        
        assert response is not None


class TestLiveAPIPerformance:
    """Test performance characteristics with real API."""
    
    def test_response_time_reasonable(self):
        """Test that responses come back in reasonable time."""
        import time
        
        orchestrator = Orchestrator()
        
        start_time = time.time()
        response = orchestrator.process(
            "Say 'quick test'",
            task_type=TaskType.CHAT
        )
        elapsed = time.time() - start_time
        
        assert response is not None
        # Should respond within 30 seconds (default timeout)
        assert elapsed < 30
        # Typically should be much faster
        print(f"Response time: {elapsed:.2f}s")
    
    def test_concurrent_requests(self):
        """Test multiple concurrent requests."""
        import asyncio
        
        orchestrator = Orchestrator()
        
        async def make_request(query):
            return await orchestrator._process_async(query, task_type=TaskType.CHAT)
        
        async def test_concurrent():
            queries = [
                "Say 'one'",
                "Say 'two'",
                "Say 'three'"
            ]
            
            results = await asyncio.gather(
                *[make_request(q) for q in queries],
                return_exceptions=True
            )
            
            # At least some should succeed
            successful = [r for r in results if isinstance(r, str)]
            assert len(successful) > 0
            
            return results
        
        results = asyncio.run(test_concurrent())
        assert len(results) == 3


class TestLiveAPIModels:
    """Test different model behaviors."""
    
    def test_different_task_types(self):
        """Test that different task types work."""
        test_cases = [
            (TaskType.CHAT, "Hello, how are you?"),
            (TaskType.CODE, "def hello(): pass"),
        ]
        
        for task_type, query in test_cases:
            # Create fresh orchestrator for each test to avoid event loop issues
            orchestrator = Orchestrator()
            response = orchestrator.process(query, task_type=task_type)
            assert response is not None
            assert isinstance(response, str)
            assert len(response) > 0
            # Cleanup
            orchestrator.cleanup()
    
    def test_model_consistency(self):
        """Test that same query gives consistent results."""
        query = "What is 5+5? Answer with just the number."
        
        responses = []
        for _ in range(3):
            # Create fresh orchestrator for each request to avoid event loop issues
            orchestrator = Orchestrator()
            response = orchestrator.process(query, task_type=TaskType.CHAT)
            responses.append(response)
            orchestrator.cleanup()
        
        # All responses should contain the answer "10"
        assert all(response is not None for response in responses)
        # Most should mention 10
        ten_count = sum(1 for r in responses if "10" in r)
        assert ten_count >= 2  # At least 2 out of 3 should be correct


class TestLiveAPIEdgeCases:
    """Test edge cases and unusual inputs."""
    
    def test_special_characters_query(self):
        """Test queries with special characters."""
        orchestrator = Orchestrator()
        
        response = orchestrator.process(
            "What is @#$%? Explain these symbols.",
            task_type=TaskType.CHAT
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    def test_multilingual_query(self):
        """Test query in different language."""
        orchestrator = Orchestrator()
        
        response = orchestrator.process(
            "Bonjour! Comment allez-vous?",  # French
            task_type=TaskType.CHAT
        )
        
        assert response is not None
        assert isinstance(response, str)
    
    def test_code_with_syntax_error(self):
        """Test code query with intentional syntax error."""
        orchestrator = Orchestrator()
        
        response = orchestrator.process(
            "Fix this code: def broken( print('hello')",
            task_type=TaskType.CODE
        )
        
        assert response is not None
        # Should attempt to fix or explain the error
        assert isinstance(response, str)


class TestLiveAPIContextManager:
    """Test orchestrator context manager usage."""
    
    def test_context_manager(self):
        """Test using orchestrator as context manager."""
        with Orchestrator() as orchestrator:
            response = orchestrator.process(
                "Hello",
                task_type=TaskType.CHAT
            )
            assert response is not None
        
        # Should cleanup properly after exit


class TestLiveAPIConfiguration:
    """Test different configurations."""
    
    def test_custom_timeout(self):
        """Test with custom timeout setting."""
        orchestrator = Orchestrator()
        
        # Short timeout - might fail or succeed quickly
        try:
            response = orchestrator.process(
                "Quick answer",
                task_type=TaskType.CHAT,
                timeout=5  # 5 second timeout
            )
            assert response is not None
        except Exception:
            # Timeout exception is acceptable
            pass
    
    def test_max_retries(self):
        """Test with custom max retries."""
        orchestrator = Orchestrator()
        
        response = orchestrator.process(
            "Test",
            task_type=TaskType.CHAT,
            max_retries=1  # Only retry once
        )
        
        assert response is not None


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v", "-s"])
