import os
from unittest.mock import MagicMock, mock_open, patch

import pytest

from report_monaco import read_files, validate_path

FILES = {'path/to/open/start.log': 'SVF2018-05-24_12:02:58.917',
         'path/to/open/end.log': 'SVF2018-05-24_12:04:03.332',
         'path/to/open/abbreviations.txt': 'SVF_Sebastian Vettel_FERRARI'}


@patch('os.path.isdir')
@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_validate_path(mock_isdir, mock_file):
    assert validate_path('path/to/open') == os.path.join(os.path.abspath('.'), 'path/to/open')
    mock_file.assert_called_with(os.path.join(os.path.abspath('.'), 'path/to/open'))
    mock_isdir.assert_not_called()


@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_validate_path_error(mock_file):
    mock_file.assert_not_called()
    with pytest.raises(FileNotFoundError) as exc:
        validate_path('path/to/open')
    assert "Folder not found" in str(exc.value)


def test_read_files():
    with patch('builtins.open', open_mock(FILES)):
        assert read_files('path/to/open') == [[content] for content in FILES.values()]


def open_mock(filename):
    for expected_filename, content in FILES.items():
        if filename == expected_filename:
            return mock_open(read_data=content).return_value
    return MagicMock(side_effect=open_mock)
