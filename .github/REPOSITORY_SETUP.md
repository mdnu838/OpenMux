# GitHub Repository Configuration Guide

This guide will help you configure the OpenMux repository settings on GitHub.

## 🔒 Branch Protection Strategy

```
┌─────────────┐
│  feature/*  │  (Feature branches)
│   fix/*     │
│   docs/*    │
└──────┬──────┘
       │ PR (reviewed)
       ▼
┌─────────────┐      Auto-publish      ┌──────────────┐
│   develop   │ ──────────────────────►│  TestPyPI    │
└──────┬──────┘   (on push to develop) └──────────────┘
       │ PR (reviewed, tested)
       │ ❌ DIRECT PUSH DISABLED
       ▼
┌─────────────┐      Auto-publish      ┌──────────────┐
│    main     │ ──────────────────────►│     PyPI     │
│ (PROTECTED) │   (on push to main)    │ + Release    │
└─────────────┘                         └──────────────┘
    ↑
    │ ONLY accepts PRs from develop
    │ Direct pushes: BLOCKED
```

## 🎯 Quick Setup Checklist

- [ ] Set `main` as default branch
- [ ] Add branch protection rules for `main`
- [ ] Add GitHub secrets for CI/CD
- [ ] Configure branch protection for `develop` (optional)
- [ ] Set up issue and PR templates

---

## 1. Set Default Branch to `main`

**Why**: The default branch is what people see first and what PRs target by default.

**Steps**:
1. Go to your repository: https://github.com/mdnu838/OpenMux
2. Click **Settings** (top navigation)
3. Click **Branches** (left sidebar)
4. Under "Default branch", click the switch icon ⇄ next to current branch
5. Select **`main`** from the dropdown
6. Click **Update**
7. Confirm by clicking **"I understand, update the default branch"**

✅ **Done!** Now `main` is your default branch.

---

## 2. Branch Protection Rules for `main`

**Why**: Protect production code from direct pushes, require reviews and passing tests.

**Steps**:

### 2.1 Access Branch Protection
1. Go to **Settings → Branches**
2. Under "Branch protection rules", click **Add rule**
3. In "Branch name pattern", enter: `main`

### 2.2 Configure Protection Settings

**✅ Required:**
- ☑ **Require a pull request before merging**
  - ☑ Require approvals: `1` (or more for stricter review)
  - ☑ Dismiss stale pull request approvals when new commits are pushed
  - ☑ Require review from Code Owners (if you add CODEOWNERS file)

- ☑ **Require status checks to pass before merging**
  - ☑ Require branches to be up to date before merging
  - Select these status checks (after first CI run):
    - `test (3.9)`
    - `test (3.10)`
    - `test (3.11)`
    - `test (3.12)`
    - `test (3.13)`

- ☑ **Require conversation resolution before merging**

- ☑ **Restrict who can push to matching branches**
  - Add: No one (this prevents direct pushes entirely)
  - Note: This forces all changes to come via PRs from `develop` branch

- ☑ **Do not allow bypassing the above settings** (even for admins)

- ☑ **Lock branch** (optional, for maximum protection)
  - This makes the branch read-only except via PRs

**⚠️ Optional (Recommended):**
- ☑ Require linear history (clean commit history)
- ☑ Include administrators (apply rules to admins too)

**❌ Not recommended:**
- ☐ Require signed commits (unless you have GPG set up)
- ☐ Require deployments to succeed (not applicable yet)

### 2.3 Save Changes
Click **Create** (or **Save changes**)

---

## 3. Branch Protection for `develop` (Optional)

For the integration branch, use lighter protection:

1. **Settings → Branches → Add rule**
2. Branch name pattern: `develop`
3. Enable:
   - ☑ Require status checks to pass before merging
   - ☑ Require branches to be up to date before merging
4. **Save**

---

## 4. Add GitHub Secrets

Required for CI/CD workflows.

### 4.1 Access Secrets
1. Go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret** for each

### 4.2 Add These Secrets

