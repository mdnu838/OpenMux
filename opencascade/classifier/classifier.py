"""
Rule-based task classifier for determining query types.
"""

import re
from typing import Tuple

from .task_types import TaskType
from ..utils.logging import setup_logger


logger = setup_logger(__name__)


class TaskClassifier:
    """Rule-based classifier for identifying task types from queries."""
    
    def __init__(self):
        """Initialize the classifier with pattern rules."""
        # Strong code indicators (enough by themselves)
        self.strong_code_patterns = [
            r'\b(function|class|method|implement|code|program|script|debug|fix|refactor|optimize)\b',
            r'(```|`)',  # Code blocks
            r'\b(algorithm|data structure)\b',
        ]
        
        # Language patterns (supportive evidence)
        self.language_patterns = [
            r'\b(python|javascript|java|c\+\+|rust|go|typescript)\b',
        ]
        
        # Embeddings/search patterns (be more specific)
        self.embeddings_patterns = [
            r'\b(embed|embedding|embeddings)\b',
            r'\b(vector|vectors)\b',
            r'\b(semantic search)\b',
        ]
        
        # Compile patterns for efficiency
        self.strong_code_regex = re.compile('|'.join(self.strong_code_patterns), re.IGNORECASE)
        self.language_regex = re.compile('|'.join(self.language_patterns), re.IGNORECASE)
        self.embeddings_regex = re.compile('|'.join(self.embeddings_patterns), re.IGNORECASE)
    
    def classify(self, query: str) -> Tuple[TaskType, float]:
        """Classify a query into a task type.
        
        Args:
            query: Input query to classify
            
        Returns:
            Tuple of (TaskType, confidence_score)
        """
        query_lower = query.lower()
        
        # Check for embeddings first (most specific)
        if self.embeddings_regex.search(query):
            logger.info("Classified as EMBEDDINGS task")
            return TaskType.EMBEDDINGS, 0.9
        
        # Check for strong code indicators
        strong_code_matches = len(self.strong_code_regex.findall(query))
        language_matches = len(self.language_regex.findall(query))
        
        # Strong code pattern OR (language + some context)
        if strong_code_matches >= 1 or language_matches >= 2:
            confidence = min(0.9, 0.7 + (strong_code_matches * 0.1))
            logger.info(f"Classified as CODE task (confidence: {confidence})")
            return TaskType.CODE, confidence
        
        # Default to chat (including questions about programming languages)
        logger.info("Classified as CHAT task (default)")
        return TaskType.CHAT, 0.7
    
    def classify_batch(self, queries: list[str]) -> list[Tuple[TaskType, float]]:
        """Classify multiple queries at once.
        
        Args:
            queries: List of queries to classify
            
        Returns:
            List of (TaskType, confidence) tuples
        """
        return [self.classify(query) for query in queries]
