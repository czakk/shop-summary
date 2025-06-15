"""Main script file."""

import os
import shutil

from datetime import datetime

import src.utils as utils

from src.constans import DATE_FORMAT, XLSX_FILE_NAME_PATTERN
from src.report import Report
from src.summary import Summary


def generate_fake_data():
    fake_data_report, fake_data_path = utils.generate_fake_data(10)
    fake_data_report.to_excel(fake_data_path , index=False, header=True)

def main():
    os.makedirs(utils.TEMP_DIR_PATH, exist_ok=True)
    for report_xlsx in utils.dir_files(
            path=utils.PROJECT_ROOT_PATH / 'reports',
            pattern=XLSX_FILE_NAME_PATTERN.replace('.xlsx', '_report.xlsx')
    ):
        os.remove(report_xlsx)

    for report_xlsx in utils.dir_files(
            path=utils.VALIDATION_ERRORS_DIR_PATH,
            pattern=XLSX_FILE_NAME_PATTERN.replace('.xlsx', '_errors.json')
    ):
            os.remove(report_xlsx)

    reports = [
        Report(
            path=report,
            date=datetime.strptime(report.stem, DATE_FORMAT).date(),
        )
        for report in utils.dir_files(path=utils.PROJECT_ROOT_PATH / 'data', pattern=XLSX_FILE_NAME_PATTERN)
    ]
    if not reports:
        raise Exception("No reports found")

    summary = Summary(reports=reports)
    summary.save()

    shutil.rmtree(utils.TEMP_DIR_PATH)

if __name__ == "__main__":
    main()
