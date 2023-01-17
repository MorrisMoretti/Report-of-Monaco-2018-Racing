from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Racer:
    """
    A class used to represent Racer.
    Attributes
    ----------
    lap_time
        Time in road.
    car
        Model car.
    driver
        Full driver name.
    """
    lap_time: str
    car: str
    driver: str
    abr: str


class RacingDataAnalyzer:
    """
    Class order racers by time and print report that shows the 15 racers(asc or desc) and the rest after underline.
    """

    def __init__(self, raw_data: List[List[str]]) -> None:
        """
        Parameters
        :param raw_data: text from 3 files
        start_list: list
            Data from start.log
        end_list: list
            Data from end.log
        abbreviations_list: list
            Data from abbreviations.txt
        racer_data: list
            Data from func build_report
        """
        self.sorted_data = None
        self.racer_data = None
        self.start_list, self.end_list, self.abbreviations_list = raw_data

    def build_report(self) -> List[Racer]:
        """
        Lap time calculation.
        :return:
            Data with lap time, car and driver name.
        """
        time_reg = '%H:%M:%S.%f'
        racer_data = []
        for start_item in self.start_list:
            end = str([end_time for end_time in self.end_list if (start_item[0:7] in end_time)])
            abbrev = [name.strip() for name in self.abbreviations_list if (start_item[0:3] in name)]
            lap_time = datetime.strptime(end[16:28], time_reg) - datetime.strptime(start_item[14:26], time_reg)
            if '-' not in str(lap_time):
                abr, driver, car = abbrev[0].split('_', 2)
                racer_data.append(Racer(str(lap_time), car, driver, abr))
        self.racer_data = racer_data
        return self.racer_data

    def print_single_racer(self, driver_name: str) -> None:
        """
        Print driver info.
        Parameters
        :param driver_name:
             Full driver name.
        """
        data_driver = next(iter([driver_info for driver_info in self.racer_data if driver_info.driver == driver_name]))
        print(f"{data_driver.driver}  | {data_driver.car}  | {data_driver.lap_time}")

    def print_reports(self, direction: bool) -> None:
        """
        Print report that shows the 15 racers(asc or desc) and the rest after underline.
        Parameters
        :param direction:
              Shows list of drivers and order by [--asc | --desc].
        """
        sorted_data = sorted(self.racer_data, key=lambda time: time.lap_time, reverse=direction)
        enumerate_data = enumerate(sorted_data, start=1)
        for number, data_driver in enumerate_data:
            if number == 16:  # top 15 racers and the rest after underline
                print('_' * 40)
            print(f"{number}. {data_driver.driver}  | {data_driver.car}  | {data_driver.lap_time}")

    def sort_by_time(self, direction: bool) -> List[Racer]:
        """
        Return list that show racers(asc or desc).
        Parameters
        :param direction:
              Sort list of drivers and order by [--asc | --desc].
        """
        self.sorted_data = sorted(self.racer_data, key=lambda time: time.lap_time, reverse=direction)
        return self.sorted_data

    def enumerate_drivers(self) -> List[Racer]:
        """
        Return report with enumerate.
        """
        return list(enumerate(self.sorted_data, start=1))

    def find_driver_by_code(self, driver_code: str) -> Racer:
        """
        Return driver info.
        Parameters
        :param driver_code
        """
        return next(iter([driver_info for driver_info in self.racer_data if driver_info.abr == driver_code]))
