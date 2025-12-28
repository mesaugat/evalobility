# Knowledge Base Agent with AWS and Datadog Integration

A Strands agent that connects to AWS Knowledge Base for information retrieval with Datadog LLM Observability integration for comprehensive monitoring and tracing.

## Features

- **AWS Knowledge Base Integration**: Store and retrieve information using AWS Bedrock Knowledge Base
- **Datadog LLM Observability**: Full tracing and monitoring of all LLM operations with spans and metrics
- **Intelligent Action Classification**: Automatically determines whether to store or retrieve based on user queries
- **Interactive CLI**: User-friendly command-line interface for easy interaction

## Prerequisites

- Python 3.14+
- AWS account with Knowledge Base configured
- Datadog account with API key
- AWS credentials configured (via AWS CLI or environment variables)

## Installation

1. Install dependencies:
```bash
uv sync
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

## Configuration

### Required Environment Variables

- `STRANDS_KNOWLEDGE_BASE_ID`: Your AWS Knowledge Base ID
- `DD_API_KEY`: Your Datadog API key

### Optional Environment Variables

- `DD_SITE`: Datadog site (default: datadoghq.com)
- `DD_ENV`: Environment name (e.g., dev, staging, prod)
- `DD_SERVICE`: Service name for Datadog (default: knowledge-base-agent)
- `DD_VERSION`: Service version (default: 1.0.0)
- `AWS_ACCESS_KEY_ID`: AWS access key (if not using AWS CLI)
- `AWS_SECRET_ACCESS_KEY`: AWS secret key (if not using AWS CLI)
- `AWS_DEFAULT_REGION`: AWS region (default: us-east-1)

## Usage

Run the agent:
```bash
python knowledge_base_agent.py
```

### Example Interactions

**Storing Information:**
```
> Remember that my birthday is on July 25
✓ Stored: Remember that my birthday is on July 25
```

**Retrieving Information:**
```
> What day is my birthday?
Processing...

Your birthday is on July 25.
```

**Other Examples:**
- "The capital of France is Paris"
- "What is the capital of France?"
- "My favorite color is blue"
- "What's my favorite color?"

## Datadog Observability Features

The agent automatically traces and monitors:

- **Action Classification**: Tracks LLM decisions on store vs. retrieve
- **Knowledge Base Operations**: Monitors all store and retrieve operations
- **Answer Generation**: Traces LLM response generation
- **Error Tracking**: Captures and logs all errors with full context
- **Performance Metrics**: Measures latency and throughput of operations

### Viewing Traces in Datadog

1. Log into your Datadog account
2. Navigate to APM → Traces
3. Filter by service: `knowledge-base-agent`
4. View detailed traces with spans for each operation

## Architecture

```
User Query
    ↓
Action Classification (LLM) [Traced by Datadog]
    ↓
┌─────────────┬─────────────┐
│   Store     │   Retrieve  │
│             │             │
│  AWS KB     │  AWS KB     │ [Traced by Datadog]
│  Store      │  Query      │
└─────────────┤             │
              │  Generate   │
              │  Answer     │ [Traced by Datadog]
              │  (LLM)      │
              └─────────────┘
                    ↓
              Response to User
```

## Error Handling

The agent includes comprehensive error handling:
- Missing environment variables with helpful warnings
- AWS authentication errors
- Knowledge Base access issues
- LLM operation failures

All errors are automatically traced in Datadog for debugging.

## Development

### Project Structure

```
.
├── knowledge_base_agent.py  # Main agent implementation
├── pyproject.toml           # Project dependencies
├── .env.example             # Environment variable template
└── README.md                # This file
```

### Adding New Features

The agent is built using:
- **Strands Framework**: For agent orchestration
- **AWS Bedrock**: For knowledge base operations
- **Datadog ddtrace**: For observability and tracing

## Troubleshooting

### Knowledge Base Not Found
Ensure `STRANDS_KNOWLEDGE_BASE_ID` is set correctly and your AWS credentials have access to the Knowledge Base.

### Datadog Not Receiving Traces
- Verify `DD_API_KEY` is correct
- Check `DD_SITE` matches your Datadog account region
- Ensure network connectivity to Datadog endpoints

### Import Errors
Run `uv sync` to install all dependencies.

## License

MIT

## Contributing

Contributions welcome! Please open an issue or pull request.
