"""Evaluate semantic vs. semantic+BM25+contextual"""

import logging

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from langchain_core.runnables import Runnable

from src.main.rag import arxiv_1, arxiv_2
from src.test.metrics import (
    contextual_precision_metric,
    contextual_recall_metric,
    contextual_relevancy_metric,
    correctness_metric
)

_logger = logging.getLogger(__name__)


def create_test_cases(chain: Runnable) -> list[LLMTestCase]:
    question = ""  # TODO
    output = chain.invoke(question)
    tc1 = LLMTestCase(
        input=question,
        expected_output="",  # TODO
        actual_output=output["answer"],
        retrieval_context=output["retrieved_context"],
    )

    return [tc1]


def do_evaluate(sut):
    _logger.info("Creating test cases...")
    chain_basic = sut.create_chain()
    test_cases_basic = create_test_cases(chain_basic)
    _logger.info(f"Evaluating {len(test_cases_basic)} test cases...")
    evaluate(
        test_cases=test_cases_basic,
        metrics=[
            correctness_metric,
            contextual_recall_metric,
            contextual_precision_metric,
            contextual_relevancy_metric,
        ],
        show_indicator=False,
        max_concurrent=1,
        run_async=False,
    )


def evaluate_test_cases():
    _logger.warning("========== BASIC RETRIEVAL ==========")
    do_evaluate(arxiv_1)

    _logger.warning("========== ADVANCED RETRIEVAL ==========")
    do_evaluate(arxiv_2)


if __name__ == "__main__":
    load_dotenv()
    evaluate_test_cases()
