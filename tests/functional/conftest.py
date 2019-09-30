import pytest


@pytest.fixture()
def pdf_data():
    from pathlib import Path

    import numpy as np

    cwd = Path.cwd()
    if 'functional' in str(cwd):
        expected = cwd.parent / 'data' / 'test.pdf'
    elif (cwd / 'tests' / 'data' / 'test.pdf').exists():
        expected = cwd / 'tests' / 'data' / 'test.pdf'
    else:
        pass

    yield np.fromfile(expected, dtype=np.int8)
