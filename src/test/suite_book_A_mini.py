"""Evaluate generator (book_1 - book_3)"""

import logging

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from langchain_core.runnables import Runnable

from main import book_1 as app
from src.test.metrics import correctness_metric

_logger = logging.getLogger(__name__)


def create_test_cases(chain: Runnable) -> list[LLMTestCase]:
    # Difficult
    question = "What did Mr. King advise Walter about the use of his spare time?"
    tc8 = LLMTestCase(
        input=question,
        expected_output="Mr. King warned Walter to be careful with how he used his spare time, as idleness could lead to temptation.",
        actual_output=chain.invoke(question),
    )

    question = "What was the outcome of Frank Hardy's trial?"
    tc9 = LLMTestCase(
        input=question,
        expected_output="Frank was sentenced to two years' imprisonment with hard labor for receiving stolen property.",
        actual_output=chain.invoke(question),
    )

    return [tc8, tc9]


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
