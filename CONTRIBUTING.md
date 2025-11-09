# Contributing to OpenMux

Thank you for your interest in contributing to OpenMux! This document provides guidelines and instructions for contributing.

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Commit Message Convention](#commit-message-convention)
- [Testing Requirements](#testing-requirements)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

---

## 📜 Code of Conduct

### Our Standards
- **Be Respectful**: Treat everyone with respect and kindness
- **Be Constructive**: Provide helpful, constructive feedback
- **Be Collaborative**: Work together towards common goals
- **Be Professional**: Maintain professionalism in all interactions

### Unacceptable Behavior
- Harassment or discrimination of any kind
- Trolling, insulting, or derogatory comments
- Personal or political attacks
- Publishing others' private information

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Git
- uv (recommended) or pip

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/mdnu838/OpenMux.git
cd OpenMux

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"

# Verify setup
pytest tests/unit/ -v
```

---

## 🌿 Development Workflow

### Branch Strategy

We follow a simplified Git Flow model:

- **`main`**: Production-ready code. Protected branch requiring PR reviews. → Publishes to **PyPI**
- **`develop`**: Integration branch for features. Tested code ready for next release. → Publishes to **TestPyPI**
- **`feature/*`**: New features (e.g., `feature/add-new-provider`)
- **`fix/*`**: Bug fixes (e.g., `fix/classifier-accuracy`)
- **`docs/*`**: Documentation updates (e.g., `docs/api-reference`)
- **`chore/*`**: Maintenance tasks (e.g., `chore/update-dependencies`)

### Creating a New Branch

```bash
# For a new feature
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# Make changes, commit, push
git add .
git commit -m "feat: Add awesome feature"
git push origin feature/your-feature-name

# Create PR on GitHub: feature/* → develop
```

### Keep Your Branch Updated

```bash
# Update from upstream
git fetch origin
git checkout develop
git merge origin/develop

# Rebase your feature branch
git checkout feature/your-feature-name
git rebase develop
```

---

## 📝 Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

### Examples

```bash
feat(classifier): Add support for image classification tasks

fix(orchestrator): Handle timeout errors gracefully

docs(readme): Update installation instructions

chore(deps): Upgrade transformers to v4.35.0

test(router): Add integration tests for failover logic
```

---

## 🧪 Testing Requirements

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v

# Run with coverage
pytest --cov=openmux --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_classifier.py -v
```

### Test Structure

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_classifier.py
│   └── test_orchestrator.py
├── integration/             # Integration tests
│   ├── test_orchestrator_mock.py    # Mock-based
│   └── test_openrouter_live.py      # Live API (requires key)
└── fixtures/                # Test data
```

### Writing Tests

```python
import pytest
from openmux import Orchestrator

def test_orchestrator_initialization():
    """Test that orchestrator initializes correctly."""
    orchestrator = Orchestrator(api_key="test_key")
    assert orchestrator is not None
    assert orchestrator.api_key == "test_key"

@pytest.mark.asyncio
async def test_async_processing():
    """Test async processing with mock data."""
    # Test implementation
    pass
```

### Test Coverage Requirements

- **Unit tests**: Minimum 80% coverage
- **Integration tests**: All major workflows
- **All new features**: Must include tests
- **Bug fixes**: Must include regression tests

---

## 🎨 Code Style

### Python Style

- Follow **PEP 8**
- Use **4 spaces** for indentation
- Maximum line length: **100 characters** (flexible to 120 for readability)
- Use **type hints** for function signatures
- Use **docstrings** (Google style preferred)

### Code Formatting

```bash
# Format code with Black
black openmux/ tests/

# Sort imports with isort
isort openmux/ tests/

# Lint with Ruff
ruff check openmux/ tests/

# Type check with mypy
mypy openmux/ --ignore-missing-imports
```

### Example Code Style

```python
from typing import Dict, List, Optional

def process_query(
    query: str,
    options: Optional[Dict[str, any]] = None
) -> List[str]:
    """
    Process a user query and return results.
    
    Args:
        query: The user's input query
        options: Optional configuration parameters
        
    Returns:
        List of processed results
        
    Raises:
        ValueError: If query is empty
    """
    if not query:
        raise ValueError("Query cannot be empty")
    
    # Implementation here
    return results
```

---

## 🔄 Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow convention
- [ ] Branch is up-to-date with develop

### PR Description Template

Use the PR template to include:

1. **What** - What changes does this PR make?
2. **Why** - Why are these changes needed?
3. **How** - How did you implement the changes?
4. **Testing** - How was this tested?
5. **Related Issues** - Link any related issues

### Review Process

1. Create PR from your branch to `develop`
2. Automated CI checks must pass
3. At least one maintainer approval required
4. Address all review comments
5. Maintainer merges PR

---

## 📦 Release Process (Maintainers Only)

### Version Management

We use semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Publishing Workflow

#### 1. Development → TestPyPI (develop branch)

```bash
# Merge features to develop
git checkout develop
git pull origin develop

# Update version for testing (e.g., 0.2.0-beta.1)
# Edit pyproject.toml and openmux/__init__.py

# Update CHANGELOG.md
git add pyproject.toml openmux/__init__.py CHANGELOG.md
git commit -m "chore: Bump version to 0.2.0-beta.1"
git push origin develop

# 🚀 GitHub Actions automatically:
# - Runs all tests
# - Builds package
# - Publishes to TestPyPI
```

**Test the package:**
```bash
pip install -i https://test.pypi.org/simple/ openmux==0.2.0-beta.1
```

#### 2. Production → PyPI (main branch)

```bash
# Update version to stable (e.g., 0.2.0)
# Edit pyproject.toml and openmux/__init__.py

# Create PR: develop → main
# After review and merge:

# 🚀 GitHub Actions automatically:
# - Runs all tests
# - Builds package
# - Publishes to PyPI
# - Creates GitHub Release with tag v0.2.0
```

**Install from PyPI:**
```bash
pip install openmux==0.2.0
```

### Release Checklist

- [ ] All tests pass locally
- [ ] Version bumped in `pyproject.toml` and `openmux/__init__.py`
- [ ] CHANGELOG.md updated with changes
- [ ] Documentation updated (if needed)
- [ ] Breaking changes documented
- [ ] Migration guide provided (if breaking changes)

### Workflow Summary

```
feature/my-feature
    ↓ (PR + merge)
develop ──────────► TestPyPI (test.pypi.org)
    ↓ (PR + merge)
main ─────────────► PyPI (pypi.org) + GitHub Release
```

### Emergency Hotfix

For critical bugs in production:

```bash
# Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b fix/critical-bug

# Fix the bug, bump patch version (e.g., 0.2.0 → 0.2.1)

# Push and create PR to main
git push origin fix/critical-bug

# After merge to main, backport to develop
git checkout develop
git merge main
git push origin develop
```

---

## 📚 Additional Resources

- [Development Guide](docs/DEVELOPMENT_GUIDE.md)
- [Architecture Documentation](docs/ARCHITECTURE.md)
- [Testing Strategy](docs/TESTING_STRATEGY.md)
- [CI/CD Workflow Guide](.github/WORKFLOW_GUIDE.md)
- [GitHub Secrets Setup](.github/SECRETS_SETUP.md)

---

## 🆘 Need Help?

- Check existing [issues](https://github.com/mdnu838/OpenMux/issues)
- Review [documentation](docs/)
- Ask in [GitHub Discussions](https://github.com/mdnu838/OpenMux/discussions)
- Reach out to maintainers

---

## 🙏 Thank You!

Thank you for contributing to OpenMux! Your efforts help make this project better for everyone. 🚀
