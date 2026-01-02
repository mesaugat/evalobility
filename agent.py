#!/usr/bin/env python3

"""
Knowledge Base Agent

This agent demonstrates:
- Connection to AWS Knowledge Base for ecommerce policy information retrieval
- Intelligent determination of search vs. retrieve action
- Query answering from policy documents or general IT/security

Prerequisites:
- AWS credentials configured (via AWS CLI or environment variables)
- Knowledge Base ID set in environment (STRANDS_KNOWLEDGE_BASE_ID)

Environment Variables:
- STRANDS_KNOWLEDGE_BASE_ID: Your AWS Knowledge Base ID
- BEDROCK_GUARDRAIL_ID: Guardrail ID for Bedrock models

How to Run:
1. Set required environment variables
2. Run: python knowledge_base_agent.py
3. Enter user queries
"""

import os
import uuid
from dotenv import load_dotenv

from strands import Agent
from strands.models import BedrockModel
from strands.session.file_session_manager import FileSessionManager
from strands_tools import use_agent, memory

from strands.telemetry.config import StrandsTelemetry

load_dotenv(override=True)

# Check for AWS credentials
if not (os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY")):
    print("\n⚠️  WARNING: AWS credentials are not set!")
    print(
        "Please configure your AWS credentials via the AWS CLI or set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
    )
    exit(1)

# Check for Knowledge Base ID
if not os.environ.get("STRANDS_KNOWLEDGE_BASE_ID"):
    print("\n⚠️  WARNING: STRANDS_KNOWLEDGE_BASE_ID environment variable is not set!")
    print(
        "To use a real knowledge base, please set the STRANDS_KNOWLEDGE_BASE_ID environment variable."
    )
    exit(1)

# Check for Bedrock Guardrail ID
if not os.environ.get("BEDROCK_GUARDRAIL_ID"):
    print("\n⚠️  WARNING: BEDROCK_GUARDRAIL_ID environment variable is not set!")
    print(
        "To use guardrails with Bedrock models, please set the BEDROCK_GUARDRAIL_ID environment variable."
    )
    exit(1)

# System prompt for the main agent with knowledge base access
MAIN_SYSTEM_PROMPT = """You are a helpful assistant for wwktm, an ecommerce company. You help answer questions about company policies, procedures, and compliance documents, as well as general IT/security and ecommerce topics.

When answering questions:
- Use the memory tool to retrieve information from the company's knowledge base for company-specific policies and procedures
- Provide direct, concise answers (aim for less than 100 words unless more detail is requested)
- Maintain conversation context to handle follow-up questions like "tell me more" or "can you elaborate"
- For general technical questions (not company-specific), you can answer directly from your knowledge

Be helpful, accurate, and conversational."""

# Initialize telemetry with OTLP exporter
# telemetry = StrandsTelemetry()
# telemetry.setup_otlp_exporter()

def create_agent_with_session(bedrock_model):
    """Create a new agent with a fresh session.

    Args:
        bedrock_model: The BedrockModel instance to use for the agent

    Returns:
        tuple: (agent, session_id)
    """
    # Generate unique session ID
    session_id = str(uuid.uuid4())

    # Create session manager
    session_manager = FileSessionManager(
        session_id=session_id,
        storage_dir="./sessions"
    )

    # Initialize agent with tools and session manager
    agent = Agent(
        tools=[memory, use_agent],
        model=bedrock_model,
        session_manager=session_manager,
        system_prompt=MAIN_SYSTEM_PROMPT
    )

    return agent, session_id


def run_kb_agent(agent, query):
    """Process a user query with the knowledge base agent."""
    # Simply call the agent - it will decide whether to use tools or not
    answer = agent(query)

    return answer


def main():
    """Main entry point for the knowledge base agent."""



    # Initialize Bedrock model with guardrails (shared across sessions)
    bedrock_model = BedrockModel(
        model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        guardrail_id=os.environ.get("BEDROCK_GUARDRAIL_ID"),
        guardrail_version="2",
        guardrail_trace="enabled",
        streaming=True
    )

    # Create initial agent and session
    agent, session_id = create_agent_with_session(bedrock_model)

    # Print welcome message
    print("\n🧠 Knowledge Base Agent 🧠\n")
    print(f"Session ID: {session_id}")
    print(
        "This agent helps you retrieve information from wwktm (an ecommerce company) policy knowledge base or search for general IT/security or ecommerce knowledge."
    )
    print("\nTry queries like:")
    print('- What is the password policy?')
    print('- What are the MFA requirements?')
    print('- What is the RTO for our payment system?')
    print('- What is our incident response process?')
    print('- What are the data retention requirements?')
    print("\nCommands:")
    print('- Type "exit" or "/q" to exit')
    print('- Type "restart" or "/r"to start a new session')

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() in ["exit", "/q"]:
                print("\nGoodbye! 👋")
                break

            # Handle session restart
            if user_input.lower() in ["restart", "/r"]:
                print("\n🔄 Restarting session...\n")
                # Create new agent and session
                agent, session_id = create_agent_with_session(bedrock_model)
                print(f"✓ New session started")
                print(f"Session ID: {session_id}\n")
                continue

            if not user_input.strip():
                continue

            print("Processing...\n")
            run_kb_agent(agent, user_input)

        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    main()
