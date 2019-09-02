import pytest

form_data = {'entrydate': '2019-6-18', 'entrypoint': 'May Lake TH',
             'exitdate': '2019-06-20', 'exitpoint': 'May Lake TH',
             }


@pytest.fixture()
def good_form_data():
    yield form_data
