# CI/CD Workflow Guide

## Overview

OpenMux uses a streamlined CI/CD pipeline with two main workflows:

```
┌─────────────────┐
│ Feature Branch  │
└────────┬────────┘
         │ (PR)
         ▼
┌─────────────────┐      Push      ┌──────────────┐
│    develop      │ ─────────────► │  TestPyPI    │
└────────┬────────┘   (automatic)  └──────────────┘
         │ (PR)
         ▼
┌─────────────────┐      Push      ┌──────────────┐      ┌─────────────┐
│      main       │ ─────────────► │     PyPI     │ ────►│ GitHub      │
└─────────────────┘   (automatic)  └──────────────┘      │ Release     │
                                                          └─────────────┘
```

## Workflows

### 1. CI Tests (`ci.yml`)

**Triggers:**
- Push to: `develop`, `feature/*`, `fix/*`, `docs/*`, `chore/*`
- Pull requests to: `main`, `develop`

**Jobs:**
- ✅ Run tests on Python 3.9-3.13
- ✅ Code linting (Black, Ruff, mypy)
- ✅ Security scanning (Bandit, Safety)
- ✅ Build package verification
- ✅ Coverage reporting

**Does NOT publish packages** - testing only!

### 2. Publish Package (`publish.yml`)

**Triggers:**
- Push to `develop` → Publishes to **TestPyPI**
- Push to `main` → Publishes to **PyPI** + Creates GitHub Release

**Jobs:**
- ✅ Build package
- ✅ Run package checks
- ✅ Publish to appropriate registry
- ✅ Create release (main only)
- ✅ Upload artifacts

## Version Management

### Important: Manual Versioning Only

Both TestPyPI and PyPI use the **same version** from `pyproject.toml`. No auto-incrementing.

**Version Format:** `MAJOR.MINOR.PATCH` (Semantic Versioning)

```toml
# pyproject.toml
[project]
version = "0.2.0"
```

```python
# openmux/__init__.py
__version__ = "0.2.0"
```

⚠️ **Both files must match!**

## Development Workflow

### Step 1: Develop Features

```bash
# Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/my-new-feature

# Make changes, commit
git add .
git commit -m "feat: Add awesome feature"
git push origin feature/my-new-feature

# Create PR: feature/my-new-feature → develop
```

**What happens:** CI tests run automatically

### Step 2: Test on TestPyPI

```bash
# After PR is merged to develop
git checkout develop
git pull origin develop

# Bump version for testing
# Edit: pyproject.toml and openmux/__init__.py
# Example: 0.1.0 → 0.2.0-beta.1

git add pyproject.toml openmux/__init__.py CHANGELOG.md
git commit -m "chore: Bump version to 0.2.0-beta.1"
git push origin develop
```

**What happens automatically:**
1. CI tests run
2. Package builds
3. Publishes to TestPyPI
4. You can test: `pip install -i https://test.pypi.org/simple/ openmux==0.2.0-beta.1`

### Step 3: Release to Production

```bash
# When ready for production release
# Update version to stable (remove -beta suffix)
# Edit: pyproject.toml and openmux/__init__.py
# Example: 0.2.0-beta.1 → 0.2.0

git checkout develop
git add pyproject.toml openmux/__init__.py CHANGELOG.md
git commit -m "chore: Release version 0.2.0"
git push origin develop

# Create PR: develop → main
# After review and approval, merge to main
```

**What happens automatically:**
1. CI tests run
2. Package builds
3. Publishes to PyPI
4. Creates GitHub Release (tag: v0.2.0)
5. Users can install: `pip install openmux==0.2.0`

## Version Bumping Strategy

### Pre-release (develop → TestPyPI)

Use pre-release suffixes for testing:

- `0.2.0-alpha.1` - Early development
- `0.2.0-beta.1` - Feature complete, testing
- `0.2.0-rc.1` - Release candidate

### Stable Release (main → PyPI)

Use clean version numbers:

