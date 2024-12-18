"""Evaluate generator (general_1)"""

import logging

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from langchain_core.runnables import Runnable

from main import general_1 as app
from src.test.metrics import correctness_metric

_logger = logging.getLogger(__name__)


def create_test_cases(chain: Runnable) -> list[LLMTestCase]:
    question = "What is the main function of mitochondria in a cell?"
    tc1 = LLMTestCase(
        input=question,
        expected_output="The main function of mitochondria is to produce energy in the form of ATP through cellular respiration.",
        actual_output=chain.invoke(question),
    )

    question0 = "Calculate the value of the following limit: lim (x -> 0) [(sin(x) - x) / x^3]"
    tc10 = LLMTestCase(
        input=question0,
        expected_output="-1/6",
        actual_output=chain.invoke(question0),
    )

    return [tc1, tc10]


def evaluate_test_cases():
    _logger.info("Creating test cases...")
    chain = app.create_chain()
    test_cases = create_test_cases(chain)
    _logger.info(f"Evaluating {len(test_cases)} test cases...")
    evaluate(
        test_cases=test_cases,
        metrics=[correctness_metric],
        show_indicator=False,
        max_concurrent=1,
        run_async=False,
    )


if __name__ == "__main__":
    load_dotenv()
    evaluate_test_cases()
