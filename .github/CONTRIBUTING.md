# Contributing to OpenMux

Thank you for your interest in contributing to OpenMux! This document provides guidelines and instructions for contributing.

## Development Workflow

### Branch Strategy

We follow a simplified Git Flow model:

- **`main`**: Production-ready code. Protected branch requiring PR reviews.
- **`develop`**: Integration branch for features. Tested code ready for next release.
- **`feature/*`**: New features (e.g., `feature/add-new-provider`)
- **`fix/*`**: Bug fixes (e.g., `fix/classifier-accuracy`)
- **`docs/*`**: Documentation updates (e.g., `docs/api-reference`)
- **`chore/*`**: Maintenance tasks (e.g., `chore/update-dependencies`)

### Creating a New Branch

```bash
# For a new feature
git checkout -b feature/your-feature-name develop

# For a bug fix
git checkout -b fix/issue-description develop

# For documentation
git checkout -b docs/doc-update develop
```

### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(classifier): Add support for image classification tasks

fix(orchestrator): Handle timeout errors gracefully

docs(readme): Update installation instructions

chore(deps): Upgrade transformers to v4.35.0
```

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/mdnu838/OpenMux.git
cd OpenMux
```

### 2. Set Up Development Environment

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### 3. Configure Git

```bash
# Add upstream remote
git remote add upstream https://github.com/mdnu838/OpenMux.git

# Keep your fork in sync
git fetch upstream
git checkout main
git merge upstream/main
```

## Making Changes

### 1. Create a Branch

```bash
git checkout develop
git pull upstream develop
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, readable code
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Add type hints where applicable
- Write or update tests for your changes

### 3. Test Your Changes

```bash
# Run unit tests
pytest tests/unit/ -v

# Run integration tests (with mocks)
pytest tests/integration/test_orchestrator_mock.py -v

# Run with coverage
pytest tests/unit/ tests/integration/test_orchestrator_mock.py \
  --cov=openmux \
  --cov-report=term-missing

# Run live integration tests (requires OPENROUTER_API_KEY)
export OPENROUTER_API_KEY=your_key_here
pytest tests/integration/test_openrouter_live.py -v
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat(scope): Brief description of your change"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub from your branch to `develop`.

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow convention
- [ ] Branch is up-to-date with develop

### PR Description

Include:
1. **What** - What changes does this PR make?
2. **Why** - Why are these changes needed?
3. **How** - How did you implement the changes?
4. **Testing** - How was this tested?
5. **Screenshots** - If UI changes (not applicable for this project yet)

### Review Process

1. Automated CI checks must pass
2. At least one maintainer approval required
3. No merge conflicts with target branch
4. All review comments addressed

## Code Style Guidelines

### Python Style

- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters (flexible to 120 for readability)
- Use type hints for function signatures
- Use docstrings (Google style preferred)

### Example

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

### Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Update CHANGELOG.md (if exists)

## Testing Guidelines

### Test Structure

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_classifier.py
│   └── test_orchestrator.py
├── integration/             # Integration tests
│   ├── test_orchestrator_mock.py    # Mock-based
│   └── test_openrouter_live.py      # Live API
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

## Debugging

### Running Specific Tests

```bash
# Run specific test file
pytest tests/unit/test_classifier.py -v

# Run specific test function
pytest tests/unit/test_classifier.py::test_task_classification -v

# Run with debug output
pytest tests/unit/ -v -s --tb=long
```

### Common Issues

1. **Import errors**: Ensure package is installed in editable mode: `uv pip install -e .`
2. **Test failures**: Check if dependencies are up to date: `uv pip install -e ".[dev]"`
3. **Async errors**: Ensure pytest-asyncio is installed

## Release Process (Maintainers Only)

1. Ensure all changes are merged to `develop`
2. Run full test suite including live integration tests
3. Update version in `pyproject.toml` and `openmux/__init__.py`
4. Update CHANGELOG.md
5. Create PR from `develop` to `main`
6. After merge, tag the release:
   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```
7. GitHub Actions will automatically publish to PyPI

## Need Help?

- Check existing issues and discussions
- Review documentation in `docs/`
- Ask questions in GitHub Discussions
- Reach out to maintainers

## Code of Conduct

Be respectful, inclusive, and professional. We're all here to build great software together.

Thank you for contributing to OpenMux! 🚀
