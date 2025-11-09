# OpenMux Development Guide

## Getting Started with Development

This guide covers everything you need to know to contribute to OpenMux development.

---

## 🚀 Initial Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/openmux.git
cd openmux
```

### 2. Set Up Development Environment
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"
```

### 3. Verify Installation
```bash
# Run tests to ensure everything is working
pytest tests/unit -v

# Check code formatting
black --check openmux/
isort --check openmux/

# Run linter
ruff check openmux/
```

---

## 🏗️ Development Workflow

### Task-Based Development
Each task follows this workflow:

```
1. Select Task → 2. Create Branch → 3. Write Tests → 4. Implement Code
        ↓                                                    ↓
8. Merge PR ← 7. Code Review ← 6. Run Full Tests ← 5. Debug & Fix
```

### Detailed Steps

#### Step 1: Select Task
- Review `docs/TASK_BREAKDOWN.md`
- Check task dependencies are complete
- Assign yourself the task

#### Step 2: Create Branch
```bash
# Create feature branch
git checkout -b task-X.Y-feature-name

# Example
git checkout -b task-1.1-config-system
```

#### Step 3: Write Tests First (TDD)
```bash
# Create test file
touch tests/unit/test_module/test_feature.py

# Write comprehensive tests
# - Unit tests for all functions
# - Edge cases
# - Error handling
# - Integration scenarios
```

#### Step 4: Implement Code
```bash
# Create implementation file
touch openmux/module/feature.py

# Implement to satisfy tests
# - Follow code style guidelines
# - Add docstrings
# - Include type hints
```

#### Step 5: Debug & Fix
```bash
# Run tests
pytest tests/unit/test_module/test_feature.py -v

# Run with coverage
pytest --cov=openmux.module.feature --cov-report=term

# Debug failing tests
pytest -s --pdb  # Enter debugger on failure
```

#### Step 6: Run Full Test Suite
```bash
# Run all unit tests
pytest tests/unit -v

# Run integration tests
pytest tests/integration -v

# Check coverage
pytest --cov=openmux --cov-report=html --cov-fail-under=90

# Format code
black openmux/ tests/
isort openmux/ tests/

# Lint code
ruff check openmux/
mypy openmux/
```

#### Step 7: Code Review
```bash
# Commit changes
git add .
git commit -m "Task X.Y: Feature description

- Implementation details
- Test coverage
- Related issues"

# Push to remote
git push origin task-X.Y-feature-name

# Create Pull Request
# - Fill out PR template
# - Link to task
# - Request review
```

#### Step 8: Merge
- Address review comments
- Ensure CI passes
- Squash and merge

---

## 📝 Code Style Guidelines

### Python Style
Follow PEP 8 with these specifics:

```python
# Use type hints
def process_query(query: str, config: Optional[Dict[str, Any]] = None) -> str:
    """Process a query and return response.
    
    Args:
        query: The input query to process
        config: Optional configuration overrides
        
    Returns:
        The processed response string
        
    Raises:
        ValueError: If query is empty
        ProcessingError: If processing fails
    """
    pass

# Use dataclasses for data structures
from dataclasses import dataclass
from typing import List

@dataclass
class ModelCapability:
    """Model capability metadata."""
    name: str
    tasks: List[str]
    max_tokens: int
    latency_ms: float = 0.0

# Use enums for constants
from enum import Enum

class TaskType(Enum):
    """Supported task types."""
    CHAT = "chat"
    CODE = "code"
    IMAGE = "image"

# Use context managers
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()

# Use f-strings for formatting
message = f"Processing query: {query[:50]}..."

# Use list/dict comprehensions
results = [process(item) for item in items if item.is_valid()]
```

### Naming Conventions
```python
# Classes: PascalCase
class ModelSelector:
    pass

# Functions/methods: snake_case
def select_model():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3

# Private methods: _leading_underscore
def _internal_helper():
    pass

# Module-level private: _leading_underscore
_MODULE_CONSTANT = "value"
```

### Documentation
Every module, class, and function must have docstrings:

```python
"""
Module docstring.

This module provides functionality for...
"""

class Example:
    """Class docstring.
    
    Detailed description of what this class does.
    
    Attributes:
        attr1: Description of attr1
        attr2: Description of attr2
    """
    
    def method(self, param: str) -> int:
        """Method docstring.
        
        Args:
            param: Description of parameter
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When validation fails
        """
        pass
```

---

## 🧪 Testing Guidelines

### Test Structure
```python
# tests/unit/test_module/test_feature.py

import pytest
from openmux.module import Feature

class TestFeature:
    """Test suite for Feature class."""
    
    def setup_method(self):
        """Setup before each test method."""
        self.feature = Feature()
    
    def teardown_method(self):
        """Cleanup after each test method."""
        pass
    
    def test_basic_functionality(self):
        """Test basic feature operation."""
        result = self.feature.do_something("input")
        assert result == "expected"
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            self.feature.do_something(None)
    
    @pytest.mark.parametrize("input,expected", [
        ("a", "A"),
        ("b", "B"),
    ])
    def test_multiple_cases(self, input, expected):
        """Test multiple input cases."""
        assert self.feature.transform(input) == expected
```

### Test Naming
- `test_<feature>_<scenario>_<expected_result>`
- Examples:
  - `test_selector_valid_task_returns_provider`
  - `test_router_timeout_raises_exception`
  - `test_combiner_empty_list_returns_empty_string`

