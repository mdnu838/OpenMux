# Publishing OpenMux to PyPI

This guide explains how to publish OpenMux to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**
   - Create account at https://pypi.org/account/register/
   - Verify your email

2. **Test PyPI Account** (recommended for testing)
   - Create account at https://test.pypi.org/account/register/

3. **API Tokens**
   - Get PyPI API token: https://pypi.org/manage/account/token/
   - Get TestPyPI token: https://test.pypi.org/manage/account/token/

## Setup

### 1. Install Build Tools

```bash
uv pip install build twine
```

### 2. Configure PyPI Credentials

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

**Important**: Replace `YOUR_PYPI_TOKEN_HERE` with your actual tokens.

## Publishing Process

### Step 1: Clean Previous Builds

```bash
cd /Users/nizamuddin/Documents/Project/Smart-Model-selector
rm -rf dist/ build/ *.egg-info
```

### Step 2: Build the Package

```bash
python -m build
```

This creates:
- `dist/openmux-0.1.0a0-py3-none-any.whl` (wheel)
- `dist/openmux-0.1.0a0.tar.gz` (source distribution)

### Step 3: Validate the Build

```bash
twine check dist/*
```

Should show: `PASSED` for all files.

### Step 4: Test on TestPyPI (Recommended First)

```bash
twine upload --repository testpypi dist/*
```

Then test installation:

```bash
uv pip install --index-url https://test.pypi.org/simple/ openmux
```

### Step 5: Upload to PyPI

Once tested:

```bash
twine upload dist/*
```

### Step 6: Verify Installation

```bash
uv pip install openmux
python -c "import openmux; print(openmux.__version__)"
```

## Version Management

Update version in `pyproject.toml`:

```toml
[project]
name = "openmux"
version = "0.1.0"  # Update this for new releases
```

Version naming:
- `0.1.0a0` - Alpha release
- `0.1.0b0` - Beta release
- `0.1.0rc0` - Release candidate
- `0.1.0` - Stable release

## Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
      run: twine upload dist/*
```

Add `PYPI_TOKEN` to GitHub Secrets:
1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `PYPI_TOKEN`
4. Value: Your PyPI API token

## Manual Publishing Steps

### Quick Command Reference

```bash
# 1. Clean
rm -rf dist/ build/ *.egg-info

# 2. Build
python -m build

# 3. Check
twine check dist/*

# 4. Test (optional)
twine upload --repository testpypi dist/*

# 5. Publish
twine upload dist/*
```

## Troubleshooting

### "File already exists"

If version exists on PyPI:
1. Update version in `pyproject.toml`
2. Rebuild: `python -m build`
3. Upload again

### "Invalid credentials"

1. Check `~/.pypirc` configuration
2. Verify API token is correct
3. Token should start with `pypi-`

### "Package name not available"

1. Choose a different name in `pyproject.toml`
2. Check availability: https://pypi.org/project/YOUR_NAME/

## Post-Publication

### 1. Create GitHub Release

```bash
git tag v0.1.0
git push origin v0.1.0
```

Then create release on GitHub with changelog.

### 2. Update Documentation

Add PyPI badge to README.md:

```markdown
[![PyPI version](https://badge.fury.io/py/openmux.svg)](https://pypi.org/project/openmux/)
[![Downloads](https://pepy.tech/badge/openmux)](https://pepy.tech/project/openmux)
```

### 3. Announce

- Update README with installation instructions
- Share on social media
- Post on relevant forums/communities

## Security Notes

- **Never commit** `~/.pypirc` to version control
- Use API tokens, not passwords
- Rotate tokens periodically
- Use TestPyPI for testing

## Resources

- PyPI: https://pypi.org/
- TestPyPI: https://test.pypi.org/
- Packaging Guide: https://packaging.python.org/
- Twine Docs: https://twine.readthedocs.io/

---

**Ready to publish? Follow the steps above!**
