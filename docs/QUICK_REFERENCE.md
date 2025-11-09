# OpenMux - Quick Reference

Quick reference for common tasks and commands.

---

## 🚀 Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/openmux.git
cd openmux
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit

# Run with coverage
pytest --cov=openmux --cov-report=html

# Run specific test
pytest tests/unit/test_orchestrator.py -v

# Debug mode
pytest -s --pdb

# Watch mode
ptw
```

---

## 🎨 Code Quality

```bash
# Format code
black openmux/ tests/
isort openmux/ tests/

# Lint
ruff check openmux/
mypy openmux/

# Run all checks
./scripts/check_all.sh
```

---

## 📝 Git Workflow

```bash
# Create feature branch
git checkout -b task-X.Y-feature-name

# Commit changes
git add .
git commit -m "Task X.Y: Brief description"

# Push and create PR
git push origin task-X.Y-feature-name
```

---

## 📚 Documentation

### File Locations
- **User Docs**: `docs/`
- **API Reference**: `docs/api_reference.md`
- **Examples**: `docs/examples/`
- **Architecture**: `docs/ARCHITECTURE.md`
- **Tasks**: `docs/TASK_BREAKDOWN.md`

### Updating Docs
1. Edit relevant .md file
2. Update index if needed
3. Test code examples
4. Submit PR

---

## 🔧 Common Commands

```bash
# Install dependencies
uv pip install -e ".[dev]"

# Update dependencies
uv pip compile requirements.txt -o uv.lock

# Clean build artifacts
find . -type d -name __pycache__ -exec rm -rf {} +
rm -rf .pytest_cache .coverage htmlcov

# Generate coverage report
pytest --cov=openmux --cov-report=html
open htmlcov/index.html
```

---

## 📋 Task Workflow

1. **Select Task**: Check `docs/TASK_BREAKDOWN.md`
2. **Create Branch**: `git checkout -b task-X.Y-name`
3. **Write Tests**: Create test file first
4. **Implement**: Write code to pass tests
5. **Debug**: Fix any issues
6. **Format**: Run black/isort
7. **Lint**: Run ruff/mypy
8. **Document**: Update docs
9. **Commit**: Write clear commit message
10. **PR**: Create pull request

---

## 🐛 Debugging

```bash
# Run with debug output
pytest -s

# Enter debugger on failure
pytest --pdb

# View logs
tail -f logs/openmux.log

# Check specific module
pytest tests/unit/test_module.py -v -s
```

---

## 📊 Performance

```bash
# Run benchmarks
pytest tests/benchmarks/ -m benchmark

# Profile code
python -m cProfile -o profile.stats script.py
python -m pstats profile.stats
```

---

## 🔍 Finding Things

```bash
# Find function definition
grep -r "def function_name" openmux/

# Find test
grep -r "test_feature" tests/

# Find TODO comments
grep -r "TODO" openmux/
```

---

## 📦 Building

```bash
# Build package
python -m build

# Install locally
pip install -e .

# Uninstall
pip uninstall openmux
```

---

## 🎯 Quick Links

- Tasks: `docs/TASK_BREAKDOWN.md`
- Architecture: `docs/ARCHITECTURE.md`
- Testing: `docs/TESTING_STRATEGY.md`
- Development: `docs/DEVELOPMENT_GUIDE.md`
- Contributing: `CONTRIBUTING.md`

---

## ⚡ Keyboard Shortcuts (pytest)

- `Ctrl+C` - Stop tests
- `-x` - Stop on first failure
- `-v` - Verbose output
- `-s` - Show print statements
- `--pdb` - Enter debugger on failure
- `-k "pattern"` - Run tests matching pattern

---

## 🔑 Environment Variables

```bash
# Set log level
export OPENCASCADE_LOG_LEVEL=DEBUG

# Set config path
export OPENCASCADE_CONFIG_PATH=/path/to/config

# Disable encryption
export OPENCASCADE_DISABLE_ENCRYPTION=1
```

---

## 📈 Coverage Targets

- Overall: 90%+
- Core: 95%+
- Providers: 85%+
- Utils: 95%+

---

## ✅ PR Checklist

- [ ] Tests pass
- [ ] Coverage >= 90%
- [ ] Code formatted
- [ ] Linting passes
- [ ] Docs updated
- [ ] CHANGELOG updated
- [ ] No merge conflicts