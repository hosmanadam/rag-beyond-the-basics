import logging

from dotenv import load_dotenv

_logger = logging.getLogger(__name__)


def run():
    _logger.info("Running RAG...")


if __name__ == "__main__":
    load_dotenv()
    run()
