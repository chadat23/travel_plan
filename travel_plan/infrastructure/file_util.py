import os
from typing import List

from werkzeug.datastructures import FileStorage


def save_files(files: List[FileStorage], path: str):
    file_names = [os.path.join(path, f.filename) for f in files]
    [f.save(n) for n, f in zip(file_names, files)]

    return file_names