from deepeval.metrics import ContextualPrecisionMetric, ContextualRecallMetric, ContextualRelevancyMetric, GEval
from deepeval.test_case import LLMTestCaseParams

from src.main.util.llm_factory import get_evaluation_model

correctness_metric = GEval(
    name="Correctness",
    model=get_evaluation_model(),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    evaluation_steps=[
        "Check whether the facts in 'actual output' contradicts any facts in 'expected output'",
        "You should also lightly penalize omission of detail, and focus on the main idea",
        "Vague language, or contradicting OPINIONS, are OK",
    ],
)

contextual_recall_metric = ContextualRecallMetric(
    model=get_evaluation_model()
)

contextual_precision_metric = ContextualPrecisionMetric(
    model=get_evaluation_model()
)

contextual_relevancy_metric = ContextualRelevancyMetric(
    model=get_evaluation_model()
)
