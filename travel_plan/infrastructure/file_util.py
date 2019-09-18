import datetime
import os
from typing import List

from werkzeug.datastructures import FileStorage

from travel_plan.models.travels import Travel


def save_files_with_name(files: List[FileStorage], name: str, path: str):
    """
    Renames and saves files so that they're all named the same short of a suffix number
    :param files:
    :param name:
    :param path:
    :return:
    """
    file_names = []
    for i, file in enumerate(files):
        ext = os.path.splitext(file.filename)[1]
        file_name = f'{name}_{i+1}{ext}'
        full_path = os.path.join(path, file_name)
        file.save(full_path)
        file_names.append(file_name)

    return file_names


def generate_name(leader_name: str, start_date: str) -> str:
    return leader_name.strip().replace(' ', '_').replace(',', '') \
           + '_' \
           + start_date.replace('-', '')
