#!/usr/bin/env python3

"""
Knowledge Base Agent

This agent demonstrates:
- Connection to AWS Knowledge Base for ecommerce policy information retrieval
- Intelligent determination of search vs. retrieve action
- Query answering from policy documents or general IT/security or ecommerce knowledge

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
from dotenv import load_dotenv

from strands import Agent
from strands.models import BedrockModel
from strands_tools import use_agent, memory

load_dotenv(override=True)

# Check for Knowledge Base ID
if not os.environ.get("STRANDS_KNOWLEDGE_BASE_ID"):
    print("\n⚠️  WARNING: STRANDS_KNOWLEDGE_BASE_ID environment variable is not set!")
    print(
        "To use a real knowledge base, please set the STRANDS_KNOWLEDGE_BASE_ID environment variable."
    )

# Check for Bedrock Guardrail ID
if not os.environ.get("BEDROCK_GUARDRAIL_ID"):
    print("\n⚠️  WARNING: BEDROCK_GUARDRAIL_ID environment variable is not set!")
    print(
        "To use guardrails with Bedrock models, please set the BEDROCK_GUARDRAIL_ID environment variable."
    )

# System prompt to determine action
ACTION_SYSTEM_PROMPT = """You are a knowledge base assistant focusing ONLY on classifying user queries.

Your task is to determine whether a user query requires:
- RETRIEVE: Fetching information from the internal knowledge base containing ecommerce company policies, procedures, and compliance documents
- SEARCH: Searching for technical information not specific to the company

Reply with EXACTLY ONE WORD - either "search" or "retrieve".
DO NOT include any explanations or other text.

Examples:
- "What is the company's password policy?" -> retrieve (company policy from knowledge base)
- "What is a strong password hashing algorithm?" -> search (general technical knowledge)
- "What are our MFA requirements?" -> retrieve (company security policy)
- "What is the RTO for our payment system?" -> retrieve (company business continuity policy)
- "What is PCI-DSS?" -> search (general compliance knowledge)
- "What are our data retention requirements?" -> retrieve (company data protection policy)
- "How does OAuth2 work?" -> search (general technical knowledge)
- "What is our incident response process?" -> retrieve (company security policy)
- "What are the latest cybersecurity trends?" -> search (current information from web)
- "What is our policy on remote work?" -> retrieve (company HR/IT policy)

Only respond with "search" or "retrieve" - no explanation, prefix, or any other text."""

# System prompt for generating answers from retrieved information
ANSWER_SYSTEM_PROMPT = """You are a helpful assistant answering questions based on retrieved knowledge base content. Be direct and concise with less than 50 words.

Examples:
- "What is the password policy?" -> "Passwords must be at least 12 characters, avoid common words and reused credentials, and prefer passphrases. Password managers are encouraged for employees."
- "What are the latest cybersecurity trends?" -> "Cybersecurity is dominated by AI-driven threats, including automated malware and deepfake social engineering. Organizations are shifting toward Zero Trust architectures and post-quantum cryptography to safeguard against evolving computing power. Meanwhile, supply chain attacks and triple extortion ransomware remain critical risks to global infrastructure."
"""

SEARCH_SYSTEM_PROMPT = """You are a helpful assistant that provides accurate, concise answers to questions related to technical ecommerce or IT related topics. Provide direct answers within 50 words without mentioning your knowledge cutoff or sources. Do not answer questions unrelated to IT/security or ecommerce topics."""


def determine_action(agent, query):
    """Determine if the user query is a search or retrieve action."""

    result = agent.tool.use_agent(
        prompt=f"Query: {query}",
        system_prompt=ACTION_SYSTEM_PROMPT,
        model_provider="bedrock",
        model_settings={"model_id": "us.anthropic.claude-haiku-4-5-20251001-v1:0"},
    )

    # Clean and extract the action
    action_text = str(result).lower().strip()

    # Check for search or retrieve action
    if "search" in action_text:
        action = "search"
    else:
        # Default to retrieve for knowledge base queries
        action = "retrieve"

    return action


def run_kb_agent(query):
    """Process a user query with the knowledge base agent."""

    # Initialize Bedrock model with guardrails
    bedrock_model = BedrockModel(
        model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        guardrail_id=os.environ.get("BEDROCK_GUARDRAIL_ID"),
        guardrail_version="2",
        guardrail_trace="enabled",
    )

    # Initialize agent with tools
    agent = Agent(tools=[memory, use_agent], model=bedrock_model)

    # Determine the action - search or retrieve
    action = determine_action(agent, query)

    if action == "search":
        # For search actions, use LLM general knowledge
        answer = agent.tool.use_agent(
            prompt=query,
            system_prompt=SEARCH_SYSTEM_PROMPT,
        )
    else:
        # For retrieve actions, query the knowledge base
        result = agent.tool.memory(
            action="retrieve",
            query=query,
            min_score=0.5,
            max_results=5,
        )

        # Convert the result to a string to extract just the content text
        result_str = str(result)

        # Generate a clear, conversational answer using the retrieved information
        answer = agent.tool.use_agent(
            prompt=f'User question: "{query}"\n\nInformation from knowledge base:\n{result_str}\n\nStart your answer with newline character and provide a helpful answer based on this information:',
            system_prompt=ANSWER_SYSTEM_PROMPT,
            model_provider="bedrock",
            model_settings={"model_id": "amazon.nova-pro-v1:0"},
        )

    print(answer)


def main():
    """Main entry point for the knowledge base agent."""
    # Print welcome message
    print("\n🧠 Knowledge Base Agent 🧠\n")
    print(
        "This agent helps you retrieve information from wwktm (an ecommerce company) policy knowledge base or search for general IT/security or ecommerce knowledge."
    )
    print("\nTry queries like:")
    print('- "What is the password policy?"')
    print('- "What are the MFA requirements?"')
    print('- "What is the RTO for our payment system?"')
    print('- "What is our incident response process?"')
    print('- "What are the data retention requirements?"')
    print("\nType your question below or 'exit' to quit:")

    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() in ["exit", "quit"]:
                print("\nGoodbye! 👋")
                break

            if not user_input.strip():
                continue

            # Process the input through the knowledge base agent
            print("Processing...")
            run_kb_agent(user_input)

        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    main()
