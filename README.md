# OpenMux

**Free Multi-Source GenAI Orchestration Library**

OpenMux is a Python library that automatically selects, routes, and combines outputs from free GenAI models and API providers. It creates a unified interface for discovering, connecting, and using open-access models across the AI ecosystem — including OpenRouter, HuggingFace, Together AI, Mistral, Ollama, LM Studio, and other publicly available sources.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen)](docs/TESTING_STRATEGY.md)

---

## 🚀 Quick Start

```python
from openmux import Orchestrator, TaskType

# Initialize
orchestrator = Orchestrator()

# Process a query
response = orchestrator.process("What is Python?")
print(response)

# Process with specific task type
code_response = orchestrator.process(
    "Write a fibonacci function",
    task_type=TaskType.CODE
)

# Multi-model processing
combined = orchestrator.process_multi(
    query="Explain quantum computing",
    num_models=2,
    combination_method="summarize"
)
```

## 🌟 Features

Smart Model Selector is a unified interface for discovering, connecting, and using open-access models across the AI ecosystem. It automatically selects, routes, and combines outputs from free GenAI models and API providers.

## Features

- **Automatic Provider Discovery**
  - Maintains updated list of free GenAI model providers
  - Automatic metadata updates from central registry
  - Focus on free and open-source endpoints

- **Task Auto-Classification**
  - Intelligent query analysis for task classification
  - Supports: chat, code, tts, audio, embeddings, image
  - Lightweight local classifier with manual override options

- **Model Auto-Selection**
  - Smart model selection based on capability metadata
  - Response quality tracking
  - Latency and uptime monitoring
  - Transparent selection reasoning

- **Multi-Model Routing**
  - Parallel query processing across multiple models
  - Configurable response combination methods
  - Support for text and embeddings (multimodal planned)

- **Offline & Local Fallback**
  - Local model hosting support via Ollama, LM Studio
  - Bundled lightweight open models
  - Hardware-aware automatic mode switching
  - Configurable fallback settings

## Project Structure

```
smart_model_selector/
├── core/               # Core functionality
│   ├── selector.py     # Model selection logic
│   ├── router.py      # Query routing
│   └── combiner.py    # Response combination
├── providers/         # Provider implementations
│   ├── base.py       # Base provider interface
│   ├── openrouter.py # OpenRouter integration
│   ├── huggingface.py # HuggingFace integration
│   └── ollama.py     # Ollama integration
├── classifier/        # Task classification
│   ├── classifier.py # Main classifier
│   └── models.py     # Classification models
└── utils/            # Utility functions
    ├── config.py     # Configuration management
    ├── security.py   # Security utilities
    └── logging.py    # Logging utilities
```

## 📦 Installation

### From PyPI (Coming Soon)
```bash
pip install openmux
# or using uv
uv pip install openmux
```

### From Source (Current)
```bash
# Clone the repository
git clone https://github.com/mdnu838/openmux.git
cd openmux

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
uv pip install -e ".[dev]"
```

### Environment Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Add your API keys to `.env`:
   ```bash
   # OpenRouter (required for online models)
   OPENROUTER_API_KEY=your_key_here
   
   # HuggingFace (optional)
   HF_TOKEN=your_token_here
   
   # Ollama (for local models)
   OLLAMA_URL=http://localhost:11434
   ```

3. **Never commit your `.env` file!** It's already in `.gitignore`.

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run unit tests only
pytest tests/unit/ -v

# Run with coverage
pytest tests/ --cov=openmux --cov-report=term-missing

# Run mock-based tests (no API keys needed)
pytest tests/unit/ tests/integration/test_orchestrator_mock.py -v
```

**Test Status**: 12/12 core tests passing (100% success rate)

---

## 🤝 Contributing

We welcome contributions! **All feature changes require a branch and Pull Request.**

### Quick Contribution Guide

1. **Fork and clone** the repository
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes** following our code style
4. **Add tests** for new functionality
5. **Run tests**: `pytest tests/ -v`
6. **Format code**: `black openmux/ tests/`
7. **Create Pull Request** to `main` branch

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Branching Strategy

- `main` - Production-ready code (protected)
- `mvp-alpha` - Alpha testing branch (protected)
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `docs/*` - Documentation updates

**All PRs require**:
- ✅ Passing CI/CD checks
- ✅ Code review approval
- ✅ ≥90% test coverage
- ✅ Updated documentation

---

## 📖 Documentation

- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Architecture](docs/ARCHITECTURE.md) - System design
- [API Documentation](docs/API.md) - Detailed API reference
- [Testing Strategy](docs/TESTING_STRATEGY.md) - Testing guidelines
- [MVP Tasks](docs/MVP_TASKS.md) - Development roadmap
- [Test Results](TEST_RESULTS.md) - Current test status

---

## 🔒 Security

- **Never commit API keys** or secrets to the repository
- Use `.env` file for sensitive data (already in `.gitignore`)
- Report security issues privately (see CONTRIBUTING.md)

---

## 📊 Project Status

**Current Version**: 0.1.0-alpha  
**Branch**: mvp-alpha  
**Test Coverage**: 100% (core components)  
**Status**: Code-complete, ready for alpha testing

### Recent Updates
- ✅ Complete orchestration engine
- ✅ Mock-based integration tests
- ✅ Classifier fully functional
- ✅ GitHub Actions CI/CD
- ✅ Comprehensive documentation

See [DEVELOPMENT_SUMMARY.md](DEVELOPMENT_SUMMARY.md) for detailed progress.

---

## Development

1. Clone the repository
2. Set up the development environment:
```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Contributing

Contributions are welcome! Please read our contributing guidelines and code of conduct.

**Important**: All feature changes require a separate branch and Pull Request to `main`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

Built with:
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [pytest](https://pytest.org/) - Testing framework
- [aiohttp](https://docs.aiohttp.org/) - Async HTTP client
- [pydantic](https://pydantic.dev/) - Data validation
- [rich](https://rich.readthedocs.io/) - Beautiful terminal output

---

**Star ⭐ this repo if you find it useful!**
