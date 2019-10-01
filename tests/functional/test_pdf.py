def test_pdf(travel_object, tmpdir):
    from pathlib import Path
    import numpy as np

    from travel_plan.infrastructure.pdf_util import make_and_save_pdf

    make_and_save_pdf(travel_object, 'test', str(tmpdir))

    cwd = Path.cwd()
    if 'functional' in str(cwd):
        expected = cwd.parent / 'data' / 'test.pdf'
    elif (cwd / 'tests' / 'data' / 'test.pdf').exists():
        expected = cwd / 'tests' / 'data' / 'test.pdf'
    else:
        assert False
    expected = np.fromfile(expected, dtype=np.int8)

    actual = tmpdir / 'test.pdf'
    actual = np.fromfile(actual, dtype=np.int8)

    actual = np.concatenate((actual[:4465], actual[4482:]))
    expected = np.concatenate((expected[:4465], expected[4482:]))

    assert np.array_equal(actual, expected)


def test_pdf_w_nones(travel_object_w_nones, tmpdir):
    from pathlib import Path
    import numpy as np

    from travel_plan.infrastructure.pdf_util import make_and_save_pdf

    make_and_save_pdf(travel_object_w_nones, 'test_w_nones', str(tmpdir))

    cwd = Path.cwd()
    if 'functional' in str(cwd):
        expected = cwd.parent / 'data' / 'test_w_nones.pdf'
    elif (cwd / 'tests' / 'data' / 'test_w_nones.pdf').exists():
        expected = cwd / 'tests' / 'data' / 'test_w_nones.pdf'
    else:
        assert False
    expected = np.fromfile(expected, dtype=np.int8)

    actual = tmpdir / 'test_w_nones.pdf'
    actual = np.fromfile(actual, dtype=np.int8)

    actual = np.concatenate((actual[:3260], actual[3285:]))
    expected = np.concatenate((expected[:3260], expected[3285:]))

    assert np.array_equal(actual, expected)

