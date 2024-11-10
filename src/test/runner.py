import logging

_logger = logging.getLogger(__name__)


def evaluate_all():
    _logger.warning("Evaluating ALL test cases. Maybe save time & money by running only the one you're trying to fix?")


def evaluate_current():
    _logger.warning("Evaluating test cases specific to the current version.")


if __name__ == "__main__":
    evaluate_all()
