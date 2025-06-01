"""Main script file."""
import pandas as pd

import src.utils as utils

from datetime import datetime
from src.constans import XLSX_FILE_NAME_PATTERN
from src.report import Report
from src.summary import Summary


def main():
    summary = Summary()
    summary.reports = [
        Report(
            path=report,
            date=datetime.strptime(report.stem, '%Y_%m_%d').date(),
        )
        for report in utils.dir_files(path=utils.PROJECT_ROOT_PATH / 'data', pattern=XLSX_FILE_NAME_PATTERN)
    ]


if __name__ == "__main__":
    main()
