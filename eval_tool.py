#!/usr/bin/env python3

"""
Tool Call Accuracy Evaluation

This script evaluates whether the agent uses the correct tools for different types of queries.
"""

import os
import logging

from dotenv import load_dotenv

from strands_evals import Case, Experiment
from strands_evals.evaluators import ToolSelectionAccuracyEvaluator
from strands_evals.mappers import StrandsInMemorySessionMapper
from strands_evals.telemetry.config import StrandsEvalsTelemetry
from agent_config import MODEL_AMAZON_NOVA_PRO, create_agent

load_dotenv(override=True)

logging.getLogger("strands").setLevel(os.getenv("LOG_LEVEL", "INFO"))
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", handlers=[logging.StreamHandler()]
)

# Setup telemetry
telemetry = StrandsEvalsTelemetry().setup_in_memory_exporter()
memory_exporter = telemetry.in_memory_exporter

test_cases = [
    Case[str, str](
        name="password-policy-use-memory",
        input="What is the password policy?",
        metadata={"category": "policy", "expected_tool": "memory"},
    ),
    Case[str, str](
        name="mfa-requirements-use-memory",
        input="What are the MFA requirements?",
        metadata={"category": "policy", "expected_tool": "memory"},
    ),
    Case[str, str](
        name="rto-payment-use-memory",
        input="What is the RTO for our payment system?",
        metadata={"category": "policy", "expected_tool": "memory"},
    ),
    Case[str, str](
        name="incident-response-use-memory",
        input="What is our incident response process?",
        metadata={"category": "policy", "expected_tool": "memory"},
    ),
]


def run_agent(case: Case) -> dict:
    """
    Run agent with input query and capture tool usage.

    Args:
        case: Test case with input query

    Returns:
        Dict with 'output' (response text) and 'session' (Session with tool calls)
    """
    # Clear previous spans to ensure each test case has a clean session
    memory_exporter.clear()

    # Create agent using shared configuration
    agent = create_agent(model=MODEL_AMAZON_NOVA_PRO, callback_handler=None)

    agent_response = agent(case.input)

    # Map spans to sessions
    finished_spans = memory_exporter.get_finished_spans()
    mapper = StrandsInMemorySessionMapper()
    session = mapper.map_to_session(finished_spans, session_id=case.session_id)

    return {"output": str(agent_response), "trajectory": session}


def main():
    """Run the tool call accuracy evaluation."""
    print("EVAL: TOOL CALL ACCURACY")
    print(f"Running {len(test_cases)} test cases...")

    evaluator = ToolSelectionAccuracyEvaluator()

    experiment = Experiment[str, str](cases=test_cases, evaluators=[evaluator])
    reports = experiment.run_evaluations(run_agent)

    reports[0].run_display()

    print("\nEvaluation complete!")


if __name__ == "__main__":
    main()
