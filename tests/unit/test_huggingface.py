"""
Unit tests for HuggingFace provider.
"""

import pytest
import os
from unittest.mock import AsyncMock, MagicMock, patch
import aiohttp

from openmux.providers.huggingface import HuggingFaceProvider
from openmux.classifier.task_types import TaskType


@pytest.fixture
def hf_provider():
    """Create HuggingFace provider with mock token."""
    with patch.dict(os.environ, {"HF_TOKEN": "hf_test_token"}):
        provider = HuggingFaceProvider()
        yield provider


@pytest.fixture
def hf_provider_no_token():
    """Create HuggingFace provider without token."""
    with patch.dict(os.environ, {}, clear=True):
        if "HF_TOKEN" in os.environ:
            del os.environ["HF_TOKEN"]
        provider = HuggingFaceProvider()
        yield provider


class TestHuggingFaceProviderInitialization:
    """Test HuggingFace provider initialization."""
    
    def test_init_with_env_token(self):
        """Test initialization with environment variable token."""
        with patch.dict(os.environ, {"HF_TOKEN": "hf_env_token"}):
            provider = HuggingFaceProvider()
            assert provider.api_token == "hf_env_token"
            assert provider.name == "HuggingFace"
    
    def test_init_with_explicit_token(self):
        """Test initialization with explicit token parameter."""
        provider = HuggingFaceProvider(api_token="hf_explicit_token")
        assert provider.api_token == "hf_explicit_token"
    
    def test_init_with_custom_model(self):
        """Test initialization with custom model ID."""
        provider = HuggingFaceProvider(
            api_token="hf_token",
            model_id="custom/model-id"
        )
        assert provider.model_id == "custom/model-id"
    
    def test_default_models_configured(self, hf_provider):
        """Test that default models are configured for each task type."""
        assert TaskType.CHAT in hf_provider.default_models
        assert TaskType.CODE in hf_provider.default_models
        assert TaskType.EMBEDDINGS in hf_provider.default_models
        
        # Verify model IDs are strings
        assert isinstance(hf_provider.default_models[TaskType.CHAT], str)
        assert isinstance(hf_provider.default_models[TaskType.CODE], str)
        assert isinstance(hf_provider.default_models[TaskType.EMBEDDINGS], str)


class TestHuggingFaceProviderAvailability:
    """Test provider availability checks."""
    
    def test_is_available_with_token(self, hf_provider):
        """Test that provider is available with valid token."""
        assert hf_provider.is_available() is True
    
    def test_is_available_without_token(self, hf_provider_no_token):
        """Test that provider is not available without token."""
        assert hf_provider_no_token.is_available() is False
    
    def test_supports_chat_task(self, hf_provider):
        """Test that provider supports chat tasks."""
        assert hf_provider.supports_task(TaskType.CHAT) is True
    
    def test_supports_code_task(self, hf_provider):
        """Test that provider supports code tasks."""
        assert hf_provider.supports_task(TaskType.CODE) is True
    
    def test_supports_embeddings_task(self, hf_provider):
        """Test that provider supports embeddings tasks."""
        assert hf_provider.supports_task(TaskType.EMBEDDINGS) is True
    
    def test_all_supported_task_types(self, hf_provider):
        """Test that all defined task types are checked for support."""
        # Provider should support all current TaskType values
        for task_type in TaskType:
            # HuggingFace supports CHAT, CODE, EMBEDDINGS
            result = hf_provider.supports_task(task_type)
            assert isinstance(result, bool)


class TestHuggingFaceProviderSession:
    """Test session management."""
    
    @pytest.mark.asyncio
    async def test_session_creation(self, hf_provider):
        """Test that session is created with correct headers."""
        session = await hf_provider._get_session()
        
        assert session is not None
        assert isinstance(session, aiohttp.ClientSession)
        assert hf_provider._session is session
        
        # Cleanup
        await session.close()
    
    @pytest.mark.asyncio
    async def test_session_reuse(self, hf_provider):
        """Test that same session is reused."""
        session1 = await hf_provider._get_session()
        session2 = await hf_provider._get_session()
        
        assert session1 is session2
        
        # Cleanup
        await session1.close()
    
    @pytest.mark.asyncio
    async def test_session_recreation_after_close(self, hf_provider):
        """Test that new session is created after closing."""
        session1 = await hf_provider._get_session()
        await session1.close()

        session2 = await hf_provider._get_session()

        assert session1 is not session2
        assert session1.closed  # session1 should be closed
        assert not session2.closed  # session2 should be open
        assert not session2.closed
        
        # Cleanup
        await session2.close()


