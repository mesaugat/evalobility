#!/usr/bin/env python3

"""
Simple Evaluation for Knowledge Base Agent
https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/quickstart/

This script demonstrates basic output evaluation using the Strands Evals SDK.
"""

from dotenv import load_dotenv

from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator

from agent_config import create_agent

load_dotenv(override=True)


def get_response(case: Case) -> str:
    """
    Task function that runs the agent and returns the response.

    Args:
        case: Test case with input query

    Returns:
        Agent response as string
    """
    # Create agent for this test case using shared configuration
    agent = create_agent(
        callback_handler=None
    )  # Disable console output during evaluation

    response = agent(case.input)
    return str(response)


test_cases = [
    Case[str, str](
        name="policy-password",
        input="What is the password policy?",
        expected_output="Passwords must be at least 12 characters long, avoid common words and reused credentials. Passphrases are preferred. Password managers are encouraged.",
        metadata={"category": "policy", "difficulty": "basic"},
    ),
    Case[str, str](
        name="policy-mfa",
        input="What are the MFA requirements?",
        expected_output="Multi-factor authentication (MFA) is mandatory for administrative, engineering, finance roles, and access to sensitive systems.",
        metadata={"category": "policy", "difficulty": "basic"},
    ),
    Case[str, str](
        name="policy-rto",
        input="What is the RTO for our payment system?",
        expected_output="The Recovery Time Objective (RTO) for the payment system is ≤ 2 hours, and the Recovery Point Objective (RPO) is ≤ 15 minutes.",
        metadata={"category": "policy", "difficulty": "basic"},
    ),
    Case[str, str](
        name="general-encryption",
        input="What is the difference between symmetric and asymmetric encryption?",
        expected_output="Symmetric encryption uses the same key for encryption and decryption (e.g., AES), making it fast but requiring secure key distribution. Asymmetric encryption uses a public-private key pair (e.g., RSA).",
        metadata={"category": "general", "difficulty": "basic"},
    ),
    Case[str, str](
        name="general-ddos",
        input="What is a DDoS attack?",
        expected_output="A Distributed Denial of Service (DDoS) attack attempts to overwhelm a system, network, or service with massive traffic from multiple sources, making it unavailable to legitimate users.",
        metadata={"category": "general", "difficulty": "basic"},
    ),
]

OUTPUT_EVALUATOR_SYSTEM_PROMPT = """You are an expert evaluator for an ecommerce company's knowledge base agent (wwktm).

Your task is to evaluate agent responses across two distinct categories:

**POLICY QUESTIONS** (company-specific):
- Answers should accurately reflect company policies from the knowledge base
- Key topics include: password requirements, MFA policies, RTO/RPO metrics, incident response procedures, data retention
- Responses must be factually correct according to company documentation
- Should be concise (under 100 words unless detail requested)

**GENERAL KNOWLEDGE QUESTIONS** (IT/security/ecommerce):
- Technical definitions and explanations (e.g., encryption types, security attacks, ecommerce concepts)
- Should be accurate based on industry-standard knowledge
- Must be clear and accessible to non-experts
- Should provide practical context where relevant

Evaluate each response objectively against the expected output provided."""

OUTPUT_EVALUATOR_RUBRIC = """Compare the actual response to the expected output and score based on:

1. **Accuracy** (most important): Does the response contain the core factual information from the expected output?
   - For policy questions: Are specific values, requirements, and thresholds correct?
   - For general questions: Is the technical definition/explanation accurate?

2. **Completeness**: Does it cover all key points from the expected output?
   - Missing critical details should reduce the score

3. **Clarity**: Is the information presented clearly and concisely?
   - Avoid unnecessary verbosity
   - Technical terms should be explained appropriately

**Scoring Guidelines:**
- 1.0: Accurate, complete, and clear. All key information present.
- 0.75: Mostly accurate and complete, minor omissions or clarity issues.
- 0.5: Partially correct, missing important details or has some inaccuracies.
- 0.25: Significant inaccuracies or major information gaps.
- 0.0: Incorrect, misleading, or completely misses the question.

**Note**: Slight variations in wording are acceptable if the core meaning matches. Focus on factual correctness over stylistic preferences."""


def main():
    """Run the evaluation."""
    print("EVAL: SIMPLE")
    print(f"Running {len(test_cases)} test cases...")

    evaluator = OutputEvaluator(
        system_prompt=OUTPUT_EVALUATOR_SYSTEM_PROMPT,
        rubric=OUTPUT_EVALUATOR_RUBRIC,
        include_inputs=True,
    )

    experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])
    reports = experiment.run_evaluations(get_response)

    reports[0].run_display()

    print("\nEvaluation complete!")


if __name__ == "__main__":
    main()
