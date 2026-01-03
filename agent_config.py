"""
Common Agent Configuration
Shared configuration for creating agents
"""

import os
from strands import Agent
from strands.models import BedrockModel
from strands_tools import use_agent, memory


SYSTEM_PROMPT = """You are a helpful assistant for wwktm, an ecommerce company. You help answer questions about company policies, procedures, and compliance documents, as well as general IT/security and ecommerce topics.

When answering questions:
- Use the memory tool to retrieve information from the company's knowledge base for company-specific policies and procedures
- Provide direct, concise answers (aim for less than 100 words unless more detail is requested)
- For general technical questions (not company-specific), you can answer directly from your knowledge

Be helpful, accurate, and conversational."""


def create_bedrock_model(
    model_id: str = "us.anthropic.claude-haiku-4-5-20251001-v1:0",
    guardrail_id: str | None = None,
    guardrail_version: str | None = "2",
) -> BedrockModel:
    """
    Create a BedrockModel instance with default configuration.

    Args:
        model_id: Bedrock model identifier
        guardrail_id: Optional guardrail ID (defaults to env var BEDROCK_GUARDRAIL_ID)
        guardrail_version: Guardrail version

    Returns:
        Configured BedrockModel instance
    """
    if guardrail_id is None:
        guardrail_id = os.environ.get("BEDROCK_GUARDRAIL_ID")

    if guardrail_version is None:
        guardrail_version = os.environ.get("BEDROCK_GUARDRAIL_VERSION")

    return BedrockModel(
        model_id=model_id,
        guardrail_id=guardrail_id,
        guardrail_version=guardrail_version,
    )


def create_agent(
    model: BedrockModel | None = None,
    system_prompt: str | None = None,
    tools: list | None = None,
    callback_handler=None,
) -> Agent:
    """
    Create an Agent instance with default configuration.

    Args:
        model: BedrockModel to use (creates default if None)
        system_prompt: System prompt (uses SYSTEM_PROMPT if None)
        tools: List of tools (uses [memory, use_agent] if None)
        callback_handler: Callback handler (None to disable console output)

    Returns:
        Configured Agent instance
    """
    if model is None:
        model = create_bedrock_model()

    if system_prompt is None:
        system_prompt = SYSTEM_PROMPT

    if tools is None:
        tools = [memory, use_agent]

    return Agent(
        tools=tools,
        model=model,
        system_prompt=system_prompt,
        callback_handler=callback_handler,
    )
