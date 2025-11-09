"""
Command-line interface for OpenCascade.
"""

import sys
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    typer = None

from ..core.orchestrator import Orchestrator
from ..classifier.task_types import TaskType


if RICH_AVAILABLE:
    app = typer.Typer(help="OpenCascade - Free Multi-Source GenAI Orchestration")
    console = Console()
else:
    app = None
    console = None


def version_callback(value: bool):
    """Display version information."""
    if value:
        from .. import __version__
        if RICH_AVAILABLE:
            console.print(f"OpenCascade version {__version__}")
        else:
            print(f"OpenCascade version {__version__}")
        raise typer.Exit()


if RICH_AVAILABLE:
    @app.command()
    def query(
        text: str = typer.Argument(..., help="Query text to process"),
        task_type: Optional[str] = typer.Option(None, "--task", "-t", help="Task type (chat, code, embeddings)"),
        num_models: int = typer.Option(1, "--models", "-m", help="Number of models to use"),
        combination: str = typer.Option("merge", "--combine", "-c", help="Combination method (merge, summarize)"),
        version: Optional[bool] = typer.Option(None, "--version", "-v", callback=version_callback, is_eager=True)
    ):
        """Process a query using OpenCascade."""
        try:
            # Initialize orchestrator
            orchestrator = Orchestrator()
            
            # Parse task type
            task = None
            if task_type:
                task = TaskType.from_string(task_type)
            
            # Process query
            console.print(Panel("Processing query...", style="blue"))
            
            if num_models > 1:
                response = orchestrator.process_multi(
                    query=text,
                    num_models=num_models,
                    combination_method=combination,
                    task_type=task
                )
            else:
                response = orchestrator.process(
                    query=text,
                    task_type=task
                )
            
            # Display response
            console.print(Panel(response, title="Response", style="green"))
            
        except Exception as e:
            console.print(Panel(f"Error: {str(e)}", style="red"))
            raise typer.Exit(code=1)


    @app.command()
    def providers():
        """List available providers."""
        try:
            orchestrator = Orchestrator()
            orchestrator._initialize_selector()
            
            available = orchestrator.registry.get_all()
            
            console.print(Panel("Available Providers", style="blue"))
            
            for name, provider in available.items():
                status = "✓" if provider.is_available() else "✗"
                console.print(f"{status} {name}: {provider.name}")
            
        except Exception as e:
            console.print(Panel(f"Error: {str(e)}", style="red"))
            raise typer.Exit(code=1)


def main():
    """Main CLI entry point."""
    if not RICH_AVAILABLE:
        print("Error: CLI requires 'typer' and 'rich' packages.")
        print("Install with: pip install typer rich")
        sys.exit(1)
    
    app()


if __name__ == "__main__":
    main()
