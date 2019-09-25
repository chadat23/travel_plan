def test_color_services_get_names_success(app_w_db, colors):
    from travel_plan.color import color_services

    actual_names = color_services.get_names()

    colors.append('Silver')
    expected_names = sorted(colors)

    assert actual_names == expected_names


def test_color_services_is_present_success(app_w_db, colors):
    from travel_plan.color import color_services

    assert color_services.is_present(colors[0])


def test_color_services_is_present_not_success(app_w_db, colors):
    from travel_plan.color import color_services

    assert not color_services.is_present('Nope')


def test_color_services_add_success(app_w_db, colors):
    from travel_plan.color import color_services

    color = 'Blart'

    assert not color_services.is_present(color)

    assert color_services.add(color)

    assert color_services.is_present(color)


def test_color_services_add_if_not_present_success(app_w_db, colors):
    from travel_plan.color import color_services

    color = 'Blart'

    assert not color_services.is_present(color)

    assert color_services.add_if_not_present(color)

    assert color_services.is_present(color)


def test_color_services_add_if_not_present_not_success(app_w_db, colors):
    from travel_plan.color import color_services

    color = colors[0]

    assert color_services.add_if_not_present(color.lower()) == color
