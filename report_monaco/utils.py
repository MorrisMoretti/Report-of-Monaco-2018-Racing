import os
from typing import List


def validate_path(folder_path: str) -> str:
    """Checks if the folder exists."""
    data_folder = os.path.join(os.path.abspath('.'), folder_path)
    if not os.path.isdir(data_folder):
        raise FileNotFoundError('Folder not found')
    return str(data_folder)


def read_files(data_folder: str) -> List[List[str]]:
    """Read files from files and store in lists"""
    data_from_files = []
    files = ["start.log", "end.log", "abbreviations.txt"]
    for file in files:
        file = os.path.join(data_folder, file)
        with open(file) as file_:
            data_from_files.append([line for line in file_ if line.strip() != ""])
    return data_from_files
