"""
Unit tests for custom exception classes.
"""
import pytest
from openmux.utils.exceptions import (
    OpenMuxError,
    ConfigurationError,
    ProviderError,
    ProviderUnavailableError,
    APIError,
    NoProvidersAvailableError,
    FailoverError,
    ClassificationError,
    ValidationError,
    TimeoutError,
    ModelNotFoundError,
)


class TestOpenMuxError:
    """Tests for base OpenMuxError class."""
    
    def test_simple_message(self):
        """Test error with just a message."""
        error = OpenMuxError("Something went wrong")
        assert str(error) == "Something went wrong"
        assert error.message == "Something went wrong"
        assert error.details is None
    
    def test_message_with_details(self):
        """Test error with message and details."""
        error = OpenMuxError("Error occurred", "Try this solution")
        assert "Error occurred" in str(error)
        assert "Try this solution" in str(error)
        assert error.message == "Error occurred"
        assert error.details == "Try this solution"
    
    def test_is_exception_subclass(self):
        """Test that OpenMuxError is a proper Exception subclass."""
        error = OpenMuxError("test")
        assert isinstance(error, Exception)


class TestConfigurationError:
    """Tests for ConfigurationError."""
    
    def test_basic_message(self):
        """Test configuration error with basic message."""
        error = ConfigurationError("Missing API key")
        assert "Missing API key" in str(error)
        assert "openmux init" in str(error)  # Auto-added suggestion
        assert error.message == "Missing API key"
    
    def test_custom_details(self):
        """Test configuration error with custom details."""
        error = ConfigurationError("Bad config", "Check line 42")
        assert "Bad config" in str(error)
        assert "Check line 42" in str(error)
        assert "openmux init" not in str(error)  # Custom details override
    
    def test_is_openmux_error(self):
        """Test inheritance from OpenMuxError."""
        error = ConfigurationError("test")
        assert isinstance(error, OpenMuxError)


class TestProviderError:
    """Tests for ProviderError."""
    
    def test_provider_name_in_message(self):
        """Test that provider name is included in message."""
        error = ProviderError("OpenRouter", "Failed to connect")
        assert "OpenRouter" in str(error)
        assert "Failed to connect" in str(error)
        assert error.provider_name == "OpenRouter"
    
    def test_with_details(self):
        """Test provider error with details."""
        error = ProviderError("HuggingFace", "Timeout", "Retry in 5 seconds")
        assert "HuggingFace" in str(error)
        assert "Timeout" in str(error)
        assert "Retry in 5 seconds" in str(error)


class TestProviderUnavailableError:
    """Tests for ProviderUnavailableError."""
    
    def test_no_reason(self):
        """Test unavailable error without reason."""
        error = ProviderUnavailableError("Ollama")
        assert "Ollama" in str(error)
        assert "not available" in str(error)
    
    def test_with_reason(self):
        """Test unavailable error with reason."""
        error = ProviderUnavailableError("OpenRouter", "Missing API key")
        assert "OpenRouter" in str(error)
        assert "Missing API key" in str(error)
    
    def test_api_key_suggestion(self):
        """Test auto-suggestion for API key errors."""
        error = ProviderUnavailableError("OpenRouter", "API key not found")
        assert "Configure OpenRouter API key" in str(error)
        assert ".env file" in str(error)
    
    def test_server_suggestion(self):
        """Test auto-suggestion for server errors."""
        error = ProviderUnavailableError("Ollama", "Server not responding")
        assert "Ensure Ollama server is running" in str(error)


class TestAPIError:
    """Tests for APIError."""
    
    def test_with_status_code(self):
        """Test API error with status code."""
        error = APIError("OpenRouter", status_code=404)
        assert "OpenRouter" in str(error)
        assert "404" in str(error)
        assert error.status_code == 404
    
    def test_with_message(self):
        """Test API error with custom message."""
        error = APIError("OpenRouter", status_code=500, message="Server error")
        assert "500" in str(error)
        assert "Server error" in str(error)
    
    def test_401_suggestion(self):
        """Test auto-suggestion for 401 errors."""
        error = APIError("OpenRouter", status_code=401)
        assert "Invalid API key" in str(error)
        assert "credentials" in str(error)
    
    def test_429_suggestion(self):
        """Test auto-suggestion for 429 errors."""
        error = APIError("OpenRouter", status_code=429)
        assert "Rate limit" in str(error)
        assert "wait before retrying" in str(error)
    
    def test_500_suggestion(self):
        """Test auto-suggestion for 500 errors."""
        error = APIError("OpenRouter", status_code=503)
        assert "Server error" in str(error)
        assert "experiencing issues" in str(error)
    
    def test_with_response_text(self):
        """Test API error with response text."""
        error = APIError("OpenRouter", response_text="Detailed error info here")
        assert "Detailed error info" in str(error)
    
    def test_without_status_code(self):
        """Test API error without status code."""
        error = APIError("OpenRouter", message="Connection failed")
        assert "Connection failed" in str(error)
        assert error.status_code is None


