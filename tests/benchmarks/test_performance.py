"""
Performance benchmarks for OpenMux.

Measures response times, throughput, and resource usage.
"""
import pytest
import os
from openmux import Orchestrator, TaskType


# Skip benchmarks if API key is not available
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="OPENROUTER_API_KEY not set - skipping benchmarks"
)


class TestOrchestratorBenchmarks:
    """Benchmark orchestrator performance."""
    
    def test_simple_chat_response_time(self, benchmark):
        """Benchmark response time for simple chat queries."""
        orchestrator = Orchestrator()
        
        def run_query():
            return orchestrator.process(
                "Hello", 
                task_type=TaskType.CHAT
            )
        
        result = benchmark(run_query)
        assert result is not None
        
        # Print benchmark stats
        print(f"\nSimple chat benchmark:")
        print(f"  Mean: {benchmark.stats['mean']:.3f}s")
        print(f"  Min: {benchmark.stats['min']:.3f}s")
        print(f"  Max: {benchmark.stats['max']:.3f}s")
    
    def test_code_generation_response_time(self, benchmark):
        """Benchmark response time for code generation."""
        orchestrator = Orchestrator()
        
        def run_query():
            return orchestrator.process(
                "def add(a, b):",
                task_type=TaskType.CODE
            )
        
        result = benchmark(run_query)
        assert result is not None
        
        print(f"\nCode generation benchmark:")
        print(f"  Mean: {benchmark.stats['mean']:.3f}s")
        print(f"  Min: {benchmark.stats['min']:.3f}s")
        print(f"  Max: {benchmark.stats['max']:.3f}s")
    
    def test_classification_overhead(self, benchmark):
        """Benchmark overhead of task classification."""
        orchestrator = Orchestrator()
        
        def run_with_auto_classification():
            return orchestrator.process(
                "What is Python?"
                # No task_type - will auto-classify
            )
        
        result = benchmark(run_with_auto_classification)
        assert result is not None
        
        print(f"\nAuto-classification benchmark:")
        print(f"  Mean: {benchmark.stats['mean']:.3f}s")


class TestProviderPerformance:
    """Benchmark provider-specific performance."""
    
    def test_openrouter_response_time(self, benchmark):
        """Benchmark OpenRouter provider specifically."""
        orchestrator = Orchestrator()
        
        def run_query():
            return orchestrator.process(
                "Quick test",
                task_type=TaskType.CHAT,
                provider_preference=["OpenRouter"]
            )
        
        result = benchmark(run_query)
        assert result is not None
        
        print(f"\nOpenRouter provider benchmark:")
        print(f"  Mean: {benchmark.stats['mean']:.3f}s")
        print(f"  StdDev: {benchmark.stats['stddev']:.3f}s")


class TestConcurrency:
    """Benchmark concurrent request handling."""
    
    def test_sequential_requests(self, benchmark):
        """Benchmark sequential request processing."""
        orchestrator = Orchestrator()
        
        def run_sequential():
            results = []
            for i in range(3):
                result = orchestrator.process(
                    f"Test {i}",
                    task_type=TaskType.CHAT
                )
                results.append(result)
            return results
        
        results = benchmark(run_sequential)
        assert len(results) == 3
        assert all(r is not None for r in results)
        
        print(f"\nSequential (3 requests) benchmark:")
        print(f"  Mean: {benchmark.stats['mean']:.3f}s")
        print(f"  Per request: {benchmark.stats['mean']/3:.3f}s")


class TestMemoryUsage:
    """Benchmark memory usage (requires memory_profiler)."""
    
    def test_orchestrator_initialization_overhead(self, benchmark):
        """Benchmark cost of creating orchestrator instances."""
        def create_orchestrator():
            orch = Orchestrator()
            return orch
        
        orchestrator = benchmark(create_orchestrator)
        assert orchestrator is not None
        
        print(f"\nOrchestrator initialization benchmark:")
        print(f"  Mean: {benchmark.stats['mean']*1000:.2f}ms")
    
    def test_cleanup_performance(self, benchmark):
        """Benchmark cleanup operations."""
        orchestrator = Orchestrator()
        
        # Do a warmup query
        orchestrator.process("Test", task_type=TaskType.CHAT)
        
        def cleanup():
            orchestrator.cleanup()
        
        benchmark(cleanup)
        
        print(f"\nCleanup benchmark:")
        print(f"  Mean: {benchmark.stats['mean']*1000:.2f}ms")


class TestThroughput:
    """Benchmark throughput metrics."""
    
    def test_queries_per_second(self, benchmark):
        """Estimate queries per second throughput."""
        orchestrator = Orchestrator()
        
        def single_query():
            return orchestrator.process(
                "Quick",
                task_type=TaskType.CHAT
            )
        
        result = benchmark(run=single_query)
        
        # Calculate queries per second
        mean_time = benchmark.stats['mean']
        qps = 1 / mean_time if mean_time > 0 else 0
        
        print(f"\nThroughput benchmark:")
        print(f"  Queries/second: {qps:.2f}")
        print(f"  Response time: {mean_time:.3f}s")


if __name__ == "__main__":
    # Run benchmarks
    pytest.main([__file__, "-v", "--benchmark-only", "--benchmark-autosave"])
