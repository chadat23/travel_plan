def test_email_util_make_contact_list(app_w_db, travel_object, tmpdir):
    from travel_plan.infrastructure import email_util

    result = email_util._make_contact_list(travel_object)

    expected = ['chad.derosier+a@gmail.com', 
                'chad.derosier+c@gmail.com', 
                'chad.derosier+d@gmail.com', 
                'chad.derosier+f@gmail.com', 
                'chad.derosier+g@gmail.com']

    assert result == expected
    