"""Evaluate generator (nobels_1)"""

import logging

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig, DisplayConfig
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from langchain_core.runnables import Runnable

from src.main.rag import nobels_1 as app
from src.test.metrics import correctness_metric

_logger = logging.getLogger(__name__)


def create_test_cases(chain: Runnable) -> list[LLMTestCase]:
    question = "Who were awarded the 2024 Nobel Prize in Physics?"
    output = chain.invoke(question)
    tc1 = LLMTestCase(
        input=question,
        expected_output="John J. Hopfield and Geoffrey E. Hinton",
        actual_output=output.get("answer"),
    )

    return [tc1]


def evaluate_test_cases():
    _logger.info("Creating test cases...")
    chain = app.create_chain()
    test_cases = create_test_cases(chain)
    _logger.info(f"Evaluating {len(test_cases)} test cases...")
    evaluate(
        test_cases=test_cases,
        metrics=[correctness_metric],
        async_config=AsyncConfig(max_concurrent=1, run_async=False),
        display_config=DisplayConfig(show_indicator=False),
    )


if __name__ == "__main__":
    load_dotenv()
    evaluate_test_cases()
