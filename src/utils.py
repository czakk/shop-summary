"""Utils for the project."""

import pathlib
import re

from src.constans import DATA_DIR_NAME


PROJECT_ROOT_PATH = pathlib.Path(__file__).parent.parent.resolve()
VALIDATION_ERRORS_DIR_PATH = PROJECT_ROOT_PATH / DATA_DIR_NAME / 'validation_errors'

def dir_files(path: pathlib.Path, pattern: str = '*') -> list[pathlib.Path]:
    return [p for p in path.iterdir() if re.match(pattern, str(p.name))]
