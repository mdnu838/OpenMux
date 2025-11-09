# GitHub Secrets Setup

This document describes the GitHub secrets required for the OpenMux CI/CD workflows.

## Required Secrets

### 1. OPENROUTER_API_KEY
- **Used in**: `.github/workflows/ci.yml`
- **Purpose**: Enables live integration testing with OpenRouter API
- **Required**: Recommended (tests will skip if not provided)
- **How to get**: Sign up at [OpenRouter](https://openrouter.ai/) and generate an API key
- **Setup**:
  1. Go to your GitHub repository settings
  2. Navigate to Secrets and variables → Actions
  3. Click "New repository secret"
  4. Name: `OPENROUTER_API_KEY`
  5. Value: Your OpenRouter API key (starts with `sk-or-v1-...`)
  6. Click "Add secret"

### 2. TESTPYPI_TOKEN
- **Used in**: `.github/workflows/publish.yml`
- **Purpose**: Publish package to TestPyPI
- **Required**: Yes (for TestPyPI publishing)
- **How to get**: 
  1. Create account at [TestPyPI](https://test.pypi.org/)
  2. Go to Account Settings → API tokens
  3. Create a new API token
- **Setup**:
  1. Go to your GitHub repository settings
  2. Navigate to Secrets and variables → Actions
  3. Click "New repository secret"
  4. Name: `TESTPYPI_TOKEN`
  5. Value: Your TestPyPI API token (starts with `pypi-...`)
  6. Click "Add secret"

### 3. PYPI_TOKEN
- **Used in**: `.github/workflows/publish.yml`
- **Purpose**: Publish package to production PyPI
- **Required**: Yes (for PyPI publishing on releases)
- **How to get**: 
  1. Create account at [PyPI](https://pypi.org/)
  2. Go to Account Settings → API tokens
  3. Create a new API token
- **Setup**:
  1. Go to your GitHub repository settings
  2. Navigate to Secrets and variables → Actions
  3. Click "New repository secret"
  4. Name: `PYPI_TOKEN`
  5. Value: Your PyPI API token (starts with `pypi-...`)
  6. Click "Add secret"

### 4. CODECOV_TOKEN (Optional)
- **Used in**: `.github/workflows/ci.yml`
- **Purpose**: Upload test coverage reports to Codecov
- **Required**: No (coverage upload will fail gracefully if not provided)
- **How to get**:
  1. Sign up at [Codecov](https://codecov.io/)
  2. Add your GitHub repository
  3. Copy the upload token
- **Setup**:
  1. Go to your GitHub repository settings
  2. Navigate to Secrets and variables → Actions
  3. Click "New repository secret"
  4. Name: `CODECOV_TOKEN`
  5. Value: Your Codecov upload token
  6. Click "Add secret"

## Workflow Behavior

### CI Workflow (ci.yml)
- Runs on all pushes and pull requests to non-main branches
- **With OPENROUTER_API_KEY**: Runs unit tests, mock integration tests, and live integration tests
- **Without OPENROUTER_API_KEY**: Runs unit tests and mock integration tests only (live tests skipped)

### Publish Workflow (publish.yml)
- Runs on pushes to main branch
- **TestPyPI Publishing**: Requires `TESTPYPI_TOKEN`, uses auto-incremented version (0.1.<run_number>)
- **PyPI Publishing**: Requires `PYPI_TOKEN`, only runs on tagged releases

## Testing the Setup

After adding secrets, you can verify they work by:

1. **OPENROUTER_API_KEY**: Push to your branch and check if live integration tests run in the Actions tab
2. **TESTPYPI_TOKEN**: Merge to main and verify the package publishes to TestPyPI
3. **PYPI_TOKEN**: Create a release tag and verify the package publishes to PyPI

## Security Notes

- Never commit API keys or tokens to the repository
- GitHub secrets are encrypted and only exposed to workflows
- Secret values are masked in workflow logs
- Rotate API keys periodically for security
- Use fine-grained tokens where possible (scoped to specific packages)
