"""
Unit tests for CLI commands.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from typer.testing import CliRunner

# Import CLI components
from openmux.cli.main import app, RICH_AVAILABLE


# Skip all tests if CLI dependencies not available
pytestmark = pytest.mark.skipif(
    not RICH_AVAILABLE,
    reason="CLI dependencies (typer, rich) not installed"
)


@pytest.fixture
def cli_runner():
    """Create CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_orchestrator():
    """Create mock orchestrator."""
    with patch('openmux.cli.main.Orchestrator') as mock:
        orchestrator_instance = Mock()
        orchestrator_instance.process.return_value = "Test response from AI"
        orchestrator_instance.process_multi.return_value = "Combined response from multiple models"
        orchestrator_instance.registry.get_all.return_value = {
            'openrouter': Mock(name='OpenRouter', is_available=Mock(return_value=True)),
            'ollama': Mock(name='Ollama', is_available=Mock(return_value=False))
        }
        orchestrator_instance.cleanup = Mock()
        orchestrator_instance.__enter__ = Mock(return_value=orchestrator_instance)
        orchestrator_instance.__exit__ = Mock(return_value=False)
        mock.return_value = orchestrator_instance
        yield mock


class TestChatCommand:
    """Test the chat command."""
    
    def test_chat_with_simple_query(self, cli_runner, mock_orchestrator):
        """Test chat command with a simple query."""
        result = cli_runner.invoke(app, ["chat", "Hello, world!"])
        
        assert result.exit_code == 0
        mock_orchestrator.return_value.process.assert_called_once()
        assert "Hello, world!" in str(mock_orchestrator.return_value.process.call_args)
    
    def test_chat_with_task_type(self, cli_runner, mock_orchestrator):
        """Test chat command with task type option."""
        result = cli_runner.invoke(app, ["chat", "Write a function", "--task", "code"])
        
        assert result.exit_code == 0
        mock_orchestrator.return_value.process.assert_called_once()
    
    def test_chat_handles_error(self, cli_runner, mock_orchestrator):
        """Test chat command handles errors gracefully."""
        mock_orchestrator.return_value.process.side_effect = Exception("API Error")
        
        result = cli_runner.invoke(app, ["chat", "Test query"])
        
        assert result.exit_code == 1
    
    def test_chat_interactive_mode_exit(self, cli_runner, mock_orchestrator):
        """Test interactive chat mode can exit."""
        result = cli_runner.invoke(app, ["chat", "--interactive"], input="exit\n")
        
        assert result.exit_code == 0


class TestInitCommand:
    """Test the init command."""
    
    def test_init_creates_env_file(self, cli_runner, tmp_path, monkeypatch):
        """Test init command creates .env file."""
        # Change to temp directory
        monkeypatch.chdir(tmp_path)
        
        # Mock user input
        inputs = [
            "test-openrouter-key",  # OpenRouter key
            "",  # HuggingFace (skip)
            "http://localhost:11434",  # Ollama URL
        ]
        
        result = cli_runner.invoke(app, ["init"], input="\n".join(inputs) + "\n")
        
        assert result.exit_code == 0
        
        env_file = tmp_path / ".env"
        assert env_file.exists()
        
        content = env_file.read_text()
        assert "OPENROUTER_API_KEY=test-openrouter-key" in content
        assert "OLLAMA_URL=http://localhost:11434" in content
    
    def test_init_prompts_before_overwrite(self, cli_runner, tmp_path, monkeypatch):
        """Test init command prompts before overwriting existing .env."""
        # Change to temp directory
        monkeypatch.chdir(tmp_path)
        
        # Create existing .env
        env_file = tmp_path / ".env"
        env_file.write_text("EXISTING_KEY=value")
        
        # Answer 'no' to overwrite prompt
        result = cli_runner.invoke(app, ["init"], input="n\n")
        
        assert result.exit_code == 1
        assert env_file.read_text() == "EXISTING_KEY=value"
    
    def test_init_force_overwrites(self, cli_runner, tmp_path, monkeypatch):
        """Test init command with --force flag overwrites without prompt."""
        # Change to temp directory
        monkeypatch.chdir(tmp_path)
        
        # Create existing .env
        env_file = tmp_path / ".env"
        env_file.write_text("EXISTING_KEY=value")
        
        # Use force flag
        inputs = [
            "new-key",  # OpenRouter key
            "",  # HuggingFace (skip)
            "http://localhost:11434",  # Ollama URL
        ]
        
        result = cli_runner.invoke(app, ["init", "--force"], input="\n".join(inputs) + "\n")
        
        assert result.exit_code == 0
        content = env_file.read_text()
        assert "new-key" in content
        assert "EXISTING_KEY" not in content


class TestQueryCommand:
    """Test the query command (legacy)."""
    
    def test_query_single_model(self, cli_runner, mock_orchestrator):
        """Test query command with single model."""
        result = cli_runner.invoke(app, ["query", "What is Python?"])
        
        assert result.exit_code == 0
        mock_orchestrator.return_value.process.assert_called_once()
    
    def test_query_multi_model(self, cli_runner, mock_orchestrator):
        """Test query command with multiple models."""
        result = cli_runner.invoke(app, ["query", "Explain AI", "--models", "2"])
        
        assert result.exit_code == 0
        mock_orchestrator.return_value.process_multi.assert_called_once()


class TestProvidersCommand:
    """Test the providers command."""
    
    def test_providers_lists_available(self, cli_runner, mock_orchestrator):
        """Test providers command lists available providers."""
        result = cli_runner.invoke(app, ["providers"])
        
        assert result.exit_code == 0
        # Should call registry to get providers
        mock_orchestrator.return_value.registry.get_all.assert_called_once()


class TestVersionCallback:
    """Test version display."""
    
    def test_version_flag(self, cli_runner):
        """Test --version flag displays version."""
        result = cli_runner.invoke(app, ["query", "--version"])
        
        # Version callback raises Exit after printing
        assert result.exit_code == 0 or "version" in result.output.lower()


class TestCLIIntegration:
    """Integration tests for CLI."""
    
    @pytest.mark.skipif(
        not RICH_AVAILABLE,
        reason="Requires CLI dependencies"
    )
    def test_cli_help_works(self, cli_runner):
        """Test CLI help command works."""
        result = cli_runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        assert "OpenMux" in result.output or "openmux" in result.output
    
    def test_chat_help_works(self, cli_runner):
        """Test chat command help works."""
        result = cli_runner.invoke(app, ["chat", "--help"])
        
        assert result.exit_code == 0
        assert "chat" in result.output.lower() or "query" in result.output.lower()
    
    def test_init_help_works(self, cli_runner):
        """Test init command help works."""
        result = cli_runner.invoke(app, ["init", "--help"])
        
        assert result.exit_code == 0
        assert "init" in result.output.lower()
