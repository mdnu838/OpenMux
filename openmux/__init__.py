"""
OpenMux - Free Multi-Source GenAI Orchestration Library

A Python library for automatic model selection and routing across free GenAI providers.
"""

import os
from pathlib import Path

# Auto-load .env file if it exists
try:
    from dotenv import load_dotenv
    
    # Look for .env in current directory and parent directories
    current_dir = Path.cwd()
    env_file = current_dir / ".env"
    
    if env_file.exists():
        load_dotenv(env_file)
    else:
        # Try to find .env in parent directories (up to 3 levels)
        for parent in list(current_dir.parents)[:3]:
            env_file = parent / ".env"
            if env_file.exists():
                load_dotenv(env_file)
                break
except ImportError:
    # dotenv not installed, skip
    pass

from .core.orchestrator import Orchestrator
from .classifier.task_types import TaskType

__version__ = "0.1.0"
__author__ = "OpenMux Contributors"
__all__ = ["Orchestrator", "TaskType"]


def get_version():
    """Get the current version of OpenMux."""
    return __version__