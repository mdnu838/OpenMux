# Contributing to OpenMux

Thank you for your interest in contributing to OpenMux! This document provides guidelines and instructions for contributing.

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Task Selection](#task-selection)
- [Testing Requirements](#testing-requirements)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Documentation](#documentation)

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
git clone https://github.com/yourusername/openmux.git
cd openmux

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"

# Verify setup
pytest tests/unit -v
```

---

## � Branching Strategy & Pull Requests

**IMPORTANT**: All feature changes require a separate branch and a Pull Request to `main`.

### Branch Structure

```
main (production-ready, protected)
├── mvp-alpha (alpha testing, protected)
├── develop (integration branch)
└── feature/* (feature branches)
    ├── feature/new-provider
    ├── bugfix/fix-selector
    └── docs/update-readme
```

### Branch Types & Naming

- **`feature/*`**: New features (e.g., `feature/add-anthropic-provider`)
- **`bugfix/*`**: Bug fixes (e.g., `bugfix/fix-selector-method`)
- **`hotfix/*`**: Critical production fixes (e.g., `hotfix/security-patch`)
- **`docs/*`**: Documentation updates (e.g., `docs/update-api-guide`)
- **`test/*`**: Test improvements (e.g., `test/add-combiner-tests`)
- **`refactor/*`**: Code refactoring (e.g., `refactor/simplify-router`)

### Creating a Feature Branch

```bash
# Always start from latest main or develop
git checkout main
git pull origin main

# Create your feature branch
git checkout -b feature/your-feature-name

# Make changes, commit regularly
git add .
git commit -m "feat: add new feature"

# Push to GitHub
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Pull Request Requirements

**Every PR MUST**:
- ✅ Pass all CI/CD checks
- ✅ Include tests for new code
- ✅ Maintain ≥90% code coverage
- ✅ Be reviewed and approved by a maintainer
- ✅ Have no merge conflicts
- ✅ Follow conventional commit format
- ✅ Update documentation if needed

### PR Title Format

Use conventional commits:
```
<type>: <description>

Examples:
feat: Add Anthropic Claude provider
fix: Resolve selector method name mismatch
docs: Update installation guide
test: Add router integration tests
```

---

## �🔄 Development Workflow

### 1. Choose a Task
- Review `docs/TASK_BREAKDOWN.md`
- Select a task that matches your skill level
- Check that dependencies are complete
- Comment on the task to claim it

### 2. Create a Branch
```bash
git checkout -b task-X.Y-brief-description
```

### 3. Implement Changes (TDD)

#### Write Tests First
```python
# tests/unit/test_module/test_feature.py
def test_new_feature():
    """Test the new feature."""
    result = new_feature("input")
    assert result == "expected_output"
```

#### Implement Code
```python
# openmux/module/feature.py
def new_feature(input: str) -> str:
    """Implement the feature.
    
    Args:
        input: The input string
        
    Returns:
        The processed output
    """
    return process(input)
```

#### Run Tests
```bash
# Run specific test
pytest tests/unit/test_module/test_feature.py -v

# Run with coverage
pytest --cov=openmux.module.feature --cov-report=term

# Debug if needed
pytest -s --pdb
```

### 4. Ensure Quality

```bash
# Format code
black openmux/ tests/
isort openmux/ tests/

# Lint code
ruff check openmux/
mypy openmux/

# Check test coverage
pytest --cov=openmux --cov-fail-under=90
```

### 5. Commit Changes
```bash
git add .
git commit -m "Task X.Y: Brief description

- Detailed change 1
- Detailed change 2
- Test coverage: 95%

Closes #issue_number"
```

### 6. Push and Create PR
```bash
git push origin task-X.Y-brief-description
```
Then create a Pull Request on GitHub.

---

## 📝 Task Selection

### Task Categories

#### 🟢 Good First Tasks
- Documentation improvements
- Adding test cases
- Fixing typos or formatting
- Simple bug fixes

#### 🟡 Intermediate Tasks
- Implementing new providers
- Adding utility functions
- Enhancing existing features
- Writing integration tests

#### 🔴 Advanced Tasks
- Core orchestration logic
- Performance optimizations
- Architecture changes
- Complex algorithm implementations

### Task Dependencies
Always check `docs/TASK_BREAKDOWN.md` for:
- Task dependencies (must be completed first)
- Estimated effort
- Required skills
- Deliverables

---

## 🧪 Testing Requirements

### Test Coverage Standards
- **Overall**: 90% minimum
- **Core modules**: 95% minimum
- **New code**: 100% coverage required

### Test Types Required

#### 1. Unit Tests (Always Required)
```python
class TestNewFeature:
    def test_basic_functionality(self):
        """Test basic operation."""
        pass
    
    def test_error_handling(self):
        """Test error cases."""
        pass
    
    def test_edge_cases(self):
        """Test boundary conditions."""
        pass
```

#### 2. Integration Tests (When Applicable)
```python
@pytest.mark.integration
class TestFeatureIntegration:
    def test_integration_with_other_module(self):
        """Test integration between modules."""
        pass
```

#### 3. Debug Checks (Always Required)
Every test must include diagnostic information:
```python
def test_with_debug_info(self):
    """Test with debugging information."""
    result = process(input_data)
    assert result == expected, (
        f"Failed: expected {expected}, got {result}\n"
        f"Input: {input_data}\n"
        f"State: {self.feature.__dict__}"
    )
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific category
pytest tests/unit
pytest tests/integration

# Run with coverage
pytest --cov=openmux --cov-report=html

# Run in watch mode (requires pytest-watch)
ptw
```

---

## 🎨 Code Style

### Python Style Guidelines

#### Type Hints (Required)
```python
from typing import Optional, List, Dict, Any

def process_query(
    query: str,
    config: Optional[Dict[str, Any]] = None
) -> str:
    """Process a query."""
    pass
```

#### Docstrings (Required)
```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description.
    
    Longer description explaining the function's purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When validation fails
        RuntimeError: When processing fails
        
    Examples:
        >>> function_name("test", 5)
        True
    """
    pass
```

#### Code Organization
```python
# 1. Imports (grouped and sorted)
from __future__ import annotations

import os
import sys
from pathlib import Path

from typing import Optional, Dict, Any

from openmux.core import Base
from openmux.utils import logger

# 2. Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# 3. Classes
class MyClass:
    """Class implementation."""
    pass

# 4. Functions
def my_function():
    """Function implementation."""
    pass
```

### Formatting Tools
```bash
# Auto-format with black
black openmux/ tests/

# Sort imports with isort
isort openmux/ tests/

# Lint with ruff
ruff check openmux/

# Type check with mypy
mypy openmux/
```

---

## 🔍 Pull Request Process

### Before Creating PR

#### Checklist
- [ ] All tests pass locally
- [ ] Code coverage >= 90%
- [ ] Code formatted (black, isort)
- [ ] Linting passes (ruff, mypy)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No merge conflicts with main

### PR Template
```markdown
## Description
Brief description of changes

## Related Task
Closes Task X.Y from docs/TASK_BREAKDOWN.md

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing locally
- [ ] Coverage >= 90%

## Documentation
- [ ] Code documented (docstrings)
- [ ] README updated (if needed)
- [ ] API docs updated (if needed)
- [ ] CHANGELOG.md updated

## Screenshots/Examples
(if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] No new warnings
- [ ] Dependent tasks completed
```

### Review Process
1. **Automated Checks**: CI must pass
2. **Code Review**: At least one approval required
3. **Testing**: Reviewer verifies tests are comprehensive
4. **Documentation**: Reviewer checks documentation updates
5. **Approval**: Maintainer approves and merges

---

## 📚 Documentation

### Documentation Requirements

#### Code Documentation
Every module, class, and function must have docstrings following Google style.

#### README Updates
Update README.md when:
- Adding new features
- Changing installation process
- Modifying usage examples
- Updating dependencies

#### API Documentation
Update `docs/api_reference.md` when:
- Adding public APIs
- Changing function signatures
- Adding new modules

#### Architecture Documentation
Update `docs/ARCHITECTURE.md` when:
- Adding new components
- Changing data flow
- Modifying system design

---

## 🐛 Reporting Bugs

### Bug Report Template
```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Step 1
2. Step 2
3. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., macOS 14]
- Python: [e.g., 3.11]
- OpenMux version: [e.g., 0.1.0]

**Logs/Screenshots**
Any relevant logs or screenshots

**Additional Context**
Any other relevant information
```

---

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How would this feature work?

**Alternatives Considered**
What other solutions did you consider?

**Additional Context**
Any other relevant information
```

---

## ❓ Questions & Support

### Getting Help
- **Documentation**: Check `docs/` folder
- **GitHub Discussions**: Ask questions
- **GitHub Issues**: Report bugs
- **Code Comments**: Read inline documentation

### Communication Guidelines
- Be clear and concise
- Provide context and examples
- Be patient and respectful
- Search existing issues/discussions first

---

## 🎓 Learning Resources

### For Contributors
- [Python Style Guide (PEP 8)](https://peps.python.org/pep-0008/)
- [Git Best Practices](https://www.git-scm.com/book/en/v2)
- [Testing Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Type Hints Guide](https://docs.python.org/3/library/typing.html)

### Project-Specific
- `docs/DEVELOPMENT_GUIDE.md` - Development setup and workflow
- `docs/TASK_BREAKDOWN.md` - Detailed task list
- `docs/TESTING_STRATEGY.md` - Testing guidelines
- `docs/ARCHITECTURE.md` - System architecture

---

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation
- Thanked in the community

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Thank you for contributing to OpenMux! Your efforts help make this project better for everyone.