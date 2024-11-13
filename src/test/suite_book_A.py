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
    question = "What was the main reason Frank Hardy refused to attend the evening school?"
    tc1 = LLMTestCase(
        input=question,
        expected_output="Frank believed he had a right to his spare time and thought evening school took away from it.",
        actual_output=chain.invoke(question),
    )

    question = "How did Walter's mother feel about his decision to join the evening school?"
    tc2 = LLMTestCase(
        input=question,
        expected_output="She was very supportive and relieved that he was seeking to improve himself.",
        actual_output=chain.invoke(question),
    )

    question = "What did the rector say about the value of learning during his sermon?"
    tc3 = LLMTestCase(
        input=question,
        expected_output="He compared ignorance to living in a dark house and emphasized that knowledge is like opening a window to let in light.",
        actual_output=chain.invoke(question),
    )

    question = "What was the consequence of Frank's association with Tom Haines?"
    tc4 = LLMTestCase(
        input=question,
        expected_output="Frank became involved in poaching and ultimately faced imprisonment.",
        actual_output=chain.invoke(question),
    )

    question = "What did Walter think about the relationship between poaching and stealing?"
    tc5 = LLMTestCase(
        input=question,
        expected_output="Walter believed that poaching was a form of stealing and that it would lead to further criminal behavior.",
        actual_output=chain.invoke(question),
    )

    question = "How did Gracie's blindness affect her character compared to her siblings?"
    tc6 = LLMTestCase(
        input=question,
        expected_output="Gracie became gentle and patient, while her siblings were known for being quarrelsome and disobedient.",
        actual_output=chain.invoke(question),
    )

    # Difficult
    question = "What was the significance of the sack found by Walter near Gracie's seat?"
    tc7 = LLMTestCase(
        input=question,
        expected_output="The sack contained stolen game, indicating Frank's involvement in poaching.",
        actual_output=chain.invoke(question),
    )

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

    question = "How did Walter's relationship with his mother change after he became successful?"
    tc10 = LLMTestCase(
        input=question,
        expected_output="Walter was able to provide for his mother, allowing her to retire from the shop and live comfortably.",
        actual_output=chain.invoke(question),
    )
    return [tc1, tc2, tc3, tc4, tc5, tc6, tc7, tc8, tc9, tc10]


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
