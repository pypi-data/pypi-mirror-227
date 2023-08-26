# ------------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------------
import json
from datetime import datetime
from functools import reduce
import logging
import os
from typing import Any, Callable

from pathlib import Path


def merge_dicts(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    """Collapse a collection of dicts together. Save some starts written to unpack.

    Returns:
        dict[Any]: Collapsed dict from source dicts.
                   A dict on the right have precedence over its left neighbour.
    """
    return reduce(lambda a, b: {**a, **b}, dicts)


def render_now_datetime():
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def indent_string(depth: int, string: str, indent_pattern="    "):
    return depth * indent_pattern + str(string)


def json_dumps(content):
    return json.dumps(content, indent=2)


def stringify_dict_keys(dictionary, to_str_function: Callable[[Any], str] = str):
    return {to_str_function(k): v for k, v in dictionary.items()}


def dump_to_file(content, name_prefix, extension, timestamp=False, log_success=True):
    """Dumps content to the generated files folder. Can be timestamped"""

    name = name_prefix
    if timestamp:
        name += "__" + render_now_datetime()
    name += "." + extension
    path = Path("tests/generated/") / name

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as text_file:
        text_file.write(str(content))

    if log_success:
        logging.info(f"Written to {path}")
