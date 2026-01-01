# Knowledge Base Agent with Session Management

A conversational Strands agent that intelligently retrieves information from AWS Bedrock Knowledge Base for company policies and answers general IT/security questions, with full session persistence for contextual conversations.

## Features

- **AWS Knowledge Base Integration**: Retrieve company-specific policy information using AWS Bedrock Knowledge Base
- **Session Management**: Full conversation history and state persistence using FileSessionManager
- **Intelligent Tool Usage**: Agent autonomously decides when to use memory tool vs. answering directly
- **Contextual Conversations**: Handles follow-up questions like "tell me more" with full conversation context
- **Bedrock Guardrails**: Built-in content safety with AWS Bedrock Guardrails
- **Interactive CLI**: User-friendly command-line interface with streaming responses

## Prerequisites

- Python 3.10+
- AWS account with Bedrock Knowledge Base configured
- AWS credentials configured (via AWS CLI or environment variables)
- Company policy documents uploaded to AWS Knowledge Base

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

- `STRANDS_KNOWLEDGE_BASE_ID`: Your AWS Bedrock Knowledge Base ID
- `BEDROCK_GUARDRAIL_ID`: Your AWS Bedrock Guardrail ID

### Optional Environment Variables

- `AWS_ACCESS_KEY_ID`: AWS access key (if not using AWS CLI)
- `AWS_SECRET_ACCESS_KEY`: AWS secret key (if not using AWS CLI)
- `AWS_DEFAULT_REGION`: AWS region (default: us-east-1)

## Usage

Run the agent:
```bash
python knowledge_base_agent.py
```

The agent will create a unique session ID and display it. All conversation history will be saved to `./sessions/session_<session_id>/`.

### Example Interactions

**Company Policy Questions:**
```
> What is the password policy?
Processing...

Passwords must be at least 12 characters, avoid common words and reused credentials,
and prefer passphrases. Password managers are encouraged for employees.

> Tell me more about password requirements
Processing...

The policy also requires regular password rotation every 90 days and prohibits
the reuse of the last 5 passwords...
```

**General Technical Questions:**
```
> What is OAuth2?
Processing...

OAuth2 is an authorization framework that enables applications to obtain limited
access to user accounts on an HTTP service...
```

**Conversational Queries:**
```
> Hello!
Processing...

Hello! I'm here to help you with questions about wwktm's company policies and
general IT/security topics. What would you like to know?
```

### More Example Queries

- "What are our MFA requirements?"
- "What is the RTO for our payment system?"
- "What is our incident response process?"
- "What are the data retention requirements?"
- "How does multi-factor authentication work?"
- "Tell me more" (follows up on previous topic)

## Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interaction                         │
│                      (Interactive CLI Loop)                      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Strands Agent (Single Instance)            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  System Prompt: Company Policy Assistant                  │  │
│  │  • Help with wwktm company policies                       │  │
│  │  • Answer IT/security questions                           │  │
│  │  • Maintain conversation context                          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Tools:                                                    │  │
│  │  • memory (AWS Knowledge Base)                            │  │
│  │  • use_agent (nested agent calls)                         │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Model: Claude Haiku 4.5 (Bedrock)                        │  │
│  │  • Streaming enabled                                       │  │
│  │  • Guardrails enabled                                      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────┬───────────────────┘
                      │                       │
                      ▼                       ▼
        ┌─────────────────────┐   ┌─────────────────────────┐
        │  FileSessionManager │   │   Agent Decision Logic  │
        │                     │   │                         │
        │  Session ID: UUID   │   │  Autonomous decision:   │
        │  Storage: ./sessions│   │  • Use memory tool?     │
        │                     │   │  • Answer directly?     │
        │  Persists:          │   │  • Be conversational?   │
        │  • Messages         │   │                         │
        │  • Agent state      │   └─────────┬───────────────┘
        │  • Conversation     │             │
        │    history          │             │
        └──────────┬──────────┘             │
                   │                        │
                   ▼                        ▼
        ┌─────────────────────┐   ┌─────────────────────────┐
        │  Local Filesystem   │   │ AWS Bedrock Knowledge   │
        │                     │   │        Base             │
        │  session_<uuid>/    │   │                         │
        │  ├── session.json   │   │  • Policy documents     │
        │  ├── agents/        │   │  • Procedures           │
        │  │   └── agent_*/   │   │  • Compliance docs      │
        │  │       ├── agent  │   │                         │
        │  │       │   .json  │   │  Retrieved via          │
        │  │       └── messages/│  │  memory tool when       │
        │  │           └── *.json│ │  needed                 │
        └─────────────────────┘   └─────────────────────────┘
