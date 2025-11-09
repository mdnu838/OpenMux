# Changelog

All notable changes to OpenMux will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Coming Soon
- Production release to PyPI
- Additional provider integrations (Anthropic, Together AI, Mistral)
- Enhanced multi-model combination strategies
- Performance optimization
- Extended API documentation

### Development Builds
**Note**: TestPyPI builds use automatic version incrementing (e.g., `0.1.100`, `0.1.101`) based on GitHub Actions run numbers to avoid conflicts. Production releases on PyPI use semantic versioning (e.g., `0.1.1`, `0.2.0`).

---

## [0.1.1] - 2025-11-09

### 🔧 Fixed
- **Packaging**: Fixed package structure to include all subpackages (core, providers, classifier, cli, utils)
- **Documentation**: Updated README with TestPyPI installation instructions
- **Documentation**: Reorganized documentation files into docs/ folder
- **Documentation**: Updated project references from opencascade to openmux

### 📝 Changed
- Moved development documentation to docs/ folder for better organization
- Updated installation instructions with TestPyPI link
- Improved README structure and clarity

---

## [0.1.0] - 2025-11-09

### 🎉 Initial Release

The first release of OpenMux (rebranded from OpenCascade)! Published to TestPyPI.

### ✨ Added

#### Core Features
- **Orchestrator**: Complete async orchestration engine for routing queries to providers
- **Task Classification**: Intelligent task type detection (chat, code, embeddings)
- **Provider System**: Modular provider architecture with base interface
- **Model Selector**: Smart provider selection based on task type
- **Query Router**: Async routing with retry logic and timeout handling
- **Response Combiner**: Multi-model response combination capabilities
- **Fallback Handler**: Graceful fallback to alternative providers

#### Providers
- **OpenRouter**: Full integration with free models (mistralai/mistral-7b-instruct:free)
- **HuggingFace**: Inference API support
- **Ollama**: Local model support with configurable endpoints
- **Provider Registry**: Automatic discovery and registration

#### Configuration & Utilities
- **Config System**: JSON-based configuration with environment variable support
- **Logging System**: Rich console logging with file rotation
- **Environment Management**: `.env` file support for API keys
- **Security**: Best practices for secret management

#### CLI & API
- **Python API**: Clean programmatic interface
- **CLI Tool**: Command-line interface with typer
- **Examples**: Usage examples and quick start guide

### 🧪 Testing

- **Unit Tests**: 6/6 passing (100%) for classifier
- **Integration Tests**: 6/6 passing (100%) for orchestrator
- **Mock-based Testing**: Complete test suite without API dependencies
- **Test Coverage**: 100% for core components
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing

### 📚 Documentation

- **README.md**: Complete project overview and quick start
- **CONTRIBUTING.md**: Comprehensive contribution guidelines with branching strategy
- **ARCHITECTURE.md**: System design and architecture documentation
- **API.md**: Detailed API reference
- **TESTING_STRATEGY.md**: Testing guidelines and best practices
- **MVP_TASKS.md**: Development roadmap and progress tracking
- **TEST_RESULTS.md**: Current test status and known issues
- **DEVELOPMENT_SUMMARY.md**: Session accomplishments and progress
- **SECURITY.md**: Security policy and best practices
- **.env.example**: Environment variable template

### 🔧 Development Tools

- **GitHub Actions**: Automated CI/CD pipeline
  - Multi-Python version testing (3.9-3.13)
  - Linting and formatting checks
  - Security scanning
  - Build verification
- **Pull Request Template**: Standardized PR format
- **.gitignore**: Comprehensive ignore rules
- **pre-commit hooks**: Code quality automation (coming soon)

### 🐛 Fixed

- **Selector Bug**: Fixed method name mismatch (`supported_tasks()` → `supports_task()`)
- **Lock File**: Resolved uv.lock corruption issues
- **BaseProvider**: Simplified interface to essential methods only

### 🔒 Security

- **Environment Variables**: Proper .env handling
- **API Key Protection**: Removed .env from version control
- **Security Documentation**: Added comprehensive security guidelines
- **CI Security Scans**: Automated security scanning with Bandit and Safety

### 📋 Known Issues

- OpenRouter API key validation (external dependency)
- HuggingFace provider not tested with live API
- Ollama provider requires local installation

### 🎯 MVP Success Criteria

✅ Support 3 providers (HuggingFace, OpenRouter, Ollama)  
✅ Basic task classification (chat, code, embeddings)  
✅ Simple output combination (merge + summarize)  
✅ CLI + Python API  
✅ Offline fallback via Ollama  
✅ Complete documentation  
✅ 90%+ test coverage  
✅ All tests passing  
✅ GitHub Actions CI/CD  

### 📊 Statistics

- **Files Created**: 35+
- **Lines of Code**: 2000+
- **Tests**: 12/12 passing
- **Coverage**: 100% (core components)
- **Documentation Files**: 15+
- **Commits**: 10+ to mvp-alpha branch

---

## Previous Development

### Added
- Initial project structure
- Comprehensive documentation system
- Task breakdown with 24+ implementation tasks
- Testing strategy with auto-debug capabilities
- Development workflow and guidelines

---

## Version Format

### Types of Changes
- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security improvements

### Version Numbers
Given a version number MAJOR.MINOR.PATCH:
- MAJOR: Incompatible API changes
- MINOR: Backwards-compatible functionality
- PATCH: Backwards-compatible bug fixes

---

## Release Notes Template

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Feature 1
- Feature 2

### Changed
- Change 1
- Change 2

### Deprecated
- Deprecation 1

### Removed
- Removal 1

### Fixed
- Bug fix 1
- Bug fix 2

### Security
- Security fix 1
```