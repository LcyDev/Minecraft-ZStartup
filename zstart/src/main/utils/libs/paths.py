from typing import List, Set, Optional

import os
from pathlib import Path

from common.logger import logger

def expandVars(string) -> str:
    return os.path.expandvars(os.path.expanduser(string))

def absPath(string) -> str:
    """
    Returns the absolute path of a given string, handling user home directories,
    environment variables, and resolving symbolic links.
    """
    try:
        return os.path.realpath(expandVars(string))
    except OSError as _:
        logger.error(f"Error resolving path: {string}")

def mkDirs(path: str) -> None:
    """Creates the directory specified by path, including any necessary parent directories."""
    obj = Path(path)
    if not obj.is_dir():
        try:
            obj.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {path}")
        except OSError as e:
            logger.error(f"Error creating directory: {path}")

