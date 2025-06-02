import pathlib
import re
import unittest.mock as mock

from src.constans import XLSX_FILE_NAME_PATTERN
import src.utils


@mock.patch('pathlib.Path.iterdir')
def test_dir_files(iterdir_mock: mock.MagicMock):
    iterdir_mock.return_value = [pathlib.Path('dummy1.file'), pathlib.Path('dummy2.file'), pathlib.Path('dummy.file')]
    pattern = r'dummy\d.file'

    paths = src.utils.dir_files(pathlib.Path('./'), pattern)

    assert paths == [pathlib.Path('./dummy1.file'), pathlib.Path('./dummy2.file')]

def test_generate_fake_data():
    dummy_report, dummy_report_path = src.utils.generate_fake_data()

    assert len(dummy_report) == 10
    assert re.match(XLSX_FILE_NAME_PATTERN, dummy_report_path.name)