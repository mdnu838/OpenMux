# OpenMux - Project Definition

## 🎯 Vision

A Python library that provides **zero-configuration AI chat** - just install, add your API key to `.env`, and start chatting with the best free models automatically.

```bash
# Install
pip install openmux

# Setup
echo "OPENROUTER_API_KEY=your-key-here" > .env

# Use
from openmux import Orchestrator

orchestrator = Orchestrator()
response = orchestrator.process("Explain quantum computing in simple terms")
print(response["response"])
```

---

## 📋 Project Overview

**OpenMux** is a Python library available through pip, conda, pixi, uv, and other package managers.

**Purpose:** Automatically select, route, and combine outputs from free GenAI models and free API providers. It creates a unified interface for discovering, connecting, and using open-access models across the AI ecosystem.

**Target Users:**
- Developers who want easy access to free AI models
- Researchers testing multiple models
- Students learning AI without API costs
- Projects with budget constraints

**Key Differentiator:** Smart model selection + automatic failover + multi-model combination

---

## ✨ Core Features

### 1. Automatic Provider Discovery
- Maintains a curated list of free, open-access GenAI model providers
- Updates provider metadata automatically from a central registry (JSON or API source)
- **Only free or open-source endpoints** — no paid or key-based commercial APIs
- Supported providers:
  - **OpenRouter** (free-tier models) - PRIMARY
  - **Hugging Face** free inference endpoints
  - **Together AI** (community models)
  - **Mistral** free APIs
  - **Ollama** locally-hosted models
  - **LM Studio** local models
  - Other publicly available sources

### 2. Task Auto-Classification
- Analyzes user queries to classify tasks:
  - `chat` - Conversational queries
  - `code` - Programming/code generation
  - `tts` - Text-to-speech
  - `audio` - Audio processing
  - `embeddings` - Vector embeddings
  - `image` - Image generation/analysis
  - `other` - Miscellaneous tasks
- Uses a lightweight local classifier (small LLM or rule-based)
- Allows manual override
- Displays classification confidence score

### 3. Model Auto-Selection
Intelligently selects the most suitable free model based on:
- **Model capability metadata** (task tags, specialization)
- **Response quality** (historical benchmarks or user votes)
- **Latency and uptime** data
- **Provider availability** (failover to backup if primary fails)

Provides transparency:
- Explains why a model was chosen
- Shows confidence scores
- Logs selection reasoning

### 4. Multi-Model Routing and Response Combination
- Optionally sends query to multiple free models simultaneously
- Collects and combines responses using configurable strategies:
  - **Concatenate & summarize** - Merge responses and create summary
  - **Majority vote** - For structured outputs (classification, etc.)
  - **Secondary summarization** - Use local model to combine outputs
  - **Best response selection** - Based on confidence/quality metrics

Priorities:
- Text and embeddings first
- Multimodal support added in later phases

### 5. Offline & Local Fallback
- Supports local hosting via **Ollama**, **LM Studio**, or **transformers**
- Bundles lightweight open models for offline operation:
  - Phi-3 Mini
  - Mistral-7B
  - Llama-3-Instruct-8B
  - Gemma-2B
- Auto-detects available hardware (GPU/CPU)
- Switches to offline mode if APIs are unreachable
- Configuration file for user-defined fallback models

### 6. Secure Configuration Management
- Stores provider configs securely using:
  - Encrypted local storage
  - OS keyring integration
  - `.env` file support (for API keys)
- **Does NOT require API keys** unless using specific free-tier services
- Only stores necessary access tokens for free-tier APIs

### 7. Transparency & Logging
- Comprehensive logging:
  - Which model handled the query
  - Selection reasoning
  - Response latency
  - Response size
  - Success/failure status
- Benchmarking mode for quality evaluation
- Performance metrics per provider

---

## 🛠️ Required Resources

### API Keys & Services

