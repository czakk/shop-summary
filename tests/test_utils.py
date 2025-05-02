import pathlib
import unittest.mock as mock

import src.utils


@mock.patch('pathlib.Path.iterdir')
def test_dir_files(iterdir_mock: mock.MagicMock):
    iterdir_mock.return_value = [pathlib.Path('dummy1.file'), pathlib.Path('dummy2.file'), pathlib.Path('dummy.file')]
    pattern = r'dummy\d.file'

    paths = src.utils.dir_files(pathlib.Path('./'), pattern)

    assert paths == [pathlib.Path('./dummy1.file'), pathlib.Path('./dummy2.file')]