#!/usr/bin/env python3

"""
Knowledge Base Agent

This agent demonstrates:
- Connection to AWS Knowledge Base for ecommerce policy information retrieval
- Intelligent determination of search vs. retrieve action
- Query answering from policy documents or general IT/security

Prerequisites:
- AWS credentials configured (via AWS CLI or environment variables)
- Knowledge Base ID set in environment (KNOWLEDGE_BASE_ID)
- Bedrock Guardrail ID set in environment (BEDROCK_GUARDRAIL_ID)

How to Run:
1. Set required environment variables
2. Run: python knowledge_base_agent.py
3. Enter user queries
"""

import os
import uuid
from dotenv import load_dotenv

from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from strands.telemetry.config import StrandsTelemetry

from agent_config import create_bedrock_model, create_agent

import logging

load_dotenv(override=True)

logging.getLogger("strands").setLevel(os.getenv("LOG_LEVEL", "INFO"))
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", handlers=[logging.StreamHandler()]
)

# Check for AWS credentials
if not (
    os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY")
):
    print("\nWARNING: AWS credentials are not set!")
    print(
        "Please configure your AWS credentials via the AWS CLI or set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
    )
    exit(1)

# Check for Knowledge Base ID
if not os.environ.get("KNOWLEDGE_BASE_ID"):
    print("\nWARNING: KNOWLEDGE_BASE_ID environment variable is not set!")
    print(
        "To use a knowledge base, please set the KNOWLEDGE_BASE_ID environment variable."
    )
    exit(1)

# Check for Bedrock Guardrail ID
if not os.environ.get("BEDROCK_GUARDRAIL_ID"):
    print("\nWARNING: BEDROCK_GUARDRAIL_ID environment variable is not set!")
    print(
        "To use guardrails with Bedrock models, please set the BEDROCK_GUARDRAIL_ID environment variable."
    )
    exit(1)


def run_kb_agent(agent, query):
    """Process a user query with the knowledge base agent."""
    answer = agent(query)

    return answer


def create_session():
    """Create a new session and return session_manager."""
    session_id = str(uuid.uuid4())
    session_manager = FileSessionManager(
        session_id=session_id, storage_dir="./sessions"
    )

    return session_manager


def main():
    """Main entry point for the knowledge base agent."""

    # Create initial session
    session_manager = create_session()

    # Setup telemetry
    # Initialize telemetry with OTLP exporter
    telemetry = StrandsTelemetry()
    telemetry.setup_otlp_exporter()

    bedrock_model = create_bedrock_model()

    agent = create_agent(model=bedrock_model, session_manager=session_manager)

    # Print welcome message
    print("\nwwktm Knowledge Base Agent\n")
    print(f"Session ID: {session_manager.session_id}")
    print(
        "This agent helps you retrieve information from wwktm (an ecommerce company) policy knowledge base or search for general IT/security or ecommerce knowledge."
    )
    print("\nTry queries like:")
    print("- What is the password policy?")
    print("- What are the MFA requirements?")
    print("- What is the RTO for our payment system?")
    print("- What is our incident response process?")
    print("- What are the data retention requirements?")
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
                session_manager = create_session()

                agent = create_agent(
                    model=bedrock_model, session_manager=session_manager
                )

                print(f"✓ New session started")
                print(f"Session ID: {session_manager.session_id}\n")
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