| Resource | Purpose | Cost | Required | How to Get |
|----------|---------|------|----------|------------|
| **OpenRouter API** | Primary model provider | Free tier available | **YES** | [openrouter.ai](https://openrouter.ai) → Sign up → Get API key |
| **Hugging Face** | Inference API access | Free tier available | Optional | [huggingface.co](https://huggingface.co) → Settings → Access Tokens |
| **Together AI** | Community models | Free tier available | Optional | [together.ai](https://together.ai) → API Keys |
| **Ollama** | Local model hosting | Free (self-hosted) | Optional | [ollama.ai](https://ollama.ai) → Download |

### Development Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Python 3.9+** | Runtime environment | `python --version` |
| **uv** | Fast package manager | `curl -LsSf https://astral.sh/uv/install.sh | sh` |
| **Git** | Version control | Pre-installed on most systems |
| **pytest** | Testing framework | `uv pip install pytest` |

### Optional Resources

| Resource | Purpose | When Needed |
|----------|---------|-------------|
| **GPU** | Faster local model inference | For offline/local models |
| **Docker** | Containerization | For deployment |
| **Redis** | Caching responses | For production setups |

---

## 📝 Detailed Task List

### Phase 1: Foundation (Current - MVP)

#### ✅ Completed Tasks
- [x] Project structure and configuration
- [x] OpenRouter provider integration
- [x] Basic task classifier (chat, code, embeddings)
- [x] Simple orchestrator
- [x] Configuration management with keyring
- [x] Unit and integration tests
- [x] CI/CD pipeline (GitHub Actions)
- [x] Package publishing (TestPyPI/PyPI)
- [x] Documentation

#### 🔄 Current Phase Tasks

**1. Enhanced User Experience**
- [ ] Automatic `.env` file detection
- [ ] Better error messages for missing API keys
- [ ] Interactive setup wizard (`openmux init`)
- [ ] CLI tool for quick testing (`openmux chat "hello"`)
- [ ] Configuration validation

**2. Model Selection Improvements**
- [ ] Add model quality scoring
- [ ] Implement failover logic
- [ ] Add model availability checking
- [ ] Provider health monitoring
- [ ] Response time tracking

**3. Testing & Quality**
- [ ] Add more integration tests with live APIs
- [ ] Performance benchmarking suite
- [ ] Error handling improvements
- [ ] Edge case testing

### Phase 2: Multi-Provider Support

**4. Additional Providers**
- [ ] Hugging Face Inference API integration
- [ ] Together AI integration
- [ ] Mistral API integration
- [ ] Provider registry system
- [ ] Dynamic provider loading

**5. Provider Management**
- [ ] Provider health checks
- [ ] Automatic provider discovery
- [ ] Provider preference settings
- [ ] Fallback chain configuration

### Phase 3: Advanced Features

**6. Multi-Model Orchestration**
- [ ] Parallel model querying
- [ ] Response combination strategies
- [ ] Consensus-based outputs
- [ ] Quality comparison tools

**7. Local & Offline Support**
- [ ] Ollama integration
- [ ] LM Studio integration
- [ ] Hugging Face transformers backend
- [ ] Model download manager
- [ ] Offline mode detection

**8. Enhanced Classification**
- [ ] Multi-label task classification
- [ ] Confidence threshold tuning
- [ ] Custom classifiers support
- [ ] Fine-tuned classification models

### Phase 4: Production Features

**9. Performance & Scalability**
- [ ] Response caching (Redis/local)
- [ ] Request rate limiting
- [ ] Batch processing support
- [ ] Async/await support throughout

**10. Monitoring & Analytics**
- [ ] Usage statistics tracking
- [ ] Cost tracking (for paid tiers)
- [ ] Model performance analytics
- [ ] Error rate monitoring
- [ ] Dashboard/visualization

**11. Security & Privacy**
- [ ] API key rotation support
- [ ] Request sanitization
- [ ] PII detection and removal
- [ ] Audit logging
- [ ] Compliance tools

### Phase 5: Extended Capabilities

**12. Multimodal Support**
- [ ] Image generation (DALL-E alternatives)
- [ ] Image analysis
- [ ] Text-to-speech
- [ ] Speech-to-text
- [ ] Video processing

**13. Developer Tools**
- [ ] Model playground UI
- [ ] Prompt template library
- [ ] Response comparison tool
- [ ] Model benchmarking CLI
- [ ] Performance profiler

**14. Ecosystem Integration**
- [ ] LangChain compatibility
- [ ] LlamaIndex integration
- [ ] OpenAI API compatibility layer
- [ ] Gradio/Streamlit components

---

## 🚀 Implementation Roadmap

### Sprint 1: Enhanced MVP (2 weeks)
**Goal:** Make installation and setup effortless

Tasks:
- Automatic `.env` detection
- `openmux init` setup wizard
- `openmux chat` CLI tool
- Better error messages
- Improved documentation

**Deliverable:** Users can install and chat within 2 minutes

### Sprint 2: Provider Expansion (2 weeks)
**Goal:** Add 2-3 more free providers

Tasks:
- Hugging Face integration
- Together AI integration
- Provider health checks
- Failover logic

**Deliverable:** Automatic failover to backup providers

### Sprint 3: Multi-Model Features (3 weeks)
**Goal:** Enable multi-model comparison

Tasks:
- Parallel querying
- Response combination
- Quality comparison
- Benchmarking tools

**Deliverable:** Users can query multiple models and compare

### Sprint 4: Local Models (3 weeks)
**Goal:** Full offline support

Tasks:
- Ollama integration
- Model download manager
- Offline detection
- Local model fallback

**Deliverable:** Works without internet connection

### Sprint 5: Production Ready (2 weeks)
**Goal:** Enterprise-grade reliability

Tasks:
- Caching layer
- Monitoring
- Error recovery
- Documentation polish

**Deliverable:** Production-ready v1.0.0

---

## 📦 Minimal User Setup (Target Experience)

### Step 1: Install
```bash
pip install openmux
```

### Step 2: Setup
```bash
# Interactive setup wizard
openmux init

# Or manual setup
echo "OPENROUTER_API_KEY=sk-or-v1-..." > .env
```

### Step 3: Use

**Option A: Python API**
```python
from openmux import Orchestrator

orchestrator = Orchestrator()  # Auto-loads from .env
response = orchestrator.process("Write a Python function to sort a list")
print(response["response"])
```

**Option B: CLI**
```bash
openmux chat "Explain recursion"
```

**Option C: Interactive Mode**
```bash
openmux
# Enters chat mode
You: What is machine learning?
AI: Machine learning is...
```

**That's it!** No configuration files, no complex setup, no model selection needed.

---

## 🎯 Success Metrics

### User Experience
- ⏱️ **Time to first query:** < 2 minutes (from install to response)
- 🔧 **Setup complexity:** < 5 steps
- 📖 **Documentation:** Complete and clear

### Technical Performance
- ⚡ **Response time:** < 5 seconds (95th percentile)
- 🎯 **Classification accuracy:** > 90%
- 🔄 **Failover time:** < 1 second
- 💯 **Uptime:** > 99% (with fallbacks)

### Adoption
- 📥 **Downloads:** 1,000+ in first month
- ⭐ **GitHub stars:** 100+ in first quarter
- 🐛 **Bug reports:** < 5 critical issues
- 📚 **Documentation completeness:** 100%

---

## 🔮 Future Vision

**Year 1:** Dominant free AI orchestration library
- 10,000+ active users
- 5+ provider integrations
- Full multimodal support
- Enterprise features

**Year 2:** AI Infrastructure Standard
- LangChain/LlamaIndex integration
- Cloud deployment options
- SaaS offering
- Community-driven model registry

**Year 3:** AI Democratization Platform
- Free AI access for everyone
- Model marketplace
- Collaborative benchmarking
- Educational platform

---

## 📄 License & Contribution

- **License:** MIT (maximum openness)
- **Contribution:** Open to all (see [CONTRIBUTING.md](../CONTRIBUTING.md))
- **Philosophy:** Make AI accessible to everyone, regardless of budget

---

**Last Updated:** November 2025  
**Version:** 0.1.0 (MVP)  
**Status:** Active Development
