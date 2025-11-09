# OpenMux Architecture

## System Overview

OpenMux is designed as a modular, extensible system for orchestrating free GenAI models. The architecture follows clean separation of concerns with clear interfaces between components.

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (CLI / Python API)                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      Orchestrator                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • Request Coordination                              │   │
│  │  • Component Integration                             │   │
│  │  • Error Handling                                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────┬─────────────┬──────────────┬──────────────┬──────────┘
      │             │              │              │
┌─────▼────┐  ┌────▼────┐  ┌──────▼─────┐  ┌────▼─────┐
│Classifier│  │Selector │  │   Router   │  │ Combiner │
└─────┬────┘  └────┬────┘  └──────┬─────┘  └────┬─────┘
      │            │              │              │
┌─────▼────────────▼──────────────▼──────────────▼─────────┐
│                  Provider Registry                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │OpenRouter│ │HuggingFace│ │ Ollama  │ │  Local   │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
└───────────────────────────────────────────────────────────┘
                        │
┌───────────────────────▼───────────────────────────────────┐
│                  Support Systems                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ Config  │  │ Logging │  │ Security│  │ Metrics │    │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │
└───────────────────────────────────────────────────────────┘
```

---

## 📦 Component Details

### 1. Orchestrator
**Responsibility**: Coordinate all system components

**Key Functions**:
- Accept user queries
- Coordinate classification, selection, and routing
- Handle errors and fallbacks
- Return processed responses

**Interfaces**:
```python
class Orchestrator:
    def process(query: str, **config) -> str
    def process_multi(query: str, num_models: int, method: str) -> str
    def get_metrics() -> Dict[str, Any]
```

**Dependencies**:
- Classifier
- Selector
- Router
- Combiner
- Config
- Logging

---

### 2. Task Classifier
**Responsibility**: Determine task type from user query

**Components**:
- **Rule-Based Classifier**: Keyword and pattern matching
- **ML Classifier**: Lightweight model-based classification
- **Unified Interface**: Combines both approaches

**Flow**:
```
Query Input
    ↓
Rule-Based Analysis
    ↓
Confidence Check (>0.8)
    ↓ No
ML Classification
    ↓
Task Type + Confidence
```

**Interface**:
```python
class TaskClassifier:
    def classify(query: str) -> Tuple[TaskType, float]
    def classify_with_override(query: str, task_type: TaskType) -> TaskType
```

---

### 3. Model Selector
**Responsibility**: Choose best model(s) for task

**Selection Criteria**:
1. **Task Compatibility**: Model supports required task
2. **Performance History**: Based on benchmarks
3. **Availability**: Provider is online and healthy
4. **Latency**: Response time requirements
5. **Quality**: Historical quality scores

**Algorithm**:
```python
def select_model(task: TaskType, preferences: List[str]) -> Provider:
    1. Filter providers by task capability
    2. Check provider health status
    3. Score each provider:
       score = (quality * 0.4) + (speed * 0.3) + (availability * 0.3)
    4. Apply user preferences
    5. Return highest-scoring provider
```

**Interface**:
```python
class Selector:
    def select_single(task: TaskType, **config) -> Provider
    def select_multiple(task: TaskType, count: int) -> List[Provider]
    def explain_selection(provider: Provider) -> str
```

---

### 4. Query Router
**Responsibility**: Route queries to selected providers

**Features**:
- Asynchronous request handling
- Retry logic with exponential backoff
- Timeout management
- Load balancing across providers

**Flow**:
```
Selected Provider(s)
    ↓
Prepare Request
    ↓
Send Async Request
    ↓
Wait with Timeout
    ↓
Retry on Failure (max 3)
    ↓
Return Response or Error
```

**Interface**:
```python
class Router:
    async def route_single(provider: Provider, query: str) -> str
    async def route_multiple(providers: List[Provider], query: str) -> List[str]
    def set_timeout(seconds: float) -> None
```

---

### 5. Response Combiner
**Responsibility**: Combine multiple model responses

**Methods**:
1. **Concatenate**: Simple concatenation with separators
2. **Voting**: Majority vote for structured outputs
3. **Summarize**: Use local model to summarize responses
4. **Best**: Select highest-quality response

**Interface**:
```python
class Combiner:
    def concatenate(responses: List[str]) -> str
    def vote(responses: List[str]) -> str
    def summarize(responses: List[str]) -> str
    def select_best(responses: List[str], metrics: List[Dict]) -> str
```

---

### 6. Provider System

#### Base Provider Interface
```python
class BaseProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str
    
    @abstractmethod
    async def is_available(self) -> bool
    
    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]
    
    @abstractmethod
    async def generate(prompt: str, **kwargs) -> str
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]
    
    @abstractmethod
    async def supported_tasks(self) -> List[str]
```

#### Provider Registry
**Responsibility**: Manage provider lifecycle

**Features**:
- Dynamic provider registration
- Health monitoring
- Capability caching
- Automatic updates from central registry

**Interface**:
```python
class ProviderRegistry:
    def register(provider: BaseProvider) -> None
    def get(name: str) -> BaseProvider
    def get_all() -> List[BaseProvider]
    def get_by_task(task: TaskType) -> List[BaseProvider]
    def update_from_remote() -> None
```

---

### 7. Model Management

#### Model Manager
**Responsibility**: Manage local models

**Features**:
- Download models from HuggingFace
- Version management
- Disk space management
- Model updates

**Interface**:
```python
class ModelManager:
    def download(model_id: str) -> Path
    def load(model_id: str) -> Any
    def list_available() -> List[str]
    def delete(model_id: str) -> None
    def update(model_id: str) -> None
