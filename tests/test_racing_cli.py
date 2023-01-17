from unittest.mock import patch

import pytest

from report_monaco import Racer, RacingDataAnalyzer

DATA_RACERS = [Racer(lap_time='0:01:04.415000', car='FERRARI', driver='Sebastian Vettel', abr='SVF'),
               Racer(lap_time='0:01:13.065000', car='RENAULT', driver='Nico Hulkenberg', abr='NHR'),
               Racer(lap_time='0:01:12.657000', car='MCLAREN RENAULT', driver='Fernando Alonso', abr='FAM')]

ASC = ('1. Sebastian Vettel  | FERRARI  | 0:01:04.415000\n'
       '2. Fernando Alonso  | MCLAREN RENAULT  | 0:01:12.657000\n'
       '3. Nico Hulkenberg  | RENAULT  | 0:01:13.065000\n')

DESK = ('1. Nico Hulkenberg  | RENAULT  | 0:01:13.065000\n'
        '2. Fernando Alonso  | MCLAREN RENAULT  | 0:01:12.657000\n'
        '3. Sebastian Vettel  | FERRARI  | 0:01:04.415000\n')

DATA_FILES = [['SVF2018-05-24_12:02:58.917'],
              ['SVF2018-05-24_12:04:03.332'],
              ['SVF_Sebastian Vettel_FERRARI']]


@pytest.mark.parametrize('param, direction, expected_result',
                         [(DATA_RACERS, False, ASC),
                          (DATA_RACERS, True, DESK),
                          ])
def test_print_reports(param, direction, expected_result, capsys):
    with patch.object(RacingDataAnalyzer, "__init__", lambda z, y: None):
        class_mock = RacingDataAnalyzer([[str(DATA_RACERS)]])
        class_mock.racer_data = DATA_RACERS
        class_mock.print_reports(direction=direction)
        captured = capsys.readouterr()
    assert captured.out == expected_result


def test_build_report(capsys):
    with patch.object(RacingDataAnalyzer, "__init__", lambda z, y: None):
        class_mock = RacingDataAnalyzer([[str(DATA_RACERS)]])
        class_mock.start_list, class_mock.end_list, class_mock.abbreviations_list = DATA_FILES


def test_driver(capsys):
    with patch.object(RacingDataAnalyzer, "__init__", lambda z, y: None):
        class_mock = RacingDataAnalyzer([[str(DATA_RACERS)]])
        class_mock.racer_data = DATA_RACERS
        class_mock.print_single_racer(driver_name='Fernando Alonso')
        captured = capsys.readouterr()
    assert captured.out == 'Fernando Alonso  | MCLAREN RENAULT  | 0:01:12.657000\n'


def test_find_driver_by_code():
    with patch.object(RacingDataAnalyzer, "__init__", lambda z, y: None):
        class_mock = RacingDataAnalyzer([[str(DATA_RACERS)]])
        class_mock.racer_data = DATA_RACERS
    assert class_mock.find_driver_by_code(driver_code='SVF') == DATA_RACERS[0]


@pytest.mark.parametrize('expected_result, param',
                         [([DATA_RACERS[0], DATA_RACERS[2], DATA_RACERS[1]], False),
                          ([DATA_RACERS[1], DATA_RACERS[2], DATA_RACERS[0]], True),
                          ])
def test_sort_by_time(param, expected_result):
    with patch.object(RacingDataAnalyzer, "__init__", lambda z, y: None):
        class_mock = RacingDataAnalyzer([[str(DATA_RACERS)]])
        class_mock.racer_data = DATA_RACERS
    assert expected_result == class_mock.sort_by_time(direction=param)


def test_enumerate_drivers():
    with patch.object(RacingDataAnalyzer, "__init__", lambda z, y: None):
        class_mock = RacingDataAnalyzer([[str(DATA_RACERS)]])
        class_mock.racer_data = DATA_RACERS
        class_mock.sort_by_time(direction=True)
    assert str(DATA_RACERS[0]) in str(class_mock.enumerate_drivers())


def test_init():
    class_mock = RacingDataAnalyzer(DATA_FILES)
    assert class_mock.start_list, class_mock.abbreviations_list == DATA_FILES
