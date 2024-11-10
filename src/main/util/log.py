import logging
import warnings


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    # FIXME: Needs to execute before any deepeval imports
    warnings.filterwarnings("ignore", category=Warning, message=".*deepeval.*")
