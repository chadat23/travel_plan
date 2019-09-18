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
        save_name = os.path.join(path, f'{name}_{i+1}{ext}')
        file.save(save_name)
        file_names.append(save_name)
    # file_names = [os.path.join(path, f.filename) for f in files]
    # [f.save(n) for n, f in zip(file_names, files)]

    return file_names


def generate_name(travel: Travel) -> str:
    return travel.trip_leader.name.strip().replace(' ', '_').replace(',', '') \
           + '_' \
           + datetime.datetime.strftime(travel.start_date, '%Y%m%d')