```

#### Hardware Detection
**Responsibility**: Detect and optimize for hardware

**Features**:
- CPU/GPU detection
- Memory calculation
- Optimization recommendations
- Resource constraints

**Interface**:
```python
class HardwareDetector:
    def detect_gpu() -> Optional[str]
    def get_available_memory() -> int
    def recommend_model_size() -> str
    def supports_quantization() -> bool
```

---

### 8. Configuration System

**Features**:
- Encrypted storage
- Environment variable support
- Default configurations
- Provider-specific settings

**Structure**:
```json
{
  "providers": {
    "openrouter": {
      "enabled": true,
      "api_key": null,
      "timeout": 30
    }
  },
  "classifier": {
    "primary": "rule_based",
    "fallback": "ml",
    "confidence_threshold": 0.8
  },
  "fallback": {
    "enabled": true,
    "offline_mode": "auto",
    "local_models": ["phi-3-mini", "mistral-7b"]
  },
  "performance": {
    "cache_responses": true,
    "max_concurrent": 10,
    "timeout": 30
  }
}
```

---

### 9. Logging & Metrics

#### Logging System
**Levels**:
- DEBUG: Detailed diagnostic information
- INFO: General operational messages
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical failures

**Specialized Loggers**:
- **ModelSelectionLogger**: Log selection decisions
- **BenchmarkLogger**: Log performance metrics
- **SecurityLogger**: Log security events

#### Metrics Collection
**Tracked Metrics**:
- Request latency
- Provider success rates
- Model quality scores
- Resource usage
- Error rates

---

## 🔄 Request Flow

### Standard Request Flow
```
1. User submits query
   ↓
2. Orchestrator receives request
   ↓
3. Classifier determines task type
   ↓
4. Selector chooses best provider
   ↓
5. Router sends request to provider
   ↓
6. Provider processes and responds
   ↓
7. Response returned to user
   ↓
8. Metrics logged
```

### Multi-Model Request Flow
```
1. User submits query with multi-model flag
   ↓
2. Orchestrator receives request
   ↓
3. Classifier determines task type
   ↓
4. Selector chooses N providers
   ↓
5. Router sends parallel requests
   ↓
6. Providers process and respond
   ↓
7. Combiner merges responses
   ↓
8. Combined response returned
   ↓
9. Metrics logged
```

### Fallback Flow
```
1. Primary provider request fails
   ↓
2. Error caught by Router
   ↓
3. Fallback handler activated
   ↓
4. Alternative provider selected
   ↓
5. Retry with fallback provider
   ↓
6. If still fails, try offline mode
   ↓
7. Response or final error returned
```

---

## 🔒 Security Architecture

### Data Flow Security
1. **Input Validation**: Sanitize all user inputs
2. **API Key Storage**: Encrypted in OS keyring
3. **Configuration Encryption**: Encrypt sensitive config
4. **Secure Communication**: HTTPS for all API calls
5. **No Data Retention**: Don't store user queries

### Security Layers
```
┌─────────────────────────────────────┐
│      Input Validation Layer         │
└───────────────┬─────────────────────┘
                │
┌───────────────▼─────────────────────┐
│    Authentication Layer              │
└───────────────┬─────────────────────┘
                │
┌───────────────▼─────────────────────┐
│      Encryption Layer                │
└───────────────┬─────────────────────┘
                │
┌───────────────▼─────────────────────┐
│      Provider Communication          │
└─────────────────────────────────────┘
```

---

## ⚡ Performance Optimizations

### Caching Strategy
1. **Response Cache**: Cache frequent queries
2. **Capability Cache**: Cache provider capabilities
3. **Model Cache**: Keep loaded models in memory
4. **Configuration Cache**: Cache config in memory

### Async Operations
- All provider calls are asynchronous
- Parallel processing for multi-model requests
- Non-blocking I/O for file operations

### Resource Management
- Model unloading when memory constrained
- Connection pooling for HTTP requests
- Lazy loading of heavy components

---

## 🧩 Extension Points

### Custom Providers
```python
from openmux.providers.base import BaseProvider

class CustomProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "custom"
    
    # Implement other abstract methods
```

### Custom Classifiers
```python
from openmux.classifier.base import BaseClassifier

class CustomClassifier(BaseClassifier):
    def classify(self, query: str) -> Tuple[TaskType, float]:
        # Custom classification logic
        pass
```

### Custom Combiners
```python
from openmux.core.combiner import BaseCombiner

class CustomCombiner(BaseCombiner):
    def combine(self, responses: List[str]) -> str:
        # Custom combination logic
        pass
```

---

## 📊 Monitoring & Observability

### Health Checks
- Provider availability
- System resource usage
- Response latency
- Error rates

### Metrics Dashboard
- Real-time performance metrics
- Provider comparison
- Quality trends
- Resource utilization

### Alerting
- Provider failures
- Performance degradation
- Resource constraints
- Security events

---

## 🔧 Deployment Considerations

### Environment Support
- Local development
- Docker containers
- Cloud platforms (AWS, GCP, Azure)
- Edge devices

### Scaling Strategy
- Horizontal scaling for concurrent requests
- Provider pool expansion
- Caching layers
- Load balancing

---

## 📝 Design Principles

1. **Modularity**: Independent, replaceable components
2. **Extensibility**: Easy to add new providers/features
3. **Reliability**: Graceful degradation and fallbacks
4. **Performance**: Optimized for low latency
5. **Security**: Privacy-first, minimal data retention
6. **Transparency**: Explainable decisions
7. **Simplicity**: Easy to use and understand
8. **Testability**: Comprehensive test coverage