| Secret Name | Required | Purpose | Where to Get |
|-------------|----------|---------|--------------|
| `OPENROUTER_API_KEY` | Recommended | Live integration tests | [OpenRouter Dashboard](https://openrouter.ai/) |
| `TESTPYPI_TOKEN` | Yes | Publish to TestPyPI | [TestPyPI Account Settings](https://test.pypi.org/manage/account/) |
| `PYPI_TOKEN` | Yes | Publish to PyPI | [PyPI Account Settings](https://pypi.org/manage/account/) |
| `CODECOV_TOKEN` | Optional | Upload coverage reports | [Codecov Dashboard](https://codecov.io/) |

**Detailed instructions**: See [.github/SECRETS_SETUP.md](./SECRETS_SETUP.md)

---

## 5. Verify Configuration

### 5.1 Check Default Branch
```bash
# Should show main as default
git remote show origin | grep "HEAD branch"
```

### 5.2 Test Branch Protection
Try to push directly to main (should fail):
```bash
git checkout main
echo "test" >> test.txt
git add test.txt
git commit -m "test direct push"
git push origin main  
# ❌ Should be rejected with:
# "refusing to allow a personal access token to push to a protected branch"
# or "protected branch hook declined"
```

Clean up:
```bash
git reset --hard HEAD~1
```

### 5.3 Verify PR-Only Access
```bash
# The ONLY way to update main is:
# 1. Create branch from develop
# 2. Make changes
# 3. PR to develop
# 4. After testing, PR from develop to main
```

---

## 6. Repository Settings (Additional)

### 6.1 General Settings
- **Settings → General**
  - ☑ Issues enabled
  - ☑ Allow merge commits
  - ☑ Allow squash merging (recommended)
  - ☑ Allow rebase merging
  - ☑ Automatically delete head branches (clean up after merge)

### 6.2 Actions Permissions
- **Settings → Actions → General**
  - ☑ Allow all actions and reusable workflows
  - ☑ Read and write permissions (for workflows)
  - ☑ Allow GitHub Actions to create and approve pull requests

---

## 7. Quick Command Reference

### Working with the protected branch structure:

```bash
# 1. Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/my-new-feature

# 2. Make changes and commit
git add .
git commit -m "feat: Add new feature"
git push origin feature/my-new-feature

# 3. Create PR on GitHub: feature/my-new-feature → develop
#    After review and merge to develop

# 4. Test on develop (auto-publishes to TestPyPI)
#    Verify everything works

# 5. Create PR on GitHub: develop → main
#    After review and merge to main
#    Auto-publishes to PyPI + creates GitHub Release
```

### ❌ This will FAIL (direct push blocked):
```bash
git checkout main
git push origin main  # ❌ ERROR: Protected branch
```

### ✅ This is the CORRECT way:
```bash
# Always go through develop
git checkout develop
git pull origin develop
# ... make changes via feature branches ...
# Create PR: feature → develop → main
```

### Update local repository:
```bash
# Sync all branches
git fetch origin

# Update main
git checkout main
git pull origin main

# Update develop
git checkout develop
git pull origin develop
```

---

## 8. Current Branch Structure

```
main (default, protected, PR-only from develop)
├── develop (integration branch, accepts PRs from features)
│   ├── feature/your-feature
│   ├── fix/bug-fix
│   ├── docs/documentation
│   └── chore/maintenance
└── [legacy branches can be deleted after migration]
    ├── mvp-alpha (can be deleted)
    └── docs-and-structure-update (can be deleted after merge)
```

### Branch Flow Rules

**Strict Workflow:**
```
feature/* → (PR) → develop → (PR) → main
fix/*     → (PR) → develop → (PR) → main
docs/*    → (PR) → develop → (PR) → main
chore/*   → (PR) → develop → (PR) → main
```

**Important:**
- ❌ **Direct pushes to `main` are DISABLED**
- ✅ Only PRs from `develop` branch can merge to `main`
- ✅ All feature work goes to `develop` first
- ✅ `develop` is tested on TestPyPI before merging to `main`
- ✅ `main` publishes to production PyPI

### Why This Workflow?

1. **Quality Control**: All code reviewed twice (feature→develop, develop→main)
2. **Testing**: Features tested on TestPyPI before production
3. **Stability**: Main branch always production-ready
4. **Rollback**: Easy to revert develop without affecting production

---

## 9. Clean Up Old Branches

After everything is set up and working:

```bash
# Delete local branches
git branch -d mvp-alpha
git branch -d docs-and-structure-update

# Delete remote branches (be careful!)
git push origin --delete mvp-alpha
git push origin --delete docs-and-structure-update
```

**⚠️ Warning**: Only delete branches after:
- All changes are merged to main/develop
- No open PRs reference these branches
- You've backed up any important work

---

## 10. Troubleshooting

### "Cannot change default branch"
- Make sure you have admin access to the repository
- Ensure the target branch exists on remote

### "Branch protection preventing push"
- This is expected! Create a PR instead
- Or temporarily disable protection (not recommended)

### "Status checks not showing up"
- Run CI workflow at least once
- Status checks appear after first successful run
- Check workflow file is on protected branch

### "Secrets not working in workflows"
- Verify secret names match exactly (case-sensitive)
- Check workflow has proper `secrets.SECRET_NAME` syntax
- Secrets from forks don't work (security feature)

---

## 📚 Additional Resources

- [GitHub Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

---

## ✅ Configuration Complete!

Once you've completed these steps, your repository will have:

✅ `main` as the default branch  
✅ Protection rules preventing direct pushes to `main`  
✅ Required status checks and PR reviews  
✅ `develop` branch for ongoing work  
✅ CI/CD secrets configured  
✅ Automated testing and deployment pipeline  

**Next**: Start developing features on `develop` branch and merge to `main` for releases! 🚀
