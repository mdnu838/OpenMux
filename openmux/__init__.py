"""
OpenCascade - Free Multi-Source GenAI Orchestration Library

A Python library for automatic model selection and routing across free GenAI providers.
"""

from .core.orchestrator import Orchestrator
from .classifier.task_types import TaskType

__version__ = "0.1.0-alpha"
__author__ = "OpenCascade Contributors"
__all__ = ["Orchestrator", "TaskType"]


def get_version():
    """Get the current version of OpenCascade."""
    return __version__