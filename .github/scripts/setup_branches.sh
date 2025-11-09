#!/bin/bash
# Setup Git branch structure for OpenMux

echo "🔧 Setting up OpenMux Git branch structure..."
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Fetch latest from origin
echo "📥 Fetching latest changes from origin..."
git fetch origin

# Create develop branch from main if it doesn't exist
if ! git show-ref --verify --quiet refs/heads/develop; then
    echo "✨ Creating develop branch from main..."
    git checkout main
    git pull origin main
    git checkout -b develop
    git push -u origin develop
    echo "✅ develop branch created"
else
    echo "ℹ️  develop branch already exists"
fi

# Switch back to main
git checkout main

echo ""
echo "✅ Branch structure setup complete!"
echo ""
echo "📋 Current branches:"
git branch -a | grep -E "(main|develop|feature|fix|docs|chore)" || git branch -a
echo ""
echo "📖 Branch Strategy:"
echo "  • main     - Production-ready code (protected)"
echo "  • develop  - Integration branch for next release"
echo "  • feature/* - New features"
echo "  • fix/*    - Bug fixes"
echo "  • docs/*   - Documentation updates"
echo "  • chore/*  - Maintenance tasks"
echo ""
echo "🔗 Next steps:"
echo "  1. Go to GitHub repository settings"
echo "  2. Navigate to Settings → Branches"
echo "  3. Set 'main' as the default branch"
echo "  4. Add branch protection rules for 'main':"
echo "     - Require pull request reviews"
echo "     - Require status checks to pass"
echo "     - Require branches to be up to date"
echo ""
echo "📝 To create a new feature branch:"
echo "  git checkout develop"
echo "  git pull origin develop"
echo "  git checkout -b feature/your-feature-name"
echo ""
