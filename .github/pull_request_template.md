---
name: Pull Request
about: Submit changes for review
title: "[TYPE] Brief description"
labels: ''
assignees: ''

---

## Description
<!-- Provide a clear and concise description of the changes -->

## Type of Change
<!-- Mark the relevant option with an 'x' -->

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🔧 Configuration change
- [ ] ♻️ Code refactoring
- [ ] ⚡ Performance improvement
- [ ] ✅ Test addition or update

## Related Issues
<!-- Link to related issues using #issue_number -->

Closes #
Relates to #

## Changes Made
<!-- List the specific changes in this PR -->

- 
- 
- 

## Testing
<!-- Describe the tests you ran and/or added -->

### Test Coverage
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing locally
- [ ] Coverage >= 90%

### Manual Testing
<!-- Describe manual testing performed -->

```bash
# Commands used for testing
pytest tests/unit/ -v
pytest tests/integration/test_orchestrator_mock.py -v
```

## Checklist
<!-- Mark completed items with an 'x' -->

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings or errors
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published
- [ ] I have updated the CHANGELOG.md (if applicable)

## Screenshots (if applicable)
<!-- Add screenshots to help explain your changes -->

## Additional Context
<!-- Add any other context about the PR here -->

## Reviewer Notes
<!-- Any specific areas you want reviewers to focus on? -->

---

**Before submitting:**
1. Ensure your branch is up to date with the target branch
2. Run `pytest tests/ -v` locally
3. Run `black openmux/ tests/` to format code
4. Run `ruff check openmux/ tests/` to lint
5. Update documentation if needed
