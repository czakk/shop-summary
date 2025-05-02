"""Utils for the project."""

import pathlib
import re


PROJECT_ROOT_PATH = pathlib.Path(__file__).parent.parent.resolve()

def dir_files(path: pathlib.Path, pattern: str = '*') -> list[pathlib.Path]:
    return [p for p in path.iterdir() if re.match(pattern, str(p.name))]