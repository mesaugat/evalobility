"""
Common Agent Configuration
Shared configuration for creating agents
"""

from typing import Optional
from strands import Agent
from strands.models import BedrockModel
from strands.session.session_manager import SessionManager
from strands_tools import use_agent, retrieve

MODEL_CLAUDE_HAIKU_4_5 = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
MODEL_AMAZON_NOVA_PRO = "us.amazon.nova-pro-v1:0"

SYSTEM_PROMPT = """You are wwktm's AI assistant, helping employees and stakeholders access company information and answer questions about policies, security, compliance, and ecommerce operations.

<role>
Your primary functions:
- Answer questions about wwktm's company policies, procedures, and compliance documents
- Provide information on IT, security, and ecommerce topics relevant to our business
- Help users find and understand internal documentation
</role>

<tools>
You have access to a retrieve tool that searches wwktm's knowledge base containing:
- Company policies (privacy, security, access control, incident response, etc.)
- Operational procedures and guidelines
- Compliance and regulatory documentation

When to use the retrieve tool:
- ANY question about wwktm's specific policies, procedures, or internal documentation
- Questions containing keywords like "our", "company", "wwktm", "policy", "requirement"
- Questions about specific metrics, thresholds, or requirements (e.g., RTO, password length, retention periods)

When to answer directly without tools:
- General knowledge questions about technology, security concepts, or industry practices
- Definitions and explanations of technical terms (e.g., "What is OAuth2?", "What is encryption?")
- Best practices or common patterns that don't reference wwktm specifically
</tools>

<response_guidelines>
1. **Be concise**: Aim for under 100 words unless the user requests more detail
2. **Be accurate**: For policy questions, cite specific requirements from the knowledge base
3. **Be helpful**: If information isn't found, suggest related topics or clarify what you can help with
4. **Be conversational**: Maintain a professional but friendly tone
5. **Cite sources**: When referencing policies, mention the relevant policy name when available
</response_guidelines>

<boundaries>
- Do not make up policy information - always use the retrieve tool for wwktm-specific questions
- Do not provide information that could compromise security
- If uncertain, acknowledge uncertainty and close the query politely
- Do not answer questions outside the scope of tools provided
- Strictly do not answer questions about personal data, financial information, or any sensitive company information
- Strictly avoid going beyond the knowledge base or technical topics
</boundaries>"""


def create_bedrock_model(
    model_id: str = MODEL_CLAUDE_HAIKU_4_5,
    guardrail_id: str | None = None,
    guardrail_version: str | None = "1",
    **kwargs
) -> BedrockModel:
    """
    Create a BedrockModel instance with default configuration.

    Args:
        model_id: Bedrock model identifier
        guardrail_id: Optional guardrail ID
        guardrail_version: Guardrail version

    Returns:
        Configured BedrockModel instance
    """

    return BedrockModel(
        model_id=model_id,
        guardrail_id=guardrail_id,
        guardrail_version=guardrail_version,
        **kwargs
    )


def create_agent(
    model: BedrockModel | None = None,
    system_prompt: str | None = None,
    tools: list | None = None,
    session_manager: Optional[SessionManager] = None,
    **kwargs,
) -> Agent:
    """
    Create an Agent instance with default configuration.

    Args:
        model: BedrockModel to use (creates default if None)
        system_prompt: System prompt (uses SYSTEM_PROMPT if None)
        tools: List of tools (uses [retrieve, use_agent] if None)
        callback_handler: Callback handler (None to disable console output)

    Returns:
        Configured Agent instance
    """

    if system_prompt is None:
        system_prompt = SYSTEM_PROMPT

    if tools is None:
        tools = [retrieve, use_agent]

    return Agent(
        name="wwktm-kb-agent",
        tools=tools,
        model=model,
        system_prompt=system_prompt,
        session_manager=session_manager,
        **kwargs,
    )
