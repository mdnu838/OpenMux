"""
Command-line interface for OpenMux.
"""

import sys
import os
from pathlib import Path
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    typer = None

from ..core.orchestrator import Orchestrator
from ..classifier.task_types import TaskType


if RICH_AVAILABLE:
    app = typer.Typer(
        name="openmux",
        help="OpenMux - Free Multi-Source GenAI Orchestration",
        add_completion=False
    )
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
    def chat(
        query: Optional[str] = typer.Argument(None, help="Query to process"),
        task_type: Optional[str] = typer.Option(None, "--task", "-t", help="Task type (chat, code, embeddings)"),
        interactive: bool = typer.Option(False, "--interactive", "-i", help="Start interactive chat mode"),
    ):
        """Chat with AI models using OpenMux."""
        try:
            # Initialize orchestrator with context manager
            with Orchestrator() as orchestrator:
            
                if interactive or not query:
                    # Interactive mode
                    console.print(Panel(
                        "[bold cyan]OpenMux Interactive Chat[/bold cyan]\n"
                        "Type your questions below. Type 'exit' or 'quit' to end the session.",
                        style="cyan"
                    ))
                    
                    while True:
                        try:
                            user_input = Prompt.ask("\n[bold green]You[/bold green]")
                            
                            if user_input.lower() in ['exit', 'quit', 'q']:
                                console.print("[yellow]Goodbye![/yellow]")
                                break
                            
                            if not user_input.strip():
                                continue
                            
                            # Parse task type
                            task = None
                            if task_type:
                                task = TaskType.from_string(task_type)
                            
                            # Process query
                            console.print("[dim]Processing...[/dim]")
                            response = orchestrator.process(query=user_input, task_type=task)
                            
                            # Display response
                            console.print(Panel(
                                response,
                                title="[bold blue]AI Response[/bold blue]",
                                style="blue"
                            ))
                            
                        except KeyboardInterrupt:
                            console.print("\n[yellow]Goodbye![/yellow]")
                            break
                        except Exception as e:
                            console.print(f"[red]Error: {str(e)}[/red]")
                else:
                    # Single query mode
                    task = None
                    if task_type:
                        task = TaskType.from_string(task_type)
                    
                    console.print("[dim]Processing...[/dim]")
                    response = orchestrator.process(query=query, task_type=task)
                    
                    console.print(Panel(
                        response,
                        title="[bold blue]Response[/bold blue]",
                        style="blue"
                    ))
                
        except Exception as e:
            console.print(Panel(f"[bold red]Error:[/bold red] {str(e)}", style="red"))
            raise typer.Exit(code=1)


    @app.command()
    def init(
        force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing .env file")
    ):
        """Initialize OpenMux configuration with API keys."""
        try:
            env_path = Path.cwd() / ".env"
            env_example_path = Path(__file__).parent.parent.parent / ".env.example"
            
            # Check if .env exists
            if env_path.exists() and not force:
                if not Confirm.ask(f".env file already exists at {env_path}. Overwrite?"):
                    console.print("[yellow]Initialization cancelled.[/yellow]")
                    raise typer.Exit()
            
            console.print(Panel(
                "[bold cyan]OpenMux Setup Wizard[/bold cyan]\n\n"
                "This wizard will help you configure OpenMux with your API keys.\n"
                "You can press Enter to skip optional keys.",
                style="cyan"
            ))
            
            # Collect API keys
            console.print("\n[bold]Required API Keys:[/bold]")
            openrouter_key = Prompt.ask(
                "OpenRouter API Key (get it at https://openrouter.ai/keys)",
                default=""
            )
            
            console.print("\n[bold]Optional API Keys:[/bold]")
            hf_token = Prompt.ask(
                "HuggingFace Token (optional, press Enter to skip)",
                default=""
            )
            
            ollama_url = Prompt.ask(
                "Ollama URL (for local models)",
                default="http://localhost:11434"
            )
            
            # Write .env file
            env_content = "# OpenMux Environment Variables\n"
            env_content += "# Generated by openmux init\n\n"
            
            env_content += "# =====================================\n"
            env_content += "# Provider API Keys\n"
            env_content += "# =====================================\n\n"
            
            env_content += "# OpenRouter API Key (Required)\n"
            env_content += f"OPENROUTER_API_KEY={openrouter_key}\n\n"
            
            if hf_token:
                env_content += "# HuggingFace Token (Optional)\n"
                env_content += f"HF_TOKEN={hf_token}\n\n"
            
            env_content += "# =====================================\n"
            env_content += "# Ollama Configuration (Optional)\n"
            env_content += "# =====================================\n\n"
            env_content += f"OLLAMA_URL={ollama_url}\n"
            
            # Write to file
            with open(env_path, 'w') as f:
                f.write(env_content)
            
            console.print(Panel(
                f"[bold green]✓ Configuration saved to {env_path}[/bold green]\n\n"
                "You can now use OpenMux:\n"
                "  • openmux chat \"Hello!\"\n"
                "  • openmux chat --interactive",
                style="green"
            ))
            
        except Exception as e:
            console.print(Panel(f"[bold red]Error:[/bold red] {str(e)}", style="red"))
            raise typer.Exit(code=1)


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
