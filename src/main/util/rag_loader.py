import importlib
import logging
import pkgutil
from functools import cache
from types import ModuleType
from typing import Dict

from langchain_core.runnables import Runnable

import src.main.rag

_logger = logging.getLogger(__name__)


def _load_modules(package_name: str) -> Dict[str, ModuleType]:
    loaded_modules = {}
    for _, module_name, is_pkg in pkgutil.iter_modules(importlib.import_module(package_name).__path__):
        if not is_pkg:
            full_module_name = f"{package_name}.{module_name}"
            module = importlib.import_module(full_module_name)
            if hasattr(module, "create_chain"):
                loaded_modules[module_name] = module
            else:
                _logger.warning(f"Ignoring module {module.__name__} as it does not have a create_chain method")
    return loaded_modules


_modules = _load_modules(src.main.rag.__name__)
_module_names = list(_modules.keys())
_logger.info(f"Loaded modules: {_module_names}")


@cache
def get(module_name: str) -> Runnable:
    if module_name in _modules:
        return _modules[module_name].create_chain()
    else:
        raise ModuleNotFoundError(f"Module {module_name} not found.")


def get_names():
    return _module_names
