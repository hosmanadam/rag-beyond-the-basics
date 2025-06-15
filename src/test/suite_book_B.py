"""Evaluate generator and retriever (book_4 - book_6)"""

import logging

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig, DisplayConfig
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from langchain_core.runnables import Runnable

from src.main.rag import book_3 as app
from src.test.metrics import (
    contextual_precision_metric,
    contextual_recall_metric,
    contextual_relevancy_metric,
    correctness_metric
)

_logger = logging.getLogger(__name__)


def create_test_cases(chain: Runnable) -> list[LLMTestCase]:
    question = "What was the main reason Frank Hardy refused to attend the evening school?"
    output = chain.invoke(question)
    tc1 = LLMTestCase(
        input=question,
        expected_output="Frank believed he had a right to his spare time and thought evening school took away from it.",
        actual_output=output.get("answer"),
        retrieval_context=output.get("retrieved_context"),
    )

    question = "How did Walter's mother feel about his decision to join the evening school?"
    output = chain.invoke(question)
    tc2 = LLMTestCase(
        input=question,
        expected_output="She was very supportive and relieved that he was seeking to improve himself.",
        actual_output=output.get("answer"),
        retrieval_context=output.get("retrieved_context"),
    )

    question = "What did the rector say about the value of learning during his sermon?"
    output = chain.invoke(question)
    tc3 = LLMTestCase(
        input=question,
        expected_output="He compared ignorance to living in a dark house and emphasized that knowledge is like opening a window to let in light.",
        actual_output=output.get("answer"),
        retrieval_context=output.get("retrieved_context"),
    )

    question = "What was the consequence of Frank's association with Tom Haines?"
    output = chain.invoke(question)
    tc4 = LLMTestCase(
        input=question,
        expected_output="Frank became involved in poaching and ultimately faced imprisonment.",
        actual_output=output.get("answer"),
        retrieval_context=output.get("retrieved_context"),
    )

    question = "What did Walter think about the relationship between poaching and stealing?"
    output = chain.invoke(question)
    tc5 = LLMTestCase(
        input=question,
        expected_output="Walter believed that poaching was a form of stealing and that it would lead to further criminal behavior.",
        actual_output=output.get("answer"),
        retrieval_context=output.get("retrieved_context"),
    )

    question = "How did Gracie's blindness affect her character compared to her siblings?"
    output = chain.invoke(question)
    tc6 = LLMTestCase(
        input=question,
        expected_output="Gracie became gentle and patient, while her siblings were known for being quarrelsome and disobedient.",
        actual_output=output.get("answer"),
        retrieval_context=output.get("retrieved_context"),
    )

    # Difficult
    question = "What was the significance of the sack found by Walter near Gracie's seat?"
    output = chain.invoke(question)
    tc7 = LLMTestCase(
        input=question,
        expected_output="The sack contained stolen game, indicating Frank's involvement in poaching.",
        actual_output=output.get("answer"),
        retrieval_context=output.get("retrieved_context"),
    )

    # Difficult
    question = "What did Mr. King advise Walter about the use of his spare time?"
    output = chain.invoke(question)
    tc8 = LLMTestCase(
        input=question,
        expected_output="Mr. King warned Walter to be careful with how he used his spare time, as idleness could lead to temptation.",
        actual_output=output.get("answer"),
        retrieval_context=output.get("retrieved_context"),
    )

    question = "What was the outcome of Frank Hardy's trial?"
    output = chain.invoke(question)
    tc9 = LLMTestCase(
        input=question,
        expected_output="Frank was sentenced to two years' imprisonment with hard labor for receiving stolen property.",
        actual_output=output.get("answer"),
        retrieval_context=output.get("retrieved_context"),
    )

    question = "How did Walter's relationship with his mother change after he became successful?"
    output = chain.invoke(question)
    tc10 = LLMTestCase(
        input=question,
        expected_output="Walter was able to provide for his mother, allowing her to retire from the shop and live comfortably.",
        actual_output=output.get("answer"),
        retrieval_context=output.get("retrieved_context"),
    )

    return [tc1, tc2, tc3, tc4, tc5, tc6, tc7, tc8, tc9, tc10]


def evaluate_test_cases():
    _logger.info("Creating test cases...")
    chain = app.create_chain()
    test_cases = create_test_cases(chain)
    _logger.info(f"Evaluating {len(test_cases)} test cases...")
    evaluate(
        test_cases=test_cases,
        metrics=[
            correctness_metric,
            contextual_recall_metric,
            contextual_precision_metric,
            contextual_relevancy_metric,
        ],
        async_config=AsyncConfig(max_concurrent=1, run_async=False),
        display_config=DisplayConfig(show_indicator=False),
    )


if __name__ == "__main__":
    load_dotenv()
    evaluate_test_cases()
