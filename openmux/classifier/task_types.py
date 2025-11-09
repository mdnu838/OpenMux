"""Task type definitions for OpenCascade."""

from enum import Enum


class TaskType(Enum):
    """Supported task types for model selection."""
    
    CHAT = "chat"
    CODE = "code"
    EMBEDDINGS = "embeddings"
    
    def __str__(self):
        """Return string representation."""
        return self.value
    
    @classmethod
    def from_string(cls, value: str) -> "TaskType":
        """Create TaskType from string.
        
        Args:
            value: String value of task type
            
        Returns:
            TaskType enum
            
        Raises:
            ValueError: If value is not a valid task type
        """
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(
                f"Invalid task type: {value}. "
                f"Valid types: {', '.join([t.value for t in cls])}"
            )
