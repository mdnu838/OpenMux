"""
Unit tests for TaskClassifier.
"""

import pytest

from openmux.classifier.classifier import TaskClassifier
from openmux.classifier.task_types import TaskType


@pytest.fixture
def classifier():
    """Create classifier instance for testing."""
    return TaskClassifier()


def test_classify_chat_query(classifier):
    """Test classification of chat queries."""
    query = "What is the capital of France?"
    task_type, confidence = classifier.classify(query)
    
    assert task_type == TaskType.CHAT
    assert 0 < confidence <= 1.0


def test_classify_code_query(classifier):
    """Test classification of code-related queries."""
    queries = [
        "Write a Python function to calculate factorial",
        "How do I implement a binary search in JavaScript?",
        "Debug this code snippet",
        "Refactor this class to use inheritance"
    ]
    
    for query in queries:
        task_type, confidence = classifier.classify(query)
        assert task_type == TaskType.CODE
        assert confidence > 0.5


def test_classify_embeddings_query(classifier):
    """Test classification of embeddings queries."""
    queries = [
        "Generate embeddings for this text",
        "Find similar documents using semantic search",
        "Create vector representations"
    ]
    
    for query in queries:
        task_type, confidence = classifier.classify(query)
        assert task_type == TaskType.EMBEDDINGS
        assert confidence > 0.5


def test_classify_batch(classifier):
    """Test batch classification."""
    queries = [
        "What is Python?",
        "Write a function to sort an array",
        "Generate embeddings for text"
    ]
    
    results = classifier.classify_batch(queries)
    
    assert len(results) == 3
    assert results[0][0] == TaskType.CHAT
    assert results[1][0] == TaskType.CODE
    assert results[2][0] == TaskType.EMBEDDINGS


def test_confidence_scores(classifier):
    """Test that confidence scores are reasonable."""
    queries = [
        ("What is machine learning?", TaskType.CHAT),
        ("Implement a Python function class method", TaskType.CODE),
        ("Create vector embeddings", TaskType.EMBEDDINGS)
    ]
    
    for query, expected_type in queries:
        task_type, confidence = classifier.classify(query)
        assert task_type == expected_type
        assert 0.5 <= confidence <= 1.0


def test_code_block_detection(classifier):
    """Test detection of code blocks."""
    query = "Here's some code: ```python\ndef hello():\n    print('hi')\n```"
    task_type, confidence = classifier.classify(query)
    
    assert task_type == TaskType.CODE