class TestNoProvidersAvailableError:
    """Tests for NoProvidersAvailableError."""
    
    def test_no_providers(self):
        """Test error when no providers are available."""
        error = NoProvidersAvailableError()
        assert "No providers currently available" in str(error)
        assert "openmux init" in str(error)
    
    def test_with_task_type(self):
        """Test error for specific task type."""
        error = NoProvidersAvailableError(task_type="CODE")
        assert "CODE" in str(error)
        assert "No providers available for task type" in str(error)
    
    def test_with_available_providers(self):
        """Test error with list of available providers."""
        error = NoProvidersAvailableError(
            task_type="IMAGE",
            available_providers=["OpenRouter", "HuggingFace"]
        )
        assert "IMAGE" in str(error)
        assert "OpenRouter" in str(error)
        assert "HuggingFace" in str(error)
        assert "None support" in str(error)


class TestFailoverError:
    """Tests for FailoverError."""
    
    def test_basic_failover(self):
        """Test failover error with attempted providers."""
        error = FailoverError(["OpenRouter", "HuggingFace"])
        assert "2 providers failed" in str(error)
        assert "OpenRouter" in str(error)
        assert "HuggingFace" in str(error)
    
    def test_with_last_error(self):
        """Test failover error with last error."""
        last_err = Exception("Connection timeout")
        error = FailoverError(["Provider1"], last_err)
        assert "Provider1" in str(error)
        assert "Connection timeout" in str(error)
        assert error.last_error == last_err
    
    def test_status_link(self):
        """Test that status page link is included."""
        error = FailoverError(["OpenRouter"])
        assert "status.openrouter.ai" in str(error)


class TestClassificationError:
    """Tests for ClassificationError."""
    
    def test_basic_classification_error(self):
        """Test classification error with query."""
        error = ClassificationError("What is Python?")
        assert "Failed to classify query" in str(error)
        assert error.query == "What is Python?"
    
    def test_with_reason(self):
        """Test classification error with reason."""
        error = ClassificationError("Test query", "Model not loaded")
        assert "Model not loaded" in str(error)
    
    def test_manual_task_suggestion(self):
        """Test that manual task type suggestion is included."""
        error = ClassificationError("Test query")
        assert "--task" in str(error)
        assert "openmux chat" in str(error)


class TestValidationError:
    """Tests for ValidationError."""
    
    def test_basic_validation(self):
        """Test validation error with field and reason."""
        error = ValidationError("email", "user@", "Invalid format")
        assert "email" in str(error)
        assert "Invalid format" in str(error)
        assert error.field == "email"
        assert error.value == "user@"
    
    def test_different_types(self):
        """Test validation error with different value types."""
        error = ValidationError("count", -5, "Must be positive")
        assert "count" in str(error)
        assert "Must be positive" in str(error)
        assert error.value == -5


class TestTimeoutError:
    """Tests for TimeoutError."""
    
    def test_basic_timeout(self):
        """Test timeout error with operation and duration."""
        error = TimeoutError("API request", 30.0)
        assert "API request" in str(error)
        assert "30" in str(error)
        assert "timed out" in str(error)
        assert error.operation == "API request"
        assert error.timeout == 30.0
    
    def test_suggestion(self):
        """Test that helpful suggestion is included."""
        error = TimeoutError("download", 10.0)
        assert "increasing the timeout" in str(error) or "network connection" in str(error)


class TestModelNotFoundError:
    """Tests for ModelNotFoundError."""
    
    def test_model_only(self):
        """Test error with just model name."""
        error = ModelNotFoundError("gpt-5")
        assert "gpt-5" in str(error)
        assert "not found" in str(error)
        assert error.model_name == "gpt-5"
        assert error.provider is None
    
    def test_with_provider(self):
        """Test error with model and provider."""
        error = ModelNotFoundError("llama-99", "HuggingFace")
        assert "llama-99" in str(error)
        assert "HuggingFace" in str(error)
        assert error.provider == "HuggingFace"
    
    def test_providers_command_suggestion(self):
        """Test that providers command suggestion is included."""
        error = ModelNotFoundError("test-model")
        assert "openmux providers" in str(error)


class TestExceptionHierarchy:
    """Tests for exception hierarchy and inheritance."""
    
    def test_all_inherit_from_openmux_error(self):
        """Test that all custom exceptions inherit from OpenMuxError."""
        exceptions = [
            ConfigurationError("test"),
            ProviderError("test", "test"),
            ProviderUnavailableError("test"),
            APIError("test"),
            NoProvidersAvailableError(),
            FailoverError([]),
            ClassificationError("test"),
            ValidationError("test", "test", "test"),
            TimeoutError("test", 1.0),
            ModelNotFoundError("test"),
        ]
        
        for exc in exceptions:
            assert isinstance(exc, OpenMuxError)
            assert isinstance(exc, Exception)
    
    def test_provider_errors_inherit_correctly(self):
        """Test provider error inheritance."""
        errors = [
            ProviderUnavailableError("test"),
            APIError("test"),
        ]
        
        for err in errors:
            assert isinstance(err, ProviderError)
            assert isinstance(err, OpenMuxError)
    
    def test_can_catch_by_base_class(self):
        """Test that we can catch specific errors by base class."""
        try:
            raise APIError("test", status_code=500)
        except ProviderError as e:
            assert isinstance(e, APIError)
        except Exception:
            pytest.fail("Should have caught as ProviderError")
    
    def test_can_catch_all_as_openmux_error(self):
        """Test that we can catch all custom errors as OpenMuxError."""
        try:
            raise ValidationError("test", "val", "reason")
        except OpenMuxError as e:
            assert isinstance(e, ValidationError)
        except Exception:
            pytest.fail("Should have caught as OpenMuxError")
