"""
Custom exception classes for OpenMux.

Provides specific exception types for better error handling and user feedback.
"""
from typing import Optional, List, Any


class OpenMuxError(Exception):
    """Base exception for all OpenMux errors."""
    
    def __init__(self, message: str, details: Optional[str] = None):
        """Initialize exception with message and optional details.
        
        Args:
            message: Main error message
            details: Additional details or suggestions
        """
        self.message = message
        self.details = details
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        """Format error message with details."""
        if self.details:
            return f"{self.message}\n\nDetails: {self.details}"
        return self.message


class ConfigurationError(OpenMuxError):
    """Raised when there's a configuration issue."""
    
    def __init__(self, message: str, details: Optional[str] = None):
        if not details:
            details = (
                "Check your .env file or run 'openmux init' to configure API keys.\n"
                "See documentation: https://github.com/mdnu838/OpenMux#configuration"
            )
        super().__init__(message, details)


class ProviderError(OpenMuxError):
    """Raised when a provider encounters an error."""
    
    def __init__(self, provider_name: str, message: str, details: Optional[str] = None):
        self.provider_name = provider_name
        full_message = f"Provider '{provider_name}': {message}"
        super().__init__(full_message, details)


class ProviderUnavailableError(ProviderError):
    """Raised when a provider is not available."""
    
    def __init__(self, provider_name: str, reason: Optional[str] = None):
        message = "Provider not available"
        if reason:
            message = f"Provider not available: {reason}"
        
        details: Optional[str] = None
        if "api key" in reason.lower() if reason else False:
            details = f"Configure {provider_name} API key in your .env file"
        elif "server" in reason.lower() if reason else False:
            details = f"Ensure {provider_name} server is running"
        
        super().__init__(provider_name, message, details)


class APIError(ProviderError):
    """Raised when an API call fails."""
    
    def __init__(self, provider_name: str, status_code: Optional[int] = None, 
                 message: Optional[str] = None, response_text: Optional[str] = None):
        self.status_code = status_code
        self.response_text = response_text
        
        if status_code:
            error_message = f"API error {status_code}"
            if message:
                error_message += f": {message}"
        else:
            error_message = message or "API request failed"
        
        details: Optional[str] = None
        if status_code == 401:
            details = "Invalid API key. Please check your credentials."
        elif status_code == 429:
            details = "Rate limit exceeded. Please wait before retrying."
        elif status_code and status_code >= 500:
            details = "Server error. The provider may be experiencing issues."
        elif response_text:
            details = f"Response: {response_text[:200]}"
        
        super().__init__(provider_name, error_message, details)


class NoProvidersAvailableError(OpenMuxError):
    """Raised when no providers are available for a task."""
    
    def __init__(self, task_type: Optional[str] = None, available_providers: Optional[List[str]] = None):
        self.task_type = task_type
        self.available_providers = available_providers or []
        
        if task_type:
            message = f"No providers available for task type: {task_type}"
        else:
            message = "No providers currently available"
        
        details_parts = []
        if not self.available_providers:
            details_parts.append("No providers are configured or available.")
            details_parts.append("Run 'openmux init' to configure providers.")
        else:
            details_parts.append(f"Available providers: {', '.join(self.available_providers)}")
            details_parts.append(f"None support the '{task_type}' task type.")
        
        details = "\n".join(details_parts)
        super().__init__(message, details)


class FailoverError(OpenMuxError):
    """Raised when all provider failover attempts fail."""
    
    def __init__(self, attempted_providers: List[str], last_error: Optional[Exception] = None):
        self.attempted_providers = attempted_providers
        self.last_error = last_error
        
        message = f"All {len(attempted_providers)} providers failed"
        
        details_parts = [
            f"Attempted providers: {', '.join(attempted_providers)}"
        ]
        if last_error:
            details_parts.append(f"Last error: {str(last_error)}")
        details_parts.append(
            "Try again later or check provider status at https://status.openrouter.ai"
        )
        
        details = "\n".join(details_parts)
        super().__init__(message, details)


class ClassificationError(OpenMuxError):
    """Raised when task classification fails."""
    
    def __init__(self, query: str, reason: Optional[str] = None):
        self.query = query
        message = "Failed to classify query"
        if reason:
            message += f": {reason}"
        
        details = (
            "You can manually specify the task type using the --task flag.\n"
            f"Example: openmux chat --task code \"{query[:50]}...\""
        )
        super().__init__(message, details)


class ValidationError(OpenMuxError):
    """Raised when input validation fails."""
    
    def __init__(self, field: str, value: Any, reason: str):
        self.field = field
        self.value = value
        message = f"Invalid {field}: {reason}"
        super().__init__(message)


class TimeoutError(OpenMuxError):
    """Raised when an operation times out."""
    
    def __init__(self, operation: str, timeout: float):
        self.operation = operation
        self.timeout = timeout
        message = f"Operation '{operation}' timed out after {timeout} seconds"
        details = "Try increasing the timeout or check your network connection."
        super().__init__(message, details)


class ModelNotFoundError(OpenMuxError):
    """Raised when a requested model is not found."""
    
    def __init__(self, model_name: str, provider: Optional[str] = None):
        self.model_name = model_name
        self.provider = provider
        
        if provider:
            message = f"Model '{model_name}' not found in provider '{provider}'"
        else:
            message = f"Model '{model_name}' not found"
        
        details = "Use 'openmux providers' to see available models."
        super().__init__(message, details)
