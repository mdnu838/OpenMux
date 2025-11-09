# OpenMux Testing Strategy

## Overview
This document outlines the comprehensive testing strategy for OpenMux, ensuring every line of code is covered by tests and includes automatic debugging capabilities.

---

## 🎯 Testing Principles

### 1. Test-Driven Development (TDD)
- Write tests BEFORE implementation
- Tests define the expected behavior
- Implementation satisfies the tests

### 2. Comprehensive Coverage
- **Target**: 90%+ code coverage
- **Unit Tests**: Every function, method, and class
- **Integration Tests**: Every module interaction
- **End-to-End Tests**: Complete user workflows

### 3. Auto-Debug System
- Built-in diagnostic information
- Detailed error messages
- State logging at failure points
- Automatic root cause analysis

### 4. Continuous Validation
- Tests run on every commit
- Integration tests on every PR
- Performance regression detection
- Automated quality gates

---

## 📁 Test Organization

```
tests/
├── unit/                      # Isolated component tests
│   ├── test_core/
│   ├── test_providers/
│   ├── test_classifier/
│   ├── test_models/
│   └── test_utils/
│
├── integration/               # Component interaction tests
│   ├── test_provider_integration.py
│   ├── test_end_to_end.py
│   ├── test_multi_model.py
│   └── test_fallback_flow.py
│
├── fixtures/                  # Test data and mocks
│   ├── sample_queries.json
│   ├── mock_responses.json
│   └── test_configs.json
│
├── benchmarks/               # Performance tests
│   ├── latency_tests.py
│   └── throughput_tests.py
│
└── conftest.py              # Shared pytest configuration
```

---

## 🧪 Unit Testing Guidelines

### Structure
```python
# tests/unit/test_module/test_feature.py

import pytest
from openmux.module import Feature

class TestFeature:
    """Test suite for Feature functionality."""
    
    def setup_method(self):
        """Setup before each test."""
        self.feature = Feature()
    
    def test_basic_functionality(self):
        """Test basic feature operation."""
        result = self.feature.do_something("input")
        assert result == "expected_output"
    
    def test_edge_case_empty_input(self):
        """Test handling of empty input."""
        result = self.feature.do_something("")
        assert result == "" or result is None
    
    def test_invalid_input_raises_error(self):
        """Test that invalid input raises appropriate error."""
        with pytest.raises(ValueError) as exc_info:
            self.feature.do_something(None)
        assert "cannot be None" in str(exc_info.value)
    
    @pytest.mark.parametrize("input,expected", [
        ("test1", "result1"),
        ("test2", "result2"),
        ("test3", "result3"),
    ])
    def test_multiple_inputs(self, input, expected):
        """Test various input scenarios."""
        result = self.feature.do_something(input)
        assert result == expected
```

### Requirements for Each Unit Test
1. **Clear Test Names**: Describe what is being tested
2. **Single Assertion Focus**: One concept per test
3. **Isolation**: No dependencies on other tests
4. **Mocking**: Mock all external dependencies
5. **Coverage**: Test success, failure, and edge cases

### Mocking External Dependencies
```python
from unittest.mock import Mock, patch, MagicMock
import pytest

class TestProviderWithMocks:
    """Test provider with mocked API calls."""
    
    @patch('openmux.providers.openrouter.aiohttp.ClientSession')
    async def test_api_call_success(self, mock_session):
        """Test successful API call."""
        # Setup mock
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"result": "success"})
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
        
        # Test
        provider = OpenRouterProvider()
        result = await provider.generate("test query")
        
        # Assert
        assert result == "success"
    
    @patch('openmux.providers.openrouter.aiohttp.ClientSession')
    async def test_api_call_failure(self, mock_session):
        """Test API call failure handling."""
        # Setup mock to fail
        mock_session.return_value.__aenter__.side_effect = Exception("Network error")
        
        # Test
        provider = OpenRouterProvider()
        with pytest.raises(Exception) as exc_info:
            await provider.generate("test query")
        
        # Assert error handling
        assert "Network error" in str(exc_info.value)
```

---

## 🔗 Integration Testing Guidelines

### Purpose
- Test interactions between components
- Validate data flow through system
- Ensure proper error propagation
- Verify fallback mechanisms

### Structure
```python
# tests/integration/test_end_to_end.py

import pytest
from openmux import Orchestrator
from openmux.providers import OpenRouterProvider, OllamaProvider

@pytest.mark.integration
class TestEndToEnd:
    """End-to-end integration tests."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator with test configuration."""
        return Orchestrator(config_path="tests/fixtures/test_config.json")
    
    @pytest.mark.asyncio
    async def test_complete_workflow(self, orchestrator):
        """Test complete query processing workflow."""
        # Test data
        query = "Write a Python hello world program"
        
        # Execute
        result = orchestrator.process(query)
        
        # Validate
        assert result is not None
        assert len(result) > 0
        assert "print" in result.lower() or "hello" in result.lower()
    
    @pytest.mark.asyncio
    async def test_provider_fallback(self, orchestrator):
        """Test fallback when primary provider fails."""
        # Simulate primary provider failure
        # (Implementation depends on mocking strategy)
        
        result = orchestrator.process("test query")
        
        # Should get result from fallback provider
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_multi_provider_combination(self, orchestrator):
        """Test multi-provider response combination."""
        result = orchestrator.process_multi(
            "Explain quantum computing",
            num_models=2,
            combination_method="summarize"
        )
        
        assert result is not None
        assert len(result) > 100  # Substantial response
```

