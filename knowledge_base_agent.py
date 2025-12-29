#!/usr/bin/env python3

"""
Knowledge Base Agent

This agent demonstrates:
- Connection to AWS Knowledge Base for ecommerce policy information retrieval
- Intelligent determination of search vs. retrieve actions
- Query answering from policy documents

Prerequisites:
- AWS credentials configured (via AWS CLI or environment variables)
- Knowledge Base ID set in environment (STRANDS_KNOWLEDGE_BASE_ID)

Environment Variables:
- STRANDS_KNOWLEDGE_BASE_ID: Your AWS Knowledge Base ID

How to Run:
1. Set required environment variables
2. Run: python knowledge_base_agent.py
3. Enter queries about company policies at the prompt

Example Queries:
- "What is the password policy?"
- "What are the MFA requirements?"
- "What is the RTO for our payment system?"
- "What is our incident response process?"
"""

import os
from dotenv import load_dotenv

from strands import Agent
from strands_tools import use_agent, memory

load_dotenv(override=True)

# Check for Knowledge Base ID
if not os.environ.get("STRANDS_KNOWLEDGE_BASE_ID"):
    print("\n⚠️  WARNING: STRANDS_KNOWLEDGE_BASE_ID environment variable is not set!")
    print(
        "To use a real knowledge base, please set the STRANDS_KNOWLEDGE_BASE_ID environment variable."
    )

KB_ID = os.environ.get("STRANDS_KNOWLEDGE_BASE_ID")

# System prompt to determine action
ACTION_SYSTEM_PROMPT = """You are a knowledge base assistant focusing ONLY on classifying user queries.

Your task is to determine whether a user query requires:
- RETRIEVE: Fetching information from the internal knowledge base containing ecommerce company policies, procedures, and compliance documents
- SEARCH: Searching the web for general knowledge, current events, or technical information not specific to the company

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
ANSWER_SYSTEM_PROMPT = """You are a helpful assistant answering questions based on retrieved knowledge base content. Ignore metadata like IDs or scores. Be direct and concise with less than 50 words.

Examples:
- "What is the password policy?" -> "Passwords must be 12+ characters with special symbols."
- "What is the capital of France?" -> "Paris."
"""

SEARCH_SYSTEM_PROMPT = """You are a helpful assistant that provides accurate, concise answers to general questions. Provide direct answers without mentioning your knowledge cutoff or sources."""


def determine_action(agent, query):
    """Determine if the query is a search or retrieve action."""
    result = agent.tool.use_agent(
        prompt=f"Query: {query}",
        system_prompt=ACTION_SYSTEM_PROMPT,
        model_provider="bedrock",
        model_settings={"model_id": "us.anthropic.claude-sonnet-4-20250514-v1:0"},
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
    # Initialize agent with tools
    agent = Agent(tools=[memory, use_agent])

    # Determine the action - search or retrieve
    action = determine_action(agent, query)

    if action == "search":
        # For search actions, use LLM general knowledge
        answer = agent.tool.use_agent(
            prompt=query,
            system_prompt=SEARCH_SYSTEM_PROMPT,
            model_provider="bedrock",
            model_settings={"model_id": "us.anthropic.claude-sonnet-4-20250514-v1:0"},
        )
        print(answer)
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

        print("\nRetrieved Information from Knowledge Base:\n", result_str)

        # Generate a clear, conversational answer using the retrieved information
        answer = agent.tool.use_agent(
            prompt=f'User question: "{query}"\n\nInformation from knowledge base:\n{result_str}\n\nStart your answer with newline character and provide a helpful answer based on this information:',
            system_prompt=ANSWER_SYSTEM_PROMPT,
            model_provider="bedrock",
            model_settings={"model_id": "us.anthropic.claude-sonnet-4-20250514-v1:0"},
        )
        print(answer)


def main():
    """Main entry point for the knowledge base agent."""
    # Print welcome message
    print("\n🧠 Knowledge Base Agent 🧠\n")
    print(
        "This agent helps you retrieve information from the ecommerce company policy knowledge base."
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
