"""Evaluate generator (general_1)"""

import logging

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig, DisplayConfig
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from langchain_core.runnables import Runnable

from src.main.rag import general_1 as app
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

    question = "Explain the difference between a simile and a metaphor."
    output = chain.invoke(question)
    tc2 = LLMTestCase(
        input=question,
        expected_output="A simile is a figure of speech that compares two things using 'like' or 'as,' while a metaphor directly states that one thing is another.",
        actual_output=output.get("answer"),
    )

    question = "Summarize Newton's first law of motion."
    output = chain.invoke(question)
    tc3 = LLMTestCase(
        input=question,
        expected_output="Newton's first law states that an object at rest will stay at rest, and an object in motion will stay in motion at a constant velocity unless acted upon by an external force.",
        actual_output=output.get("answer"),
    )

    question = "What is the boiling point of water in degrees Celsius at standard atmospheric pressure?"
    output = chain.invoke(question)
    tc4 = LLMTestCase(
        input=question,
        expected_output="100 degrees Celsius",
        actual_output=output.get("answer"),
    )

    question = "What is a haiku?"
    output = chain.invoke(question)
    tc5 = LLMTestCase(
        input=question,
        expected_output="A haiku is a traditional Japanese poem consisting of three lines with a 5-7-5 syllable structure, often focusing on nature.",
        actual_output=output.get("answer"),
    )

    question = "Who was the author of the theory of evolution by natural selection?"
    output = chain.invoke(question)
    tc6 = LLMTestCase(
        input=question,
        expected_output="Charles Darwin",
        actual_output=output.get("answer"),
    )

    question = "Identify one reason why coral reefs are important to marine ecosystems."
    output = chain.invoke(question)
    tc7 = LLMTestCase(
        input=question,
        expected_output="Coral reefs are important because they provide habitat and shelter for many marine species, supporting biodiversity.",
        actual_output=output.get("answer"),
    )

    question = "What is the integral of x^2 with respect to x?"
    output = chain.invoke(question)
    tc8 = LLMTestCase(
        input=question,
        expected_output="(1/3)x^3 + C",
        actual_output=output.get("answer"),
    )

    question = "What are the solutions to the equation 2x^2 - 8x + 6 = 0?"
    output = chain.invoke(question)
    tc9 = LLMTestCase(
        input=question,
        expected_output="x = 1 or x = 3",
        actual_output=output.get("answer"),
    )

    question = "Calculate the value of the following limit: lim (x -> 0) [(sin(x) - x) / x^3]"
    output = chain.invoke(question)
    tc10 = LLMTestCase(
        input=question,
        expected_output="-1/6",
        actual_output=output.get("answer"),
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
        async_config=AsyncConfig(max_concurrent=1, run_async=False),
        display_config=DisplayConfig(show_indicator=False),
    )


if __name__ == "__main__":
    load_dotenv()
    evaluate_test_cases()