- `0.2.0` - Minor release (new features)
- `0.2.1` - Patch release (bug fixes)
- `1.0.0` - Major release (breaking changes)

## Common Scenarios

### Scenario 1: Testing a New Feature

```bash
# 1. Develop on feature branch
git checkout -b feature/cool-thing develop
# ... make changes ...
git push origin feature/cool-thing

# 2. PR to develop, merge

# 3. Test on TestPyPI
git checkout develop
# Bump to 0.2.0-beta.1
git push origin develop

# 4. Install and test
pip install -i https://test.pypi.org/simple/ openmux==0.2.0-beta.1

# 5. If good, release to production
# Bump to 0.2.0 (remove -beta)
# PR develop → main
```

### Scenario 2: Hotfix for Production

```bash
# 1. Create hotfix from main
git checkout -b fix/critical-bug main

# 2. Fix bug, bump patch version
# 0.2.0 → 0.2.1

# 3. Push and PR to main (skip develop)
git push origin fix/critical-bug

# 4. After merge to main
# Backport to develop
git checkout develop
git merge main
git push origin develop
```

### Scenario 3: Multiple Beta Versions

```bash
# First beta
# Version: 0.2.0-beta.1
git push origin develop
# → TestPyPI

# Found issues, fixed them
# Version: 0.2.0-beta.2
git push origin develop
# → TestPyPI (new version)

# Ready for production
# Version: 0.2.0
# PR develop → main
# → PyPI + GitHub Release
```

## Required GitHub Secrets

| Secret | Used By | Purpose |
|--------|---------|---------|
| `TESTPYPI_TOKEN` | publish.yml | Publish to TestPyPI |
| `PYPI_TOKEN` | publish.yml | Publish to PyPI |
| `OPENROUTER_API_KEY` | ci.yml | Live integration tests |
| `CODECOV_TOKEN` | ci.yml | Upload coverage reports |

See [SECRETS_SETUP.md](./SECRETS_SETUP.md) for details.

## Troubleshooting

### "Version already exists on TestPyPI"

TestPyPI doesn't allow re-uploading same version. Bump the version:
- `0.2.0-beta.1` → `0.2.0-beta.2`

### "Version already exists on PyPI"

PyPI never allows re-uploading. You must bump the version:
- `0.2.0` → `0.2.1` (patch bump)

### "GitHub Release already exists"

Delete the existing tag and release on GitHub, or bump the version.

### "CI tests failing"

Check the Actions tab on GitHub for detailed error logs. Common issues:
- Test failures (fix the code)
- Linting errors (run `black` and `ruff`)
- Import errors (check dependencies)

### "Package not appearing on PyPI"

- Check GitHub Actions logs
- Verify `PYPI_TOKEN` secret is correct
- Ensure version is bumped from previous release

## Best Practices

1. **Always test on TestPyPI first** before releasing to PyPI
2. **Use semantic versioning** (MAJOR.MINOR.PATCH)
3. **Update CHANGELOG.md** for every version
4. **Keep develop and main in sync** (don't skip commits)
5. **Tag releases** are automatic (created by workflow)
6. **Never push directly to main** (use PRs)
7. **Version consistency** - pyproject.toml and __init__.py must match

## Quick Commands

```bash
# Check current version
grep "^version = " pyproject.toml

# Test package build locally
uv venv
source .venv/bin/activate
uv pip install build
python -m build

# Install from TestPyPI
pip install -i https://test.pypi.org/simple/ openmux

# Install from PyPI
pip install openmux

# Check package info
pip show openmux
```

## Workflow Files

- `.github/workflows/ci.yml` - Tests and validation
- `.github/workflows/publish.yml` - Package publishing
- `.github/CONTRIBUTING.md` - Contribution guidelines
- `.github/SECRETS_SETUP.md` - Secrets configuration

---

**Need help?** Check the [Contributing Guide](./CONTRIBUTING.md) or open an issue.
