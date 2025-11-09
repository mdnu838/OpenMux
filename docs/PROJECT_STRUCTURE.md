# OpenMux - Detailed Project Structure

## Project Name: OpenMux
**Tagline:** Free Multi-Source GenAI Orchestration Library

---

## 📁 Complete Folder Structure

```
OpenMux/
│
├── openmux/                      # Main package directory
│   ├── __init__.py                   # Package initialization
│   │
│   ├── core/                         # Core orchestration logic
│   │   ├── __init__.py
│   │   ├── orchestrator.py           # Main orchestration engine
│   │   ├── selector.py               # Model selection logic
│   │   ├── router.py                 # Query routing engine
│   │   ├── combiner.py               # Response combination engine
│   │   └── fallback.py               # Fallback handler
│   │
│   ├── providers/                    # Provider implementations
│   │   ├── __init__.py
│   │   ├── base.py                   # Base provider interface
│   │   ├── registry.py               # Provider registry
│   │   ├── openrouter.py             # OpenRouter integration
│   │   ├── huggingface.py            # HuggingFace integration
│   │   ├── together.py               # Together AI integration
│   │   ├── mistral.py                # Mistral API integration
│   │   ├── ollama.py                 # Ollama integration
│   │   ├── lmstudio.py               # LM Studio integration
│   │   └── local.py                  # Local transformers backend
│   │
│   ├── classifier/                   # Task classification
│   │   ├── __init__.py
│   │   ├── classifier.py             # Main classifier interface
│   │   ├── rule_based.py             # Rule-based classifier
│   │   ├── ml_classifier.py          # ML-based classifier
│   │   └── task_types.py             # Task type definitions
│   │
│   ├── models/                       # Local model management
│   │   ├── __init__.py
│   │   ├── manager.py                # Model download/management
│   │   ├── loader.py                 # Model loading utilities
│   │   ├── hardware.py               # Hardware detection
│   │   └── cache.py                  # Model caching
│   │
│   ├── utils/                        # Utility modules
│   │   ├── __init__.py
│   │   ├── config.py                 # Configuration management
│   │   ├── security.py               # Security utilities
│   │   ├── logging.py                # Logging system
│   │   ├── benchmarks.py             # Benchmarking utilities
│   │   ├── metrics.py                # Performance metrics
│   │   └── validators.py             # Input validators
│   │
│   └── cli/                          # Command-line interface
│       ├── __init__.py
│       ├── main.py                   # CLI entry point
│       └── commands.py               # CLI commands
│
├── tests/                            # Test suite
│   ├── __init__.py
│   │
│   ├── unit/                         # Unit tests
│   │   ├── __init__.py
│   │   ├── test_orchestrator.py
│   │   ├── test_selector.py
│   │   ├── test_router.py
│   │   ├── test_combiner.py
│   │   ├── test_fallback.py
│   │   ├── test_providers/
│   │   │   ├── test_base.py
│   │   │   ├── test_registry.py
│   │   │   ├── test_openrouter.py
│   │   │   ├── test_huggingface.py
│   │   │   ├── test_together.py
│   │   │   ├── test_mistral.py
│   │   │   ├── test_ollama.py
│   │   │   ├── test_lmstudio.py
│   │   │   └── test_local.py
│   │   ├── test_classifier/
│   │   │   ├── test_classifier.py
│   │   │   ├── test_rule_based.py
│   │   │   └── test_ml_classifier.py
│   │   ├── test_models/
│   │   │   ├── test_manager.py
│   │   │   ├── test_loader.py
│   │   │   ├── test_hardware.py
│   │   │   └── test_cache.py
│   │   └── test_utils/
│   │       ├── test_config.py
│   │       ├── test_security.py
│   │       ├── test_logging.py
│   │       ├── test_benchmarks.py
│   │       ├── test_metrics.py
│   │       └── test_validators.py
│   │
│   ├── integration/                  # Integration tests
│   │   ├── __init__.py
│   │   ├── test_provider_integration.py
│   │   ├── test_end_to_end.py
│   │   ├── test_multi_model.py
│   │   ├── test_offline_mode.py
│   │   └── test_fallback_flow.py
│   │
│   ├── fixtures/                     # Test fixtures and data
│   │   ├── __init__.py
│   │   ├── sample_queries.json
│   │   ├── mock_responses.json
│   │   └── test_configs.json
│   │
│   └── conftest.py                   # Pytest configuration
│
├── docs/                             # Documentation
│   ├── index.md                      # Documentation home
│   ├── getting_started.md            # Quick start guide
│   ├── installation.md               # Installation guide
│   ├── configuration.md              # Configuration guide
│   ├── architecture.md               # Architecture overview
│   ├── api_reference.md              # API documentation
│   ├── providers.md                  # Provider documentation
│   ├── task_classification.md        # Task classification guide
│   ├── benchmarking.md               # Benchmarking guide
│   ├── contributing.md               # Contributing guidelines
│   ├── testing_strategy.md           # Testing strategy
│   ├── debugging_guide.md            # Debugging guide
│   └── examples/                     # Example code
│       ├── basic_usage.py
│       ├── multi_model.py
│       ├── offline_mode.py
│       └── custom_provider.py
│
├── scripts/                          # Utility scripts
│   ├── setup_dev.sh                  # Development setup
│   ├── run_tests.sh                  # Test runner
│   ├── lint.sh                       # Linting script
│   ├── format.sh                     # Code formatting
│   └── update_providers.py           # Update provider registry
│
├── .github/                          # GitHub specific files
│   ├── workflows/                    # CI/CD workflows
│   │   ├── tests.yml                 # Test workflow
│   │   ├── lint.yml                  # Linting workflow
│   │   └── publish.yml               # Publishing workflow
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
│
├── config/                           # Configuration files
│   ├── default_config.json           # Default configuration
│   ├── provider_registry.json        # Provider registry
│   └── model_registry.json           # Model registry
│
├── pyproject.toml                    # Project configuration
├── uv.lock                           # Dependency lock file
├── requirements.txt                  # Requirements file
├── README.md                         # Project README
├── LICENSE                           # License file
├── CONTRIBUTING.md                   # Contributing guidelines
├── CHANGELOG.md                      # Changelog
└── .gitignore                        # Git ignore file
```

---

## 🎯 File Purposes

### Core Modules
- **orchestrator.py**: Main entry point, coordinates all operations
- **selector.py**: Implements model selection logic based on task and metadata
- **router.py**: Routes queries to appropriate providers
- **combiner.py**: Combines responses from multiple models
- **fallback.py**: Handles failures and fallback strategies

### Provider Modules
- **base.py**: Abstract base class defining provider interface
- **registry.py**: Manages provider registration and discovery
- **[provider].py**: Individual provider implementations

### Classifier Modules
- **classifier.py**: Main classifier interface
- **rule_based.py**: Simple rule-based classification
- **ml_classifier.py**: ML-based classification using lightweight models

### Model Management
- **manager.py**: Downloads and manages local models
- **loader.py**: Loads models into memory
- **hardware.py**: Detects and optimizes for available hardware
- **cache.py**: Caches loaded models for performance

### Testing Structure
- **unit/**: Tests individual functions and classes
- **integration/**: Tests interactions between components
- **fixtures/**: Shared test data and configurations

---

## 🔧 Development Workflow
1. Write code for one module
2. Write corresponding unit tests
3. Run tests and debug
4. Write integration tests
5. Document the module
6. Verify with other modules
7. Move to next task