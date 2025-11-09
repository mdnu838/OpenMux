# GitHub Actions Workflow Setup

## 📁 CI/CD Workflow File

The GitHub Actions workflow file is located at:
```
.github/workflows/ci.yml
```

## ⚠️ Important Note

This workflow file **cannot be pushed** with the current GitHub token because it lacks the `workflow` scope.

## 🔧 Setup Options

### Option 1: Manual Upload (Recommended)

1. Go to your GitHub repository
2. Navigate to `.github/workflows/`
3. Click "Add file" → "Upload files"
4. Upload `ci.yml` from your local `.github/workflows/` directory
5. Commit directly to `mvp-alpha` branch

### Option 2: Update GitHub Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Edit your existing token or create a new one
3. Enable the `workflow` scope
4. Update your local git credentials
5. Push the workflow file:
   ```bash
   git add .github/workflows/ci.yml
   git commit -m "ci: Add GitHub Actions workflow for automated testing"
   git push origin mvp-alpha
   ```

### Option 3: Create via GitHub UI

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Click "New workflow"
4. Choose "Set up a workflow yourself"
5. Copy the contents from `.github/workflows/ci.yml`
6. Save and commit

## 🎯 What the Workflow Does

The CI/CD pipeline automatically:

- ✅ Tests on Python 3.9, 3.10, 3.11, 3.12, 3.13
- ✅ Runs unit tests and integration tests
- ✅ Checks code formatting with Black
- ✅ Lints code with Ruff
- ✅ Performs security scanning with Bandit
- ✅ Builds and verifies the package
- ✅ Uploads coverage to Codecov (optional)

## 🚀 Trigger Events

The workflow runs on:
- Push to `main`, `mvp-alpha`, or `develop` branches
- Pull requests to `main`, `mvp-alpha`, or `develop` branches

## 📋 Required Secrets (Optional)

For full functionality, add these secrets in GitHub Settings → Secrets:

- `CODECOV_TOKEN`: For coverage reporting (optional)

## ✅ Verification

Once uploaded, you can verify the workflow:

1. Go to your repository
2. Click "Actions" tab
3. You should see "CI/CD Pipeline" workflow
4. Make a test commit to trigger it

## 🔍 Status Badge

After the workflow is active, add this badge to your README:

```markdown
[![CI/CD](https://github.com/mdnu838/openmux/actions/workflows/ci.yml/badge.svg)](https://github.com/mdnu838/openmux/actions/workflows/ci.yml)
```

---

**The workflow file is ready to use - just needs to be uploaded to GitHub!**
