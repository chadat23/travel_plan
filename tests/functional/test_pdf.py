def test_get_travel_by_id(travel_object, pdf_data, tmpdir):
    from pathlib import Path
    import numpy as np

    from travel_plan.infrastructure.pdf_util import make_and_save_pdf

    make_and_save_pdf(travel_object, 'test', str(tmpdir))

    actual = tmpdir / 'test.pdf'
    actual = np.fromfile(actual, dtype=np.int8)

    actual = np.concatenate((actual[:4465], actual[4482:]))
    expected = np.concatenate((pdf_data[:4465], pdf_data[4482:]))

    assert np.array_equal(actual, expected)

