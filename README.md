# Evalobility

An AI agent for wwktm AI Conference 2026 demonstrating RAG-based knowledge base agent with evaluation capabilities using Strands framework.

![Evalobility](./evalobility.png)

[Slides](https://www.canva.com/design/DAG9JohJ1aA/-cuF4bnyQDP3QvCVXUPQvw/edit)

## Overview

This project implements an AI assistant for wwktm (an ecommerce company) that intelligently answers questions about company policies, security, and compliance using AWS Bedrock Knowledge Base. The project includes robust evaluation tools for measuring output quality and tool selection accuracy.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Query                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Agent (Strands Framework)                      │
│  - Claude Haiku 4.5 / Amazon Nova Pro                      │
│  - System Prompt with Role & Guidelines                    │
│  - Bedrock Guardrails for Safety                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌───────────────┐         ┌──────────────────┐
│ Retrieve Tool │         │   Use Agent      │
│  (RAG/KB)     │         │   (Multi-agent)  │
└───────┬───────┘         └──────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│           AWS Bedrock Knowledge Base                        │
│  - 20+ Policy Documents (Privacy, Security, Compliance)     │
│  - Semantic Search & Retrieval                              │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

- **agent.py**: Main interactive CLI agent with session management
- **agent_config.py**: Shared configuration for agent creation (models, prompts, tools)
- **eval_output.py**: Output quality evaluator using LLM-as-judge pattern
- **eval_tool.py**: Tool selection accuracy evaluator for RAG decisions
- **policies/**: Knowledge base with 20+ company policy documents
- **kb_agent_comparison.ipynb**: Jupyter notebook for experimenting with different models and configurations and pushing the data to datadog

## Quick Start

### Prerequisites

- Python 3.14+
- AWS account with Bedrock access
- Knowledge Base configured with policy documents
- AWS credentials configured

### Installation

1. Install dependencies using uv:
```bash
uv sync
```

2. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```bash
# Required
KNOWLEDGE_BASE_ID=your_knowledge_base_id
BEDROCK_GUARDRAIL_ID=your_guardrail_id
BEDROCK_GUARDRAIL_VERSION=1

# Optional - if not using AWS CLI
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Datadog (optional for notebooks to run experiments)
DD_API_KEY=your_dd_api_key
DD_APPLICATION_KEY=your_dd_app_key
DD_ENV=prod
DD_SERVICE=wwktm-kb-agent
```

### Running the Agent

Start the interactive agent:
```bash
python agent.py
```

The agent supports:
- **Policy questions**: "What is the password policy?", "What is the RTO for payment system?"
- **General questions**: "What is OAuth2?", "What is a DDoS attack?"
- **Commands**: `exit` or `/q` to quit, `restart` or `/r` to start new session

### Running Evaluations

**Output Quality Evaluation** (5 test cases):
```bash
python eval_output.py
```
Measures response accuracy, completeness, and clarity using LLM-as-judge.

**Tool Selection Evaluation** (4 test cases):
```bash
python eval_tool.py
```
Validates that the agent correctly uses retrieve tool for policy questions.

## Key Features

- **RAG with AWS Bedrock KB**: Semantic search over 20+ policy documents
- **Session Persistence**: FileSessionManager stores conversation history locally
- **Multi-Model Support**: Claude Haiku 4.5 (default) and Amazon Nova Pro
- **Safety**: Bedrock Guardrails for content filtering
- **Observability**: OpenTelemetry + Datadog integration for tracing
- **Evaluation Framework**: LLM-as-judge for quality and tool usage accuracy

## Dependencies

Core frameworks:
- **strands-agents**: Agent orchestration framework
- **strands-agents-tools**: retrieve, use_agent tools
- **strands-agents-evals**: Evaluation framework with LLM-as-judge
- **boto3**: AWS SDK for Bedrock integration
- **opentelemetry**: Observability and tracing


## License

MIT
