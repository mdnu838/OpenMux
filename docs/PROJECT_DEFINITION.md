Project Definition: Free Multi-Source GenAI Orchestration Python Library
Overview

This project will be a Python library available through pip, conda, pixi, uv, and other environments.

The library’s purpose is to automatically select, route, and combine outputs from free GenAI models and free API providers. It creates a unified interface for discovering, connecting, and using open-access models across the AI ecosystem — including OpenRouter (free-tier models), Hugging Face free endpoints, Together AI (community models), Mistral free APIs, Ollama-hosted models, LM Studio, and other publicly available sources.

Core Features

Automatic Provider Discovery

Maintains a list of free, open-access GenAI model providers.

Updates provider metadata automatically from a central registry (JSON or API source).

Only free or open-source endpoints are listed — no paid or key-based commercial APIs.

Task Auto-Classification

Analyzes user queries to classify tasks such as:
chat, code, tts, audio, embeddings, image, or other.

Uses a lightweight local classifier (based on small LLM or rule set).

Allows manual override and displays classification confidence.

Model Auto-Selection

Selects the most suitable free model for each task based on:

Model capability metadata (task tags)

Response quality (historical benchmarks or user votes)

Latency and uptime data

Explains why a model was chosen (transparency report).

Multi-Model Routing and Response Combination

Optionally sends a query to multiple free models.

Collects their responses and applies a configurable combination method, such as:

Concatenate & summarize

Majority vote (for structured outputs)

Secondary summarization model (if local model available)

Designed for text and embeddings first; multimodal support added later.

Offline & Local Fallback

Supports local hosting of free models for offline operation using Ollama, LM Studio, or direct transformers backend.

Bundles lightweight open models (e.g. Phi-3 Mini, Mistral-7B, Llama-3-Instruct-8B, Gemma-2B).

Auto-detects available hardware and switches to offline mode if APIs are unreachable.

Configuration file allows users to pre-define fallback models.

Secure Configuration Management

Stores provider configs and optional local paths securely (encrypted or OS keyring).

Does not store or require API keys unless necessary for access tokens of free-tier services.

Transparency & Logging

Logs which model handled the query, reasoning behind selection, latency, and response size.

Users can enable benchmarking mode to evaluate quality per provider.