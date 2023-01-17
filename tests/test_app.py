from argparse import Namespace
from unittest.mock import patch

import pytest

from report_monaco import main, run_parser

from .test_racing_cli import DATA_FILES


@pytest.mark.parametrize('param, expected_result',
                         [(['--files', 'Road', '--asc'], Namespace(asc=False, driver=None, folder='Road')),
                          (['--files', 'Road', '--desc'], Namespace(asc=True, driver=None, folder='Road')),
                          ])
def test_run_parser(param, expected_result):
    assert run_parser(param) == expected_result


@patch('report_monaco.app.run_parser', return_value=Namespace(asc=None, driver=None, folder='path/to/open'))
def test_main_error(mock_run_parser):
    with pytest.raises(ValueError) as exc:
        main()
        assert "Please select --file dir --asc/--desc or --driver" in str(exc.value)
    mock_run_parser.assert_called_once()


@patch('report_monaco.app.run_parser', return_value=Namespace(asc=True, driver=None, folder='path/to/open'))
@patch('report_monaco.app.validate_path', return_value='path/to/open')
@patch('report_monaco.app.read_files', return_value=DATA_FILES)
@patch('report_monaco.app.RacingDataAnalyzer.build_report', return_value=DATA_FILES)
@patch('report_monaco.app.RacingDataAnalyzer.print_reports', return_value='1. Sebastian Vettel | FERRARI | 0:01:04.415')
def test_main(mock_run_parser, mock_validate_path, mock_read_files, mock_build_report,
              mock_print_reports):
    assert main() == '1. Sebastian Vettel | FERRARI | 0:01:04.415'
    mock_print_reports.assert_called_once()
    mock_build_report.assert_called_once()
    mock_read_files.assert_called_once()
    mock_validate_path.assert_called_once()
    mock_run_parser.assert_called_once()
