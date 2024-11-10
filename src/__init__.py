import logging

from dotenv import load_dotenv

import src.main.util.git as git
from src.main.util.log import setup_logging
from src.main.util.splash import print_splash

load_dotenv()
setup_logging()

_logger = logging.getLogger(__name__)

app_version = git.get_version()
if git.has_uncommitted_changes():
    print_splash(app_version=app_version + " (UNCOMMITTED CHANGES)")
    _logger.warning(
        "You made some changes in the project. "
        "This may lead to errors, including the inability to run `ws next` and similar commands. "
        "To undo these changes, you can run `git reset --hard`."
    )
else:
    print_splash(app_version=app_version)
