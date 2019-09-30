import os
from typing import Tuple

from travel_plan.infrastructure.pdf import PDF
from travel_plan.travel.travels import Travel
from travel_plan.travel.travel_user_units import TravelUserUnit


def make_and_save_pdf(travel: Travel, name: str, path: str):
    """
    Generates and saves a PDF based on a travel object.

    :param travel: the travel object to be modeled as a PDF
    :type travel: Travel
    :param name: the name that's to be used when saving the file
    :type name: str
    :param path: the folder location where the file's to be saved
    :type path: str
    :return: None
    """
    pdf = _generate_pdf(travel)
    _save_file(pdf, name, path)


def _save_file(pdf: PDF, name: str, path: str) -> str:
    """
    Saves a PDF file.

    :param pdf: the pdf file to be saved
    :type pdf: PDF
    :param name: the name that's to be used when saving the file
    :type name: str
    :param path: the folder location where the file's to be saved
    :type path: str
    :return: str
    """

    name += '.pdf'
    working_directory = os.getcwd()
    try:
        os.chdir(path)
        pdf.output(name)
    finally:
        os.chdir(working_directory)


def _generate_pdf(travel: Travel) -> PDF:
    """
    Creates a pdf file.

    :param travel: the travel plan that the pdf's to be based on
    :type travel: Travel
    :return: PDF
    """

    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    pdf.add_cell(22, 'Start Date:', 'L', False, 1, 0, 'C')
    pdf.add_cell(55, 'Entry Point:', 'L', False, 1, 0, 'C')
    pdf.add_cell(22, 'End Date:', 'L', False, 1, 0, 'C')
    pdf.add_cell(55, 'Exit Point:', 'L', False, 1, 0, 'C')
    pdf.add_cell(15, 'Tracked:', 'L', False, 1, 0, 'C')
    pdf.add_cell(20, 'PLB #:', 'L', False, 1, 1, 'C')

    pdf.add_cell(22, str(travel.start_date), 'V', False, 1, 0, 'L')
    pdf.add_cell(55, travel.entry_point.name, 'V', False, 1, 0, 'L')
    pdf.add_cell(22, str(travel.end_date), 'V', False, 1, 0, 'L')
    pdf.add_cell(55, travel.exit_point.name, 'V', False, 1, 0, 'L')
    pdf.add_cell(15, 'Yes' if travel.tracked else 'No', 'V', False, 1, 0, 'L')
    pdf.add_cell(20, travel.plb, 'V', False, 1, 1, 'L')

    pdf.cell(10, 2, '', ln=1)

    # find the trip leader TravelUserUnit that's the trip leader and separate it from the other travelers
    for unit in travel.travelers:
        if unit.traveler.email == travel.trip_leader.email:
            leader_unit = unit
            other_units = list(travel.travelers)
            other_units.remove(leader_unit)
            break

    pdf.add_cell(49, 'Name:', 'L', False, 1, 0, 'C')
    pdf.add_cell(35, 'Radio Call Sign:', 'L', False, 1, 0, 'C')
    pdf.add_cell(35, 'Pack Color:', 'L', False, 1, 0, 'C')
    pdf.add_cell(35, 'Tent Color:', 'L', False, 1, 0, 'C')
    pdf.add_cell(35, 'Fly/Tarp Color:', 'L', False, 1, 1, 'C')

    _write_traveler(pdf, leader_unit)

    for unit in other_units:
        _write_traveler(pdf, unit)

    pdf.cell(10, 2, '', ln=1)

    pdf.add_cell(22, 'Date:', 'L', False, 1, 0, 'C')
    pdf.add_cell(46, 'Starting Point:', 'L', False, 1, 0, 'C')
    pdf.add_cell(46, 'Ending Point:', 'L', False, 1, 0, 'C')
    pdf.add_cell(40, 'Route:', 'L', False, 1, 0, 'C')
    pdf.add_cell(35, 'Mode:', 'L', False, 1, 1, 'C')

    for day in sorted(travel.travel_days):
        pdf.add_cell(22, str(day.date), 'V', False, 1, 0, 'L')
        pdf.add_cell(46, day.starting_point.name, 'V', False, 1, 0, 'L')
        pdf.add_cell(46, day.ending_point.name, 'V', False, 1, 0, 'L')
        pdf.add_cell(40, day.route, 'V', False, 1, 0, 'L')
        pdf.add_cell(35, day.mode, 'V', False, 1, 1, 'L')

    pdf.cell(10, 2, '', ln=1)

    pdf.add_cell(22, 'Plate:', 'L', False, 1, 0, 'C')
    pdf.add_cell(46, 'Make:', 'L', False, 1, 0, 'C')
    pdf.add_cell(46, 'Model:', 'L', False, 1, 0, 'C')
    pdf.add_cell(40, 'Color:', 'L', False, 1, 0, 'C')
    pdf.add_cell(35, 'Location:', 'L', False, 1, 1, 'C')

    pdf.add_cell(22, travel.car.plate, 'V', False, 1, 0, 'L')
    pdf.add_cell(46, travel.car.make, 'V', False, 1, 0, 'L')
    pdf.add_cell(46, travel.car.model, 'V', False, 1, 0, 'L')
    pdf.add_cell(40, travel.car.color.name, 'V', False, 1, 0, 'L')
    pdf.add_cell(35, travel.car_location, 'V', False, 1, 1, 'L')

    pdf.cell(10, 2, '', ln=1)
    y = pdf.get_y()

    eq_ft_sz = 8
    w1 = 7
    w2 = 26
    pdf.add_cell(99, 'Equipment:', 'L', False, 1, 0, 'C')
    pdf.add_cell(30, 'Weapon:', 'L', False, 1, 0, 'C')
    pdf.add_cell(30, 'Days Worth of Food:', 'L', False, 1, 0, 'C')
    pdf.add_cell(30, 'Time You Monitor Radio:', 'L', False, 1, 1, 'C', font_size=7)
    pdf.add_cell(w1, 'X' if travel.bivy_gear else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Bivy Gear', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.head_lamp else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Head Lamp', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.rope else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Rope', 'V', False, 0, 0, 'L')
    pdf.add_cell(30, travel.weapon, 'V', False, 1, 0, 'C')
    pdf.add_cell(30, str(travel.days_of_food), 'V', False, 1, 0, 'C')
    pdf.add_cell(30, travel.radio_monitor_time, 'V', False, 1, 1, 'C')
    pdf.add_cell(w1, 'X' if travel.compass else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Compas', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.helmet else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Helmet', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.shovel else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Shovel', 'V', False, 0, 0, 'L')
    pdf.add_cell(30, 'Off-Trail Map Included?:', 'L', False, 1, 0, 'C', font_size=7)
    pdf.add_cell(30, 'Cell Phone #:', 'L', False, 1, 0, 'C')
    pdf.add_cell(30, 'Satellite Phone #:', 'L', False, 1, 1, 'C', font_size=9)
    pdf.add_cell(w1, 'X' if travel.first_aid_kit else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'First Aid Kit', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.ice_axe else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Ice Axe', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.signal_mirror else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Signal Mirror', 'V', False, 0, 0, 'L')
    pdf.add_cell(30, 'Yes' if travel.off_trail_travel else 'No', 'V', False, 1, 0, 'C')
    pdf.add_cell(30, travel.cell_number, 'V', False, 1, 0, 'C')
    pdf.add_cell(30, travel.satellite_number, 'V', False, 1, 1, 'C')
    pdf.add_cell(w1, 'X' if travel.flagging else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Flagging', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.map else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Map', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.space_blanket else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Space Blanket', 'V', False, 0, 1, 'L')
    pdf.add_cell(w1, 'X' if travel.flare else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Flare', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.matches else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Matches', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.spare_battery else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Spare Battery', 'V', False, 0, 1, 'L')
    pdf.add_cell(w1, 'X' if travel.flashlight else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Flashlight', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.probe_pole else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Probe Pole', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.tent else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Tent', 'V', False, 0, 1, 'L')
    pdf.add_cell(w1, 'X' if travel.gps else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'GPS', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.radio else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Radio', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'X' if travel.whistle else '', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Whistle', 'V', False, 0, 1, 'L')

    pdf.cell(10, 2, '', ln=1)

    pdf.add_cell(41, 'Responsible Party Name:', 'L', False, 1, 0, 'C')
    pdf.add_cell(37, 'Email:', 'L', False, 1, 0, 'C')
    pdf.add_cell(37, 'Work Phone #:', 'L', False, 1, 0, 'C')
    pdf.add_cell(37, 'Home Phone #:', 'L', False, 1, 0, 'C')
    pdf.add_cell(37, 'Cell Phone #:', 'L', False, 1, 1, 'C')

    for rp in travel.contacts:
        pdf.add_cell(41, rp.name, 'V', False, 1, 0, 'L')
        pdf.add_cell(37, rp.email, 'V', False, 1, 0, 'L')
        pdf.add_cell(37, rp.work_number, 'V', False, 1, 0, 'L')
        pdf.add_cell(37, rp.home_number, 'V', False, 1, 0, 'L')
        pdf.add_cell(37, rp.cell_number, 'V', False, 1, 1, 'L')

    pdf.cell(10, 2, '', ln=1)

    x = pdf.get_x()
    y = pdf.get_y()
    gar_width = 15
    gar_height = 34
    for _ in range(10):
        pdf.add_cell(gar_width, ' ', 'L', False, 1, 0, fill=1, height=gar_height)

    gar_x = pdf.get_x()
    gar_y = pdf.get_y()

    pdf.set_font("Arial", 'B', size=8)
    _label(pdf, 'Team Member', x, y, 0, gar_height)
    _label(pdf, 'Supervision', x, y, 1, gar_height)
    _label(pdf, 'Planning', x, y, 2, gar_height)
    _label(pdf, 'Contingency Resources', x, y, 3, gar_height)
    _label(pdf, 'Communication', x, y, 4, gar_height)
    _label(pdf, 'Team Selection', x, y, 5, gar_height)
    _label(pdf, 'Team Fitness', x, y, 6, gar_height)
    _label(pdf, 'Environment', x, y, 7, gar_height)
    _label(pdf, 'Incident Complexity', x, y, 8, gar_height)
    _label(pdf, 'Team Member Total', x, y, 9, gar_height)

    pdf.set_xy(x, y + gar_height)
    _write_gar(pdf, 1, leader_unit, gar_width)
    for i, unit in enumerate(other_units):
        _write_gar(pdf, i + 2, unit, gar_width)

    gar_color_height = 5
    pdf.set_xy(gar_x, gar_y)
    pdf.set_fill_color(*pdf.green)
    pdf.add_cell(39, 'Green: 1-35', 'V', False, 1, 0, 'C', 1, height=gar_color_height)
    pdf.set_xy(gar_x, gar_y + gar_color_height)
    pdf.set_fill_color(*pdf.amber)
    pdf.add_cell(39, 'Amber: 36-60', 'V', False, 1, 0, 'C', 1, height=gar_color_height)
    pdf.set_xy(gar_x, gar_y + 2 * gar_color_height)
    pdf.set_fill_color(*pdf.red)
    pdf.add_cell(39, 'Red: 61-80', 'V', False, 1, 0, 'C', 1, height=gar_color_height)

    pdf.set_xy(gar_x, gar_y + 1 + 3 * gar_color_height)
    pdf.add_cell(39, 'Average Team Member Totals', 'L', False, 1, 1, 'C', font_size=7)
    pdf.set_xy(gar_x, gar_y + 1 + 3 * gar_color_height + pdf.height)
    pdf.set_fill_color(*_set_gar_color(pdf, travel.gar_avg))
    pdf.add_cell(39, str(travel.gar_avg), 'V', False, 1, 0, 'C', 1)
    pdf.set_xy(gar_x, gar_y + 1 + 3 * gar_color_height + 2 * pdf.height)
    pdf.add_cell(39, 'Mitigated GAR', 'L', False, 1, 0, 'C')
    pdf.set_xy(gar_x, gar_y + 1 + 3 * gar_color_height + 3 * pdf.height)
    pdf.set_fill_color(*_set_gar_color(pdf, travel.mitigated_gar))
    pdf.add_cell(39, str(travel.mitigated_gar), 'V', False, 1, 1, 'C', 1)

    pdf.set_y(gar_y + gar_height + 1 + pdf.height * (1 + len(other_units)))

    pdf.add_cell(95, 'Mitigations Taken', 'L', False, 1, 0, 'C', 1)
    pdf.add_cell(94, 'Additional Notes', 'L', False, 1, 1, 'C', 1)
    pdf.multi_cell(95, 4, travel.gar_mitigations, 1, 'L', 0)
    pdf.multi_cell(94, 4, travel.notes, 1, 'L', 0)

    return pdf


def _write_traveler(pdf: PDF, unit):
    """
    Wright a portion of a TravelUserUnit to the PDF

    :param pdf: the PDF that's to be written to
    :type pdf: PDF
    :param unit: the TravelUserUnit to be written
    :return: None
    """
    pdf.add_cell(49, unit.traveler.name, 'V', False, 1, 0, 'L')
    pdf.add_cell(35, unit.call_sign, 'V', False, 1, 0, 'L')
    pdf.add_cell(35, unit.pack_color.name, 'V', False, 1, 0, 'L')
    pdf.add_cell(35, unit.tent_color.name, 'V', False, 1, 0, 'L')
    pdf.add_cell(35, unit.fly_color.name, 'V', False, 1, 1, 'L')


def _label(pdf: PDF, label: str, x: int, y: int, ix: int, h: int):
    """
    Creates a label for the GAR info.

    :param pdf: the pdf that's to be written to
    :type pdf: PDF
    :param label: the text that's to be written into the label
    :type label: str
    :param x: the x location of the label that's to be written
    :type x: int
    :param y: the y locaiton of the label that's to be written
    :type y: int
    :param ix: the index of the particular label in the array of labels
    :type ix: int
    :param h: the height of the label to be made
    :type h: int
    :return: None
    """

    pdf.set_xy(x + ix * 15 - 7, y + h - 3)
    pdf.rotate(75)
    pdf.cell(20, 20, label, 0, 0, 'L')
    pdf.rotate(0)


def _write_gar(pdf: PDF, i: int, unit: TravelUserUnit, width: int):
    """
    Writes the GAR info for one traveler.

    :param pdf: the PDF to be written to
    :type pdf: PDF
    :param i: the index of the traveler
    :type i: int
    :param unit: the traveler unit that's to be written
    :type unit: TravelUserUnit
    :param width: the width of the cell to be written
    :type width: int
    :return: None
    """

    pdf.add_cell(width, str(i), 'V', False, 1, 0, 'C')
    pdf.add_cell(width, str(unit.supervision), 'V', False, 1, 0, 'C')
    pdf.add_cell(width, str(unit.planning), 'V', False, 1, 0, 'C')
    pdf.add_cell(width, str(unit.contingency), 'V', False, 1, 0, 'C')
    pdf.add_cell(width, str(unit.comms), 'V', False, 1, 0, 'C')
    pdf.add_cell(width, str(unit.team_selection), 'V', False, 1, 0, 'C')
    pdf.add_cell(width, str(unit.fitness), 'V', False, 1, 0, 'C')
    pdf.add_cell(width, str(unit.env), 'V', False, 1, 0, 'C')
    pdf.add_cell(width, str(unit.complexity), 'V', False, 1, 0, 'C')
    pdf.set_fill_color(*_set_gar_color(pdf, unit.total_gar_score))
    pdf.add_cell(width, str(unit.total_gar_score), 'V', False, 1, 1, 'C', 1)


def _set_gar_color(pdf, gar_score: int) -> Tuple[int, int, int]:
    """
    Set the background color in accordance to the GAR score.

    :param pdf: the PDF that's to be written to
    :type pdf: PDF
    :param gar_score: the GAR score that's to be referenced
    :type gar_score: int
    :return: Tuple[int, int, int]
    """

    if gar_score < 36:
        return pdf.green
    elif 35 < gar_score < 61:
        return pdf.amber
    else:
        return pdf.red