### Integration Test Categories

#### 1. Provider Integration
```python
@pytest.mark.integration
class TestProviderIntegration:
    """Test provider system integration."""
    
    async def test_provider_discovery(self):
        """Test automatic provider discovery."""
        pass
    
    async def test_provider_health_checks(self):
        """Test health check coordination."""
        pass
    
    async def test_provider_capability_aggregation(self):
        """Test capability collection from all providers."""
        pass
```

#### 2. Classifier Integration
```python
@pytest.mark.integration
class TestClassifierIntegration:
    """Test classifier integration with orchestrator."""
    
    async def test_classification_influences_selection(self):
        """Verify classifier output affects model selection."""
        pass
    
    async def test_manual_override_respected(self):
        """Verify manual task type override works."""
        pass
```

#### 3. Fallback Flow Integration
```python
@pytest.mark.integration
class TestFallbackFlow:
    """Test complete fallback scenarios."""
    
    async def test_online_to_offline_transition(self):
        """Test graceful transition to offline mode."""
        pass
    
    async def test_provider_failure_recovery(self):
        """Test recovery from provider failures."""
        pass
```

---

## 🐛 Auto-Debug System

### Debug Logging
Every test includes comprehensive logging:

```python
import logging
from openmux.utils.logging import setup_logger

class TestWithDebugLogging:
    """Test with detailed debug logging."""
    
    def setup_method(self):
        """Setup debug logging."""
        self.logger = setup_logger(
            __name__,
            log_file="tests/logs/test_debug.log",
            level=logging.DEBUG
        )
    
    def test_with_debug_info(self):
        """Test with debug information capture."""
        self.logger.debug("Starting test")
        
        # Test execution
        result = self.feature.do_something("input")
        
        self.logger.debug(f"Result: {result}")
        self.logger.debug(f"Feature state: {self.feature.__dict__}")
        
        # Assertion with context
        assert result == "expected", (
            f"Expected 'expected' but got '{result}'. "
            f"Feature state: {self.feature.__dict__}"
        )
```

### State Validation
Capture system state at failure points:

```python
class TestWithStateValidation:
    """Test with state validation."""
    
    def validate_state(self, obj, expected_state):
        """Validate object state matches expected."""
        actual_state = {
            k: v for k, v in obj.__dict__.items()
            if not k.startswith('_')
        }
        
        assert actual_state == expected_state, (
            f"State mismatch:\n"
            f"Expected: {expected_state}\n"
            f"Actual: {actual_state}\n"
            f"Diff: {set(expected_state.items()) ^ set(actual_state.items())}"
        )
```

### Error Context Capture
Provide maximum context in error messages:

```python
class TestWithErrorContext:
    """Test with comprehensive error context."""
    
    def test_with_context(self):
        """Test with error context capture."""
        input_data = {"query": "test"}
        
        try:
            result = self.processor.process(input_data)
        except Exception as e:
            pytest.fail(
                f"Processing failed with error: {e}\n"
                f"Input: {input_data}\n"
                f"Processor state: {self.processor.__dict__}\n"
                f"Stack trace: {traceback.format_exc()}"
            )
```

### Automatic Root Cause Analysis
```python
class DebugHelper:
    """Helper for automatic debugging."""
    
    @staticmethod
    def analyze_failure(exception, context):
        """Analyze failure and suggest fixes."""
        analysis = {
            "exception_type": type(exception).__name__,
            "message": str(exception),
            "context": context,
            "suggestions": []
        }
        
        # Common failure patterns
        if isinstance(exception, KeyError):
            analysis["suggestions"].append(
                f"Missing key: {exception}. Check configuration."
            )
        elif isinstance(exception, ValueError):
            analysis["suggestions"].append(
                "Invalid value. Validate input data."
            )
        elif isinstance(exception, ConnectionError):
            analysis["suggestions"].append(
                "Connection failed. Check network and provider availability."
            )
        
        return analysis

# Usage in tests
def test_with_root_cause_analysis(self):
    """Test with automatic root cause analysis."""
    context = {"input": "test", "config": {...}}
    
    try:
        result = self.feature.process(context)
    except Exception as e:
        analysis = DebugHelper.analyze_failure(e, context)
        pytest.fail(
            f"Test failed:\n"
            f"Analysis: {json.dumps(analysis, indent=2)}"
        )
```

---

## 🎯 Coverage Requirements

