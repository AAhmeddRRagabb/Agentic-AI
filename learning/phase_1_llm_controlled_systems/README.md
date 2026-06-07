# Phase 1: LLM Controlled Systems

This phase aims to build production-qualityLLMinteraction layerwith structuredoutputs, validation, self
correction, costtracking,andobservability.

## Phase Topics

### 2. LLM API Architecture

Learning LLMs basic concepts:

* How to interact with LLM providers.

* Model selection tradeoffs (capability - cost - latency - tokens processing)

* How to control model behavior through inference parameters (temperature - max output tokens - top p)




## Phase Structure
## 📁 Project Structure

## 📁 Project Structure

```text
phase_1_llm_controlled_systems/
│
├── 🚀 main.py
│   └── Main execution driver for testing LLM generation and streaming across providers.
│
├── 🧠 core.py
│   └── Central abstraction layer that routes requests to the selected LLM provider.
│       Supports both normal generation and streaming generation.
│
├── 🧩 providers/
│   ├── groq.py
│   │   └── Groq API integration layer.
│   │       Handles chat completions, streaming responses, and Groq-specific model calls.
│   │
│   ├── google.py
│   │   └── Google Gemini API integration layer.
│   │       Handles Gemini content generation, streaming, and generation configuration.
│   │
│   └── __init__.py
│       └── Marks the providers directory as a Python package.
│
├── 🛠️ helpers/
│   ├── config.py
│   │   └── Central configuration file.
│   │       Loads API keys, provider names, and model constants from environment settings.
│   │
│   ├── functional.py
│   │   └── Utility functions for formatted printing, error handling, structured output display,
│   │       and debugging helpers.
│   │
│   └── __init__.py
│       └── Marks the helpers directory as a Python package.
│
├── 📚 __info/
│   └── LLM_API_Architecture.pdf
│       └── Learning reference document covering LLM API architecture concepts.
│
└── 📄 README.md
    └── Phase documentation describing the goal, topics, and learning structure.