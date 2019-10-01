def test_email_util_email_travel(travel_object, tmpdir):
    from travel_plan.infrastructure import email_util

    result = email_util.email_travel(travel_object, ['a.a', 'b.b'], tmpdir)

    return result


def test_email_util_email_travel_w_nones(travel_object_w_nones, tmpdir):
    from travel_plan.infrastructure import email_util

    result = email_util.email_travel(travel_object_w_nones, ['a.a', 'b.b'], tmpdir)

    return result


def test_email_util_make_subject(travel_object):
    from travel_plan.infrastructure import email_util

    result = email_util._make_subject(travel_object)

    expected = 'Travel itinerary for : Wild 2, Wild Pi, Wild 55'

    assert result == expected


def test_email_util_make_subject_w_nones(travel_object_w_nones):
    from travel_plan.infrastructure import email_util

    result = email_util._make_subject(travel_object_w_nones)

    expected = 'Travel itinerary for : Doe, Jane'

    assert result == expected


def test_email_util_make_body_w_nones(travel_object_w_nones):
    from travel_plan.infrastructure import email_util

    result = email_util._make_body(travel_object_w_nones)

    expected = "Here's the travel itinerary for Doe, Jane.\n Thanks"

    assert result == expected


def test_email_util_make_contact_list(travel_object):
    from travel_plan.infrastructure import email_util

    result = email_util._make_contact_list(travel_object)

    expected = ['chad.derosier+a@gmail.com',
                'chad.derosier+c@gmail.com',
                'chad.derosier+d@gmail.com',
                'chad.derosier+f@gmail.com',
                'chad.derosier+g@gmail.com']

    assert result == expected


def test_email_util_make_contact_list_w_nones(travel_object_w_nones):
    from travel_plan.infrastructure import email_util

    result = email_util._make_contact_list(travel_object_w_nones)

    expected = ['chad.derosier+a@gmail.com', 'chad.derosier+a@gmail.com']

    assert result == expected
    