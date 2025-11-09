# GitHub Copilot Instructions for OpenMux

## 🎯 Project Vision
OpenMux is a **zero-configuration AI orchestration library** that auto-selects and routes queries to free GenAI models. Target UX: `pip install openmux` → add API key to `.env` → start chatting in < 2 minutes.

## 🏗️ Architecture Overview

### Core Components (Orchestrator Pattern)
```
Orchestrator → Classifier → Selector → Router → Provider
                                     ↓
                                 Combiner (multi-model)
                                     ↓
                                 Fallback (Ollama local)
```

**Key Flow:**
1. `Orchestrator` receives query
2. `Classifier` determines TaskType (CHAT, CODE, TTS, etc.)
3. `Selector` chooses best provider based on task + availability
4. `Router` executes query via provider's async `generate()` method
5. `Combiner` merges multi-model responses (optional)
6. `Fallback` uses local Ollama if providers fail

### Provider System
- **Base:** `openmux/providers/base.py` - Abstract `BaseProvider` with `is_available()`, `supports_task()`, `generate()`
- **Registry:** `openmux/providers/registry.py` - Singleton that initializes all providers and checks availability
- **Implementations:** OpenRouter (primary), HuggingFace, Ollama
- **Convention:** Each provider checks API keys/URLs in `is_available()` before activation

## 📁 Critical File Locations

### Entry Points
- `openmux/__init__.py` - Exports `Orchestrator` and `TaskType`
- `openmux/core/orchestrator.py` - Main coordination logic (sync wrapper around async `_process_async()`)
- `openmux/cli/main.py` - CLI using Typer (WIP: `openmux chat` command)

### Configuration
- `.env` - **NEVER COMMIT!** Contains actual API keys
- `.env.example` - Template with placeholder values and documentation
- `openmux/utils/config.py` - Secure config with keyring + Fernet encryption
- `pyproject.toml` - Package metadata, dependencies, version (current: 0.1.6)

### Testing Structure
- `tests/unit/` - Fast tests with mocks, no API calls
- `tests/integration/` - Two types:
  - `test_orchestrator_mock.py` - Mock providers (always runs in CI)
  - `test_end_to_end.py`, `test_openrouter_live.py` - Real API calls (requires `OPENROUTER_API_KEY`)

## 🚀 Development Workflow

### Environment Setup (ALWAYS use `uv`)
```bash
uv venv                          # Create venv
source .venv/bin/activate        # Activate
uv pip install -e ".[dev]"       # Install with dev deps
cp .env.example .env             # Set up API keys
```

### Testing Commands
```bash
# Fast unit tests (no API keys needed)
pytest tests/unit/ -v

# Mock integration tests (no API keys needed)
pytest tests/integration/test_orchestrator_mock.py -v

# Live tests (requires OPENROUTER_API_KEY in .env)
pytest tests/integration/test_end_to_end.py -v

# Coverage report
pytest tests/ --cov=openmux --cov-report=term-missing
```

### Git Flow Branching
- **`main`** - Production (protected, publishes to PyPI)
- **`develop`** - Integration (protected, publishes to TestPyPI)
- **`feature/*`** - New features (branch from `develop`)
- **`fix/*`** - Bug fixes
- **`docs/*`** - Documentation updates

**Critical:** All PRs go `feature/*` → `develop` → `main`. Never push directly to `main`/`develop`.

### CI/CD Pipeline
- **`.github/workflows/ci.yml`** - Runs on `develop`, `feature/*`, etc. Tests only (Python 3.9-3.13 matrix)
- **`.github/workflows/publish.yml`** - Runs on `develop`/`main` pushes:
  - `develop` → TestPyPI
  - `main` → PyPI + GitHub Release
- **Versioning:** Manual in `pyproject.toml`, same version for both registries

## 🎨 Code Conventions

### Async/Await Pattern
- **External:** Sync wrapper (`orchestrator.process()`)
- **Internal:** Async implementation (`_process_async()`, all provider `generate()` methods)
- **Why:** Public API is sync for simplicity, but internal calls are async for performance

Example from `orchestrator.py`:
```python
def process(self, query: str, **kwargs) -> str:
    """Public sync API"""
    return asyncio.run(self._process_async(query, **kwargs))

async def _process_async(self, query: str, **kwargs) -> str:
    """Internal async implementation"""
    provider = self.selector.select_single(task_type)
    response = await self.router.route_single(provider, query, **kwargs)
    return response
```

