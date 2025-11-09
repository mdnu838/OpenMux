# OpenMux Documentation

Welcome to the OpenMux documentation! This directory contains comprehensive guides and references for using and contributing to OpenMux.

---

## 📚 Documentation Index

### For Users

- **[Quick Reference](QUICK_REFERENCE.md)** - Common tasks and commands at a glance
- **[Architecture](ARCHITECTURE.md)** - System design and component overview
- **[Project Definition](PROJECT_DEFINITION.md)** - Original project requirements and specifications

### For Developers

- **[Development Guide](DEVELOPMENT_GUIDE.md)** - Complete development setup and workflow
- **[Testing Strategy](TESTING_STRATEGY.md)** - Testing guidelines and best practices
- **[Project Structure](PROJECT_STRUCTURE.md)** - Codebase organization and structure

### For Contributors

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) in the root directory for:
- Branch strategy and workflow
- Commit message conventions
- Pull request process
- Release procedures

### For Maintainers

See the `.github/` directory for:
- **[Workflow Guide](../.github/WORKFLOW_GUIDE.md)** - CI/CD pipeline details
- **[Repository Setup](../.github/REPOSITORY_SETUP.md)** - GitHub configuration
- **[Secrets Setup](../.github/SECRETS_SETUP.md)** - Required secrets configuration

---

## 🚀 Quick Start

### Installation

```bash
# From PyPI (stable)
pip install openmux

# From TestPyPI (testing)
pip install -i https://test.pypi.org/simple/ openmux

# From source (development)
git clone https://github.com/mdnu838/OpenMux.git
cd OpenMux
uv pip install -e ".[dev]"
```

### Basic Usage

```python
from openmux import Orchestrator

# Initialize orchestrator
orchestrator = Orchestrator(api_key="your-openrouter-key")

# Process a query
result = orchestrator.process("Explain quantum computing")
print(result["response"])
```

---

## 📖 Documentation Organization

```
docs/
├── README.md                    # This file - documentation index
├── QUICK_REFERENCE.md          # Quick command reference
├── ARCHITECTURE.md             # System architecture
├── DEVELOPMENT_GUIDE.md        # Development workflow
├── TESTING_STRATEGY.md         # Testing guidelines
├── PROJECT_STRUCTURE.md        # Code organization
└── PROJECT_DEFINITION.md       # Original requirements
```

---

## 🔄 Workflow Overview

```
Development Flow:
feature/* → develop → TestPyPI (for testing)
develop → main → PyPI (production release)

Testing:
pytest tests/unit/              # Unit tests
pytest tests/integration/       # Integration tests
pytest --cov=openmux           # With coverage
```

---

## 🆘 Need Help?

1. **Check the docs** - Start with [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. **Search issues** - [GitHub Issues](https://github.com/mdnu838/OpenMux/issues)
3. **Ask questions** - [GitHub Discussions](https://github.com/mdnu838/OpenMux/discussions)
4. **Read the code** - Well-documented source code

---

## 📝 Documentation Standards

When contributing documentation:

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Keep examples up-to-date
- Link between related docs
- Follow Markdown best practices

---

## 🔗 External Resources

- **PyPI**: https://pypi.org/project/openmux/
- **TestPyPI**: https://test.pypi.org/project/openmux/
- **GitHub**: https://github.com/mdnu838/OpenMux
- **OpenRouter**: https://openrouter.ai/

---

Last updated: November 2025
