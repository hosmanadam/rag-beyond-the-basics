"""Evaluate generator (general_1)"""

import logging

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from langchain_core.runnables import Runnable

from src.main import general_1 as app
from src.test.metrics import correctness_metric

_logger = logging.getLogger(__name__)


def create_test_cases(chain: Runnable) -> list[LLMTestCase]:
    question = "What is the main function of mitochondria in a cell?"
    output = chain.invoke(question)
    tc1 = LLMTestCase(
        input=question,
        expected_output="The main function of mitochondria is to produce energy in the form of ATP through cellular respiration.",
        actual_output=output.get("answer"),
    )

    question = "Calculate the value of the following limit: lim (x -> 0) [(sin(x) - x) / x^3]"
    output = chain.invoke(question)
    tc10 = LLMTestCase(
        input=question,
        expected_output="-1/6",
        actual_output=output.get("answer"),
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