### Configuration Loading
- **Priority:** Environment variables > `.env` file > defaults
- **Security:** Use `keyring` for API key storage if available
- **Pattern:** Check `OPENROUTER_API_KEY` in env before initializing provider

### Error Handling Strategy
1. Try primary provider
2. Log error with context
3. Attempt fallback (Ollama) if `fallback_enabled=True`
4. Raise exception with helpful message if both fail

### Testing Patterns
- **Mock providers:** Create `MockProvider` that inherits `BaseProvider` and returns predictable responses
- **Fixtures:** Use `@pytest.fixture` for `orchestrator` instances
- **Async tests:** Use `@pytest.mark.asyncio` decorator
- **Live API tests:** Gracefully skip if `OPENROUTER_API_KEY` not available

## 📦 Dependency Management

### Core Dependencies
- `pydantic>=2.0.0` - Data validation
- `transformers`, `torch` - Task classification (local ML model)
- `aiohttp>=3.9.0` - Async HTTP for provider calls
- `python-dotenv` - Environment variable loading
- `cryptography`, `keyring` - Secure credential storage
- `rich`, `typer` - CLI interface

### Dev Dependencies
- `pytest`, `pytest-asyncio`, `pytest-cov` - Testing
- `black`, `isort`, `ruff` - Formatting/linting
- `mypy` - Type checking

## 🔑 API Key Setup

### Required for MVP
- **OpenRouter** (`OPENROUTER_API_KEY`) - Primary provider
  - Get at: https://openrouter.ai/keys
  - Free tier available

### Optional for Enhanced Features
- **HuggingFace** (`HF_TOKEN`) - Secondary provider
- **Ollama** (`OLLAMA_URL`) - Local fallback (default: http://localhost:11434)

## 🎯 Current Sprint Focus

**Phase 1: MVP Enhancement** (see `docs/TASK_LIST.md`)

Priority tasks:
1. **Task 1.2 (In Progress):** CLI tool - `openmux chat` command
2. **Task 1.1 (Planned):** Setup wizard - `openmux init` for easy API key configuration
3. **Task 1.3 (Planned):** Enhanced model selection with health checks + failover

**Key deliverables:**
- CLI working: `openmux chat "What is Python?"`
- Init wizard: `openmux init` guides user through API key setup
- Auto `.env` detection and validation

## 🚨 Important Rules

### Security
- **NEVER** commit `.env` file (already in `.gitignore`)
- **NEVER** log API keys (even partially)
- Use `keyring` for persistent storage when available

### Code Quality
- All new features require tests (unit + integration mock)
- Maintain ≥90% coverage for core modules
- Run `black` before committing
- Document public APIs with docstrings (Google style)

### Documentation
- Update `docs/TASK_LIST.md` when completing tasks
- Keep `CHANGELOG.md` updated for version changes
- Add examples to `docs/QUICK_REFERENCE.md` for new features

## 📚 Key Documentation Files

- `docs/ARCHITECTURE.md` - System design details
- `docs/PROJECT_DEFINITION.md` - Vision, features, roadmap
- `docs/TASK_LIST.md` - Detailed sprint tasks with effort estimates
- `CONTRIBUTING.md` - Git flow, commit conventions, PR process
- `.github/REPOSITORY_SETUP.md` - Branch protection configuration

## 🔧 Common Tasks

### Adding a New Provider
1. Create `openmux/providers/newprovider.py` inheriting `BaseProvider`
2. Implement `is_available()`, `supports_task()`, `generate()`
3. Register in `ProviderRegistry._initialize_providers()`
4. Add API key to `.env.example` with docs
5. Write unit tests in `tests/unit/test_newprovider.py`
6. Add integration test (mock version)

### Releasing a New Version
1. Update `version` in `pyproject.toml`
2. Update `CHANGELOG.md` with changes
3. Merge PR to `develop` → auto-publish to TestPyPI
4. Test install: `uv pip install --index-url https://test.pypi.org/simple/ openmux`
5. Merge `develop` → `main` → auto-publish to PyPI + GitHub Release

### Running Local CLI
```bash
# During development (editable install)
uv pip install -e ".[dev]"
openmux chat "test query"

# Or run directly
python -m openmux.cli.main chat "test query"
```

---

**Remember:** This project prioritizes **developer experience** and **minimal setup time**. Every feature should ask: "Does this reduce time-to-first-query?"