### Test Coverage Requirements
- **Minimum**: 90% overall
- **Target**: 95% for core modules
- **Every function** must have tests
- **Every error path** must be tested
- **Every branch** must be covered

---

## 🔍 Debugging Techniques

### Using pdb
```python
# Insert breakpoint in code
import pdb; pdb.set_trace()

# Or use built-in breakpoint (Python 3.7+)
breakpoint()
```

### Using pytest debugger
```bash
# Enter debugger on failure
pytest --pdb

# Enter debugger on first failure and stop
pytest -x --pdb
```

### Logging for Debugging
```python
from openmux.utils.logging import setup_logger

logger = setup_logger(__name__)

def debug_function():
    logger.debug(f"Input: {input_data}")
    logger.debug(f"State: {self.__dict__}")
    result = process(input_data)
    logger.debug(f"Result: {result}")
    return result
```

### Using print debugging (development only)
```python
# Pretty print data structures
import pprint
pprint.pprint(complex_dict)

# Print with context
print(f"DEBUG: {variable_name=}")
```

---

## 🔧 Common Development Tasks

### Adding a New Provider
1. Create `openmux/providers/new_provider.py`
2. Implement `BaseProvider` interface
3. Create `tests/unit/test_providers/test_new_provider.py`
4. Add provider to registry
5. Update documentation

```python
# openmux/providers/new_provider.py
from .base import BaseProvider

class NewProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "new_provider"
    
    async def is_available(self) -> bool:
        # Implementation
        pass
    
    # Implement other methods...
```

### Adding a New Task Type
1. Update `openmux/classifier/task_types.py`
2. Add to `TaskType` enum
3. Update classifier rules
4. Update tests
5. Update documentation

### Adding a New Combination Method
1. Update `openmux/core/combiner.py`
2. Implement new method
3. Add tests
4. Update documentation

---

## 🔄 Git Workflow

### Branch Naming
- `task-X.Y-description` - Feature branches
- `fix-issue-description` - Bug fixes
- `docs-description` - Documentation updates

### Commit Messages
```
Type: Brief description (50 chars or less)

Detailed explanation of what changed and why.
Can be multiple paragraphs.

- Bullet points for specific changes
- Reference issues: Fixes #123
- Include test coverage info
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Maintenance

### Pull Request Template
```markdown
## Description
Brief description of changes

## Task Reference
Closes Task X.Y from TASK_BREAKDOWN.md

## Changes Made
- Change 1
- Change 2

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing
- [ ] Coverage >= 90%

## Documentation
- [ ] Code documented
- [ ] README updated (if needed)
- [ ] API docs updated (if needed)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No console warnings/errors
- [ ] Documentation updated
```

---

## 🛠️ Useful Scripts

### Run all checks
```bash
# scripts/check_all.sh
#!/bin/bash
set -e

echo "Running tests..."
pytest tests/ -v

echo "Checking coverage..."
pytest --cov=openmux --cov-fail-under=90

echo "Formatting code..."
black openmux/ tests/
isort openmux/ tests/

echo "Linting..."
ruff check openmux/
mypy openmux/

echo "✅ All checks passed!"
```

### Update dependencies
```bash
# Update and regenerate lock file
uv pip compile requirements.txt -o uv.lock
uv pip sync uv.lock
```

### Clean build artifacts
```bash
# Remove build artifacts
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name '*.pyc' -delete
find . -type f -name '*.pyo' -delete
find . -type d -name '*.egg-info' -exec rm -rf {} +
rm -rf .pytest_cache
rm -rf .coverage
rm -rf htmlcov
```

---

## 📚 Learning Resources

### Python Best Practices
- [PEP 8](https://peps.python.org/pep-0008/) - Style Guide
- [PEP 257](https://peps.python.org/pep-0257/) - Docstring Conventions
- [Type Hints](https://docs.python.org/3/library/typing.html)

### Testing
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://realpython.com/pytest-python-testing/)

### Async Programming
- [Asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [aiohttp Documentation](https://docs.aiohttp.org/)

---

## 🐛 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Reinstall in development mode
uv pip install -e .
```

#### Test Failures
```bash
# Run specific test with verbose output
pytest tests/unit/test_file.py::test_function -vv -s
```

#### Coverage Issues
```bash
# Generate detailed coverage report
pytest --cov=openmux --cov-report=html
open htmlcov/index.html
```

#### Linting Errors
```bash
# Auto-fix with black and isort
black openmux/
isort openmux/

# Check remaining issues
ruff check openmux/ --fix
```

---

## 💡 Tips for Contributors

1. **Start Small**: Begin with small, well-defined tasks
2. **Read Existing Code**: Understand patterns before adding new code
3. **Ask Questions**: Use GitHub Discussions for clarifications
4. **Test Thoroughly**: Write tests before implementation
5. **Document Everything**: Code is read more than written
6. **Be Patient**: Code review takes time
7. **Stay Updated**: Pull latest changes regularly
8. **Follow Conventions**: Consistency is key

---

## 📞 Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and discussions
- **Documentation**: Check docs/ folder
- **Code Comments**: Read inline documentation

---

## ✅ Pre-Commit Checklist

Before every commit:
- [ ] Tests pass locally
- [ ] Code formatted (black, isort)
- [ ] Linting passes (ruff, mypy)
- [ ] Documentation updated
- [ ] Type hints added
- [ ] Docstrings complete
- [ ] No debug prints
- [ ] Commit message follows convention