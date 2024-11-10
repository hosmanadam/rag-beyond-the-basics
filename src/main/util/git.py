import logging
import re
from subprocess import call, CalledProcessError, check_output, DEVNULL

_logger = logging.getLogger(__name__)


def get_commit_message() -> str | None:
    return _get_command_output(["git", "log", "-1", "--pretty=%B"])


def get_version() -> str | None:
    commit_message = get_commit_message()
    first_part = commit_message.split()[0]
    if not re.match(r"\d+\.\d+\.\d+", first_part):
        _logger.warning("This commit message doesn't include a version")
        return "?.?.?"
    else:
        return first_part


def has_uncommitted_changes() -> bool:
    has_unstaged_changes = _get_command_exit_code(["git", "diff", "--quiet"])
    if has_unstaged_changes:
        return True
    has_staged_changes = _get_command_exit_code(["git", "diff", "--cached", "--quiet"])
    if has_staged_changes:
        return True
    return False  # Added to ensure the function returns a boolean


def goto(version: str):
    """
    Checkout the commit from master whose message starts with the specified version.
    """
    for line in _git_log_master():
        commit_hash, commit_message = line.split(' ', 1)
        if commit_message.startswith(version):
            _logger.info(f"Checking out commit '{commit_hash}'...")
            _get_command_output(["git", "checkout", commit_hash])
            return

    raise ValueError(f"Did not find version '{version}'.")


def goto_next():
    """
    Checkout the next commit in the master git log based on the current commit hash.
    """
    current_commit = _get_command_output(["git", "rev-parse", "HEAD"])
    log = _git_log_master()

    for i, line in enumerate(log):
        commit_hash, _ = line.split(' ', 1)
        if commit_hash == current_commit:
            if i == 0:
                raise ValueError("Already on the latest version.")
            next_commit_hash, _ = log[i - 1].split(' ', 1)
            _logger.info(f"Checking out next commit '{next_commit_hash}'...")
            _get_command_output(["git", "checkout", next_commit_hash])
            return

    raise ValueError("Current commit not found on master?")


def goto_previous():
    """
    Checkout the previous commit in the master git log based on the current commit hash.
    """
    current_commit = _get_command_output(["git", "rev-parse", "HEAD"])
    log = _git_log_master()

    for i, line in enumerate(log):
        commit_hash, _ = line.split(' ', 1)
        if commit_hash == current_commit:
            if i == len(log) - 3:  # Don't go to first 2 commits, they don't have this script so we'd get stuck
                raise ValueError("Already on the first version.")
            previous_commit_hash, _ = log[i + 1].split(' ', 1)
            _logger.info(f"Checking out previous commit '{previous_commit_hash}'...")
            _get_command_output(["git", "checkout", previous_commit_hash])
            return

    raise ValueError("Current commit not found on master?")


def _git_log_master() -> list[str]:
    """
    Retrieve the master git log in the following form:
    [
      "f47c20447c4b4819da0d04090d4686feda8e7798 0.0.2 Good message",
      "c5768f1a531d77878c3aa90c88bc0ad9d09f4834 0.0.1 Another change",
      "ca6fcf1136f905b2ef16a0c94e2da75b16f1a2a3 0.0.0 Some change",
    ]
    """
    return _get_command_output(["git", "log", "--pretty=format:%H %s", "master"]).split('\n')


def _get_command_output(args: list[str]) -> str | None:
    try:
        return check_output(args=args, stderr=DEVNULL, text=True, shell=False).strip()
    except CalledProcessError as e:
        _logger.error(f"Failed to run '{' '.join(args)}': {e}")
        return None


def _get_command_exit_code(args: list[str]) -> int | None:
    try:
        return call(args=args, stderr=DEVNULL, text=True, shell=False)
    except CalledProcessError as e:
        print(e)
        _logger.error(f"Failed to run '{' '.join(args)}': {e}")
        return None