### Coverage Targets
- **Overall**: 90%+
- **Core Modules**: 95%+
- **Providers**: 85%+ (external API variations)
- **Utils**: 95%+
- **CLI**: 80%+

### Coverage Configuration
```ini
# .coveragerc
[run]
source = openmux
omit = 
    */tests/*
    */venv/*
    */__init__.py

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = htmlcov
```

### Running Coverage
```bash
# Generate coverage report
pytest --cov=openmux --cov-report=html --cov-report=term

# Check coverage meets threshold
pytest --cov=openmux --cov-fail-under=90
```

### Coverage Analysis
```python
# scripts/check_coverage.py
import coverage
import sys

def check_coverage():
    """Check if coverage meets requirements."""
    cov = coverage.Coverage()
    cov.load()
    
    total = cov.report()
    
    if total < 90:
        print(f"Coverage {total}% is below required 90%")
        sys.exit(1)
    
    print(f"Coverage {total}% meets requirements")
    sys.exit(0)
```

---

## ⚡ Performance Testing

### Latency Benchmarks
```python
# tests/benchmarks/latency_tests.py

import pytest
import time
from statistics import mean, stdev

class TestLatency:
    """Test response latency."""
    
    @pytest.mark.benchmark
    def test_single_query_latency(self, orchestrator):
        """Benchmark single query latency."""
        latencies = []
        
        for _ in range(100):
            start = time.time()
            orchestrator.process("test query")
            latencies.append(time.time() - start)
        
        avg_latency = mean(latencies)
        std_latency = stdev(latencies)
        
        # Assert performance targets
        assert avg_latency < 2.0, f"Average latency {avg_latency}s exceeds 2s target"
        assert std_latency < 0.5, f"Latency std dev {std_latency}s too high"
        
        print(f"Average latency: {avg_latency:.3f}s ± {std_latency:.3f}s")
```

### Throughput Tests
```python
class TestThroughput:
    """Test request throughput."""
    
    @pytest.mark.benchmark
    async def test_concurrent_requests(self, orchestrator):
        """Test concurrent request handling."""
        num_requests = 50
        
        start = time.time()
        tasks = [
            orchestrator.process(f"query {i}")
            for i in range(num_requests)
        ]
        await asyncio.gather(*tasks)
        duration = time.time() - start
        
        throughput = num_requests / duration
        
        assert throughput > 10, f"Throughput {throughput} req/s below target"
        print(f"Throughput: {throughput:.2f} requests/second")
```

### Memory Usage Tests
```python
import tracemalloc

class TestMemory:
    """Test memory usage."""
    
    @pytest.mark.benchmark
    def test_memory_usage(self, orchestrator):
        """Test memory consumption."""
        tracemalloc.start()
        
        # Perform operations
        for _ in range(100):
            orchestrator.process("test query")
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Assert memory limits
        assert peak < 500 * 1024 * 1024, f"Peak memory {peak/1024/1024}MB exceeds 500MB"
        print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")
```

---

## 🔄 Continuous Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install uv
        uv pip install -e ".[dev]"
    
    - name: Run unit tests
      run: |
        pytest tests/unit -v --cov=openmux --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration -v
    
    - name: Check coverage
      run: |
        pytest --cov=openmux --cov-fail-under=90
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

## 📊 Test Reporting

### Test Report Generation
```python
# conftest.py
import pytest
import json

def pytest_sessionfinish(session, exitstatus):
    """Generate test report after session."""
    report = {
        "total_tests": session.testscollected,
        "passed": session.testscollected - session.testsfailed,
        "failed": session.testsfailed,
        "duration": time.time() - session.start_time,
    }
    
    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=2)
```

### Failed Test Analysis
```python
# scripts/analyze_failures.py
def analyze_test_failures():
    """Analyze test failures and provide insights."""
    # Parse pytest output
    # Categorize failures
    # Generate report with suggestions
    pass
```

---

## ✅ Test Execution Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=openmux --cov-report=html

# Run specific test file
pytest tests/unit/test_orchestrator.py

# Run tests matching pattern
pytest -k "test_provider"

# Run with verbose output
pytest -v

# Run with debug output
pytest -s

# Run only unit tests
pytest tests/unit

# Run only integration tests
pytest tests/integration -m integration

# Run benchmarks
pytest tests/benchmarks -m benchmark

# Run and stop on first failure
pytest -x

# Run failed tests from last run
pytest --lf

# Run in parallel
pytest -n auto
```

---

## 🎓 Best Practices Summary

1. **Write Tests First**: Define behavior before implementation
2. **Test Isolation**: Each test should be independent
3. **Clear Names**: Test names should describe what they test
4. **Mock External**: Mock all external dependencies
5. **Comprehensive Coverage**: Test success, failure, and edge cases
6. **Auto-Debug**: Include diagnostic information
7. **Performance**: Track and validate performance metrics
8. **Continuous**: Run tests on every change
9. **Document**: Explain complex test scenarios
10. **Maintain**: Keep tests up-to-date with code changes