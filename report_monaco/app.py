import argparse
from argparse import Namespace
from typing import Optional

from report_monaco.racing_cli import RacingDataAnalyzer
from report_monaco.utils import read_files, validate_path


def run_parser(args: list = None) -> Optional[Namespace]:
    """Run parser with arguments"""
    parser = argparse.ArgumentParser(description="Race statistics")
    parser.add_argument('--files', dest="folder", help="File folder")
    parser.add_argument('--asc', dest="asc", action='store_const', const=False, help='From slow to faster')
    parser.add_argument('--desc', dest="asc", action='store_const', const=True, help='From faster to slow')
    parser.add_argument('--driver', dest="driver", help='driver name')
    return parser.parse_args(args, namespace=None)


def main() -> None:
    args = run_parser()
    if {None} in [{args.asc, args.driver}, {args.folder}]:
        raise ValueError('Please select --file dir --asc/--desc or --driver')
    folder_path = validate_path(args.folder)
    raw_data = read_files(folder_path)
    analyzer = RacingDataAnalyzer(raw_data)
    analyzer.build_report()
    if args.driver is not None:
        return analyzer.print_single_racer(driver_name=args.driver)
    return analyzer.print_reports(direction=args.asc)
