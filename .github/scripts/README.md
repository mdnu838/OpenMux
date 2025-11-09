# GitHub Actions Scripts

This folder contains helper scripts for CI/CD workflows.

## bump_version.py

Automatically increments the patch version number based on the GitHub Actions run number.

### Usage

```bash
python .github/scripts/bump_version.py <run_number>
```

### How It Works

1. Reads the current version from `pyproject.toml`
2. Extracts major and minor version numbers
3. Replaces the patch number with the GitHub run number
4. Updates both `pyproject.toml` and `openmux/__init__.py`

### Example

```bash
# Current version: 0.1.1
python .github/scripts/bump_version.py 42

# Result: 0.1.42
# - pyproject.toml: version = "0.1.42"
# - openmux/__init__.py: __version__ = "0.1.42"
```

### CI/CD Integration

This script is automatically called during the **Publish to PyPI** workflow when pushing to the `main` branch. It ensures each TestPyPI build has a unique version number, preventing upload conflicts.

### Version Strategy

- **TestPyPI** (automatic builds): `0.1.<run_number>` (e.g., 0.1.100, 0.1.101, 0.1.102)
- **PyPI** (releases): Semantic versioning (e.g., 0.1.1, 0.2.0, 1.0.0)

This allows unlimited test builds while maintaining clean semantic versioning for production releases.