```

### Component Flow

1. **User Input**: User enters a query in the interactive CLI
2. **Agent Processing**: Single agent instance (persisted throughout session) receives query
3. **Autonomous Decision**: Agent decides based on context and system prompt:
   - Use `memory` tool to retrieve from Knowledge Base (company policies)
   - Answer directly from LLM knowledge (general questions)
   - Respond conversationally (greetings, follow-ups)
4. **Session Management**: All interactions automatically persisted to filesystem
5. **Context Maintenance**: Full conversation history available for follow-up questions
6. **Streaming Response**: Answer streamed back to user in real-time

### Key Architecture Principles

- **Single Agent Instance**: One agent per session, reused for all queries
- **Autonomous Tool Usage**: Agent decides when to use tools without manual routing
- **Session Persistence**: Automatic state and message persistence via FileSessionManager
- **Contextual Memory**: Full conversation history enables natural follow-up questions
- **Guardrails**: AWS Bedrock Guardrails ensure safe and appropriate responses

## Session Management

### How Sessions Work

Each time you run the agent, a unique session ID is generated. All conversation data is stored in:

```
./sessions/session_<session_id>/
├── session.json              # Session metadata
└── agents/
    └── agent_<agent_id>/
        ├── agent.json        # Agent state
        └── messages/
            ├── message_0.json
            ├── message_1.json
            └── ...
```

### Benefits of Session Management

- **Conversation Continuity**: Follow-up questions like "tell me more" work seamlessly
- **Context Preservation**: Agent remembers entire conversation history
- **State Persistence**: Agent state survives across queries
- **Debugging**: Full conversation logs available for review
- **Multi-Session Support**: Different sessions are isolated from each other

### Reusing Sessions

To reuse a previous session, modify the code to use a specific session ID instead of generating a new UUID:

```python
# Instead of:
session_id = str(uuid.uuid4())

# Use:
session_id = "your-specific-session-id"
```

## Error Handling

The agent includes comprehensive error handling:
- Missing environment variables with helpful warnings
- AWS authentication errors
- Knowledge Base access issues
- LLM operation failures
- Session persistence errors

All errors are caught and displayed with descriptive messages.

## Development

### Project Structure

```
.
├── knowledge_base_agent.py  # Main agent implementation
├── pyproject.toml           # Project dependencies
├── .env.example             # Environment variable template
├── README.md                # This file
├── sessions/                # Session storage directory (auto-created)
└── policies/                # Sample policy documents
    ├── 01_Privacy_Policy.md
    ├── 02_Data_Protection_and_PII_Handling.md
    ├── 03_Terms_of_Service.md
    └── ...
```

### Tech Stack

The agent is built using:
- **Strands Framework**: Agent orchestration and tool management
- **AWS Bedrock**: LLM (Claude Haiku 4.5) and Knowledge Base
- **Strands Tools**: Pre-built tools for memory and agent nesting
- **FileSessionManager**: Session persistence and state management

### Adding New Features

To extend the agent:

1. **Add more tools**: Import and add to agent's tools list
2. **Customize system prompt**: Modify `MAIN_SYSTEM_PROMPT` for different behavior
3. **Change models**: Update `BedrockModel` configuration
4. **Add observability**: Integrate with Datadog, Langsmith, or other observability tools

## Troubleshooting

### Knowledge Base Not Found
Ensure `STRANDS_KNOWLEDGE_BASE_ID` is set correctly and your AWS credentials have access to the Knowledge Base.

### Guardrails Not Working
- Verify `BEDROCK_GUARDRAIL_ID` is correct
- Check guardrail version matches (default: version 2)
- Ensure guardrails are configured in AWS Bedrock console

### Agent Not Using Memory Tool
The agent autonomously decides when to use tools. If it's not using the memory tool for company policy questions:
- Check that the system prompt is clear about when to use memory
- Verify the Knowledge Base contains relevant documents
- Review query phrasing - be specific about company policies

### Session Files Growing Large
Session files accumulate over time. To clean up:
```bash
rm -rf ./sessions/session_*
```

### Import Errors
Run `uv sync` to install all dependencies:
```bash
uv sync
```

## License

MIT

## Contributing

Contributions welcome! Please open an issue or pull request.