class TestHuggingFaceProviderGenerate:
    """Test text generation."""
    
    @pytest.mark.asyncio
    async def test_generate_chat_response(self, hf_provider):
        """Test generating chat response."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = AsyncMock(return_value=[{
            "generated_text": "Hello! How can I help you today?"
        }])
        
        # Create async context manager
        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_cm)
        
        with patch.object(hf_provider, '_get_session', return_value=mock_session):
            response = await hf_provider.generate(
                "Hello",
                task_type=TaskType.CHAT
            )
            
            assert "Hello! How can I help you today?" in response
            mock_session.post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_code_response(self, hf_provider):
        """Test generating code response."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = AsyncMock(return_value=[{
            "generated_text": "def hello():\n    print('Hello, World!')"
        }])
        
        # Create async context manager
        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_cm)
        
        with patch.object(hf_provider, '_get_session', return_value=mock_session):
            response = await hf_provider.generate(
                "Write a hello world function in Python",
                task_type=TaskType.CODE
            )
            
            assert "def hello()" in response
            mock_session.post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_embeddings(self, hf_provider):
        """Test generating embeddings."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = AsyncMock(return_value=[0.1, 0.2, 0.3, 0.4])
        
        # Create async context manager
        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_cm)
        
        with patch.object(hf_provider, '_get_session', return_value=mock_session):
            response = await hf_provider.generate(
                "Test text",
                task_type=TaskType.EMBEDDINGS
            )
            
            # Embeddings returned as string representation
            assert isinstance(response, str)
            mock_session.post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_with_custom_parameters(self, hf_provider):
        """Test generating with custom parameters."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = AsyncMock(return_value=[{"generated_text": "Response"}])
        
        # Create async context manager
        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_cm)
        
        with patch.object(hf_provider, '_get_session', return_value=mock_session):
            response = await hf_provider.generate(
                "Test",
                task_type=TaskType.CHAT,
                max_tokens=1024,
                temperature=0.9,
                top_p=0.95
            )
            
            # Verify parameters were passed
            call_args = mock_session.post.call_args
            payload = call_args[1]['json']
            assert payload['parameters']['max_new_tokens'] == 1024
            assert payload['parameters']['temperature'] == 0.9
            assert payload['parameters']['top_p'] == 0.95
    
    @pytest.mark.asyncio
    async def test_generate_without_token_raises_exception(self, hf_provider_no_token):
        """Test that generating without token raises exception."""
        with pytest.raises(Exception, match="API token not configured"):
            await hf_provider_no_token.generate("Test")
    
    @pytest.mark.asyncio
    async def test_generate_with_http_error(self, hf_provider):
        """Test error handling for HTTP errors."""
        # Create mock response that raises exception
        mock_response = MagicMock()
        mock_response.status = 429
        mock_response.raise_for_status = MagicMock(side_effect=aiohttp.ClientResponseError(
            request_info=MagicMock(),
            history=(),
            status=429,
            message="Rate limit exceeded"
        ))

        # Create async context manager
        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__ = AsyncMock(return_value=None)

        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_cm)

        with patch.object(hf_provider, '_get_session', return_value=mock_session):
            with pytest.raises(aiohttp.ClientError):
                await hf_provider.generate("test query", TaskType.CHAT)

    @pytest.mark.asyncio
    async def test_generate_uses_custom_model_id(self):
        """Test that custom model_id is used when provided."""
        provider = HuggingFaceProvider(
            api_token="hf_token",
            model_id="custom/model"
        )
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = AsyncMock(return_value=[{"generated_text": "Response"}])
        
        # Create async context manager
        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_cm)
        
        with patch.object(provider, '_get_session', return_value=mock_session):
            await provider.generate("Test")
            
            # Verify custom model was used in URL
            call_args = mock_session.post.call_args
            url = call_args[0][0]
            assert "custom/model" in url


class TestHuggingFaceProviderCleanup:
    """Test cleanup and context manager."""
    
    @pytest.mark.asyncio
    async def test_close_closes_session(self, hf_provider):
        """Test that close() closes the session."""
        session = await hf_provider._get_session()
        assert not session.closed
        
        await hf_provider.close()
        
        assert session.closed
    
    @pytest.mark.asyncio
    async def test_close_without_session(self, hf_provider):
        """Test that close() works when no session exists."""
        # Should not raise any errors
        await hf_provider.close()
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager usage."""
        with patch.dict(os.environ, {"HF_TOKEN": "hf_test_token"}):
            async with HuggingFaceProvider() as provider:
                assert provider.is_available()
                session = await provider._get_session()
                assert not session.closed
            
            # Session should be closed after exiting context
            assert session.closed


class TestHuggingFaceProviderEdgeCases:
    """Test edge cases and error conditions."""
    
    @pytest.mark.asyncio
    async def test_generate_with_empty_query(self, hf_provider):
        """Test generating with empty query."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = AsyncMock(return_value=[{"generated_text": ""}])
        
        # Create async context manager
        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_cm)
        
        with patch.object(hf_provider, '_get_session', return_value=mock_session):
            response = await hf_provider.generate("", task_type=TaskType.CHAT)
            
            # Should still work, might return empty response
            assert isinstance(response, str)
    
    @pytest.mark.asyncio
    async def test_generate_with_unsupported_task_type_fallsback(self, hf_provider):
        """Test that provider falls back to CHAT for task without default model."""
        # Create a mock task type scenario by not passing task_type
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = AsyncMock(return_value=[{"generated_text": "Response"}])
        
        # Create async context manager
        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_cm)
        
        with patch.object(hf_provider, '_get_session', return_value=mock_session):
            # Should fall back to CHAT model when no task_type specified
            response = await hf_provider.generate("Test")
            
            assert isinstance(response, str)
            # Verify CHAT model was used
            call_args = mock_session.post.call_args
            url = call_args[0][0]
            assert "Llama-2-7b-chat" in url
    
    @pytest.mark.asyncio
    async def test_generate_with_malformed_response(self, hf_provider):
        """Test handling of malformed API response."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.raise_for_status = AsyncMock()
        mock_response.json = AsyncMock(return_value={"unexpected": "format"})
        
        # Create async context manager
        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_cm)
        
        with patch.object(hf_provider, '_get_session', return_value=mock_session):
            response = await hf_provider.generate("Test", task_type=TaskType.CHAT)
            
            # Should return string representation of unexpected response
            assert isinstance(response, str)
