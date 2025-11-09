"""Logging configuration for OpenCascade."""

import logging
import sys
from pathlib import Path
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console
from datetime import datetime

def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO
) -> logging.Logger:
    """Set up a logger with console and optional file output."""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler with rich formatting
    console_handler = RichHandler(
        console=Console(force_terminal=True),
        show_time=True,
        show_path=True
    )
    console_handler.setLevel(level)
    logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

class ModelSelectionLogger:
    """Logger specifically for model selection decisions."""
    
    def __init__(self, log_file: Optional[str] = None):
        self.logger = setup_logger(
            "openmux.model_selection",
            log_file=log_file
        )
        
    def log_selection(
        self,
        query: str,
        selected_model: str,
        confidence: float,
        reasoning: str,
        metrics: dict
    ) -> None:
        """Log a model selection decision."""
        self.logger.info(
            "Model Selection:\n"
            f"Query: {query}\n"
            f"Selected Model: {selected_model}\n"
            f"Confidence: {confidence:.2f}\n"
            f"Reasoning: {reasoning}\n"
            f"Metrics: {metrics}"
        )

class BenchmarkLogger:
    """Logger for model performance benchmarks."""
    
    def __init__(self, log_file: Optional[str] = None):
        self.logger = setup_logger(
            "openmux.benchmarks",
            log_file=log_file
        )
        
    def log_benchmark(
        self,
        model: str,
        task_type: str,
        latency: float,
        success: bool,
        metrics: dict
    ) -> None:
        """Log benchmark results."""
        timestamp = datetime.now().isoformat()
        self.logger.info(
            "Benchmark Result:\n"
            f"Timestamp: {timestamp}\n"
            f"Model: {model}\n"
            f"Task Type: {task_type}\n"
            f"Latency: {latency:.2f}ms\n"
            f"Success: {success}\n"
            f"Metrics: {metrics}"
        )