from typing import Tuple

from travel_plan.disseminate.pdf import PDF
from travel_plan.models.travels import Travel
from travel_plan.models.travel_user_units import TravelUserUnit


def generate_pdf(travel: Travel) -> PDF:
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
        pdf.add_cell(22, str(day.date.date()), 'V', False, 1, 0, 'L')
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
    pdf.add_cell(40, travel.car.color, 'V', False, 1, 0, 'L')
    pdf.add_cell(35, travel.car.location, 'V', False, 1, 1, 'L')

    pdf.cell(10, 2, '', ln=1)
    y = pdf.get_y()

    eq_ft_sz = 8
    w1 = 7
    w2 = 26
    pdf.add_cell(99, 'Equipment:', 'L', False, 1, 0, 'C')
    pdf.add_cell(30, 'Weapon:', 'L', False, 1, 0, 'C')
    pdf.add_cell(30, 'Days Worth of Food:', 'L', False, 1, 0, 'C')
    pdf.add_cell(30, 'Time You Monitor Radio:', 'L', False, 1, 1, 'C', font_size=7)
    pdf.add_cell(w1, 'Yes' if travel.bivy_gear else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Bivy Gear', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.head_lamp else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Head Lamp', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.rope else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Rope', 'V', False, 0, 0, 'L')
    pdf.add_cell(30, travel.weapon, 'V', False, 1, 0, 'C')
    pdf.add_cell(30, str(travel.days_of_food), 'V', False, 1, 0, 'C')
    pdf.add_cell(30, travel.radio_monitor_time, 'V', False, 1, 1, 'C')
    pdf.add_cell(w1, 'Yes' if travel.compass else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Compas', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.helmet else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Helmet', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.shovel else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Shovel', 'V', False, 0, 0, 'L')
    pdf.add_cell(30, 'Off-Trail Map Included?:', 'L', False, 1, 0, 'C', font_size=7)
    pdf.add_cell(30, 'Cell Phone #:', 'L', False, 1, 0, 'C')
    pdf.add_cell(30, 'Satellite Phone #:', 'L', False, 1, 1, 'C', font_size=9)
    pdf.add_cell(w1, 'Yes' if travel.first_aid_kit else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'First Aid Kit', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.ice_axe else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Ice Axe', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.signal_mirror else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Signal Mirror', 'V', False, 0, 0, 'L')
    pdf.add_cell(30, 'Yes' if travel.off_trail_travel else 'No', 'V', False, 1, 0, 'C')
    pdf.add_cell(30, travel.cell_number, 'V', False, 1, 0, 'C')
    pdf.add_cell(30, travel.satellite_number, 'V', False, 1, 1, 'C')
    pdf.add_cell(w1, 'Yes' if travel.flagging else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Flagging', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.map else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Map', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.space_blanket else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Space Blanket', 'V', False, 0, 1, 'L')
    pdf.add_cell(w1, 'Yes' if travel.flare else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Flare', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.matches else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Matches', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.spare_battery else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Spare Battery', 'V', False, 0, 1, 'L')
    pdf.add_cell(w1, 'Yes' if travel.flashlight else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Flashlight', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.probe_pole else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Probe Pole', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.tent else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Tent', 'V', False, 0, 1, 'L')
    pdf.add_cell(w1, 'Yes' if travel.gps else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'GPS', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.radio else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
    pdf.add_cell(w2, 'Radio', 'V', False, 0, 0, 'L')
    pdf.add_cell(w1, 'Yes' if travel.whistle else 'No', 'V', False, 1, 0, 'L', font_size=eq_ft_sz)
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
    pdf.add_cell(39, 'Green', 'V', False, 1, 0, 'C', 1, height=gar_color_height)
    pdf.set_xy(gar_x, gar_y + gar_color_height)
    pdf.set_fill_color(*pdf.amber)
    pdf.add_cell(39, 'Amber', 'V', False, 1, 0, 'C', 1, height=gar_color_height)
    pdf.set_xy(gar_x, gar_y + 2 * gar_color_height)
    pdf.set_fill_color(*pdf.red)
    pdf.add_cell(39, 'Red', 'V', False, 1, 0, 'C', 1, height=gar_color_height)

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
    pdf.add_cell(49, unit.traveler.name, 'V', False, 1, 0, 'L')
    pdf.add_cell(35, unit.call_sign, 'V', False, 1, 0, 'L')
    pdf.add_cell(35, unit.pack_color, 'V', False, 1, 0, 'L')
    pdf.add_cell(35, unit.tent_color, 'V', False, 1, 0, 'L')
    pdf.add_cell(35, unit.fly_color, 'V', False, 1, 1, 'L')


def _label(pdf: PDF, label, x, y, dx, h):
    pdf.set_xy(x + dx * 15 - 7, y + h - 3)
    pdf.rotate(75)
    pdf.cell(20, 20, label, 0, 0, 'L')
    pdf.rotate(0)


def _write_gar(pdf: PDF, i: int, unit: TravelUserUnit, width: int):
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
    if gar_score < 36:
        return pdf.green
    elif 35 < gar_score < 61:
        return pdf.amber
    else:
        return pdf.red

# from typing import List

# from fpdf import fpdf, FPDF

# from travel_plan.models.travel_days import TravelDay
# from travel_plan.models.travel_user_units import TravelUserUnit
# from travel_plan.models.users import User



# def make_pdf(start_date: str, entry_point: str, end_date: str, exit_point: str,
#              tracked: bool, plb: str, trip_leader_name: str,
#              traveler_units: List[TravelUserUnit], day_plans: List[TravelDay],
#              car_plate: str, car_make: str, car_model: str, car_color: str, car_location: str,
#              bivy_gear: bool,
#              compass: bool,
#              first_aid_kit: bool,
#              flagging: bool,
#              flare: bool,
#              flashlight: bool,
#              gps: bool,
#              head_lamp: bool,
#              helmet: bool,
#              ice_axe: bool,
#              map: bool,
#              matches: bool,
#              probe_pole: bool,
#              radio: bool,
#              rope: bool,
#              shovel: bool,
#              signal_mirror: bool,
#              space_blanket: bool,
#              spare_battery: bool,
#              tent: bool,
#              whistle: bool,
#              days_of_food: str, weapon: str, radio_monitor_time: str,
#              off_trail_travel: bool,
#              cell_number: str, satellite_number: str,
#              contacts: List[User],
#              gar_avg: float, mitigated_gar: int, gar_mitigations: str,
#              notes: str) -> fpdf:
#     pdf = FPDF(orientation='planning', unit='mm', format='A4')
#     pdf.add_page()

#     ht = 6

#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(22, ht, 'Start Date:', 1, 0, 'comms')
#     pdf.cell(55, ht, 'Entry Point:', 1, 0, 'comms')
#     pdf.cell(22, ht, 'End Date:', 1, 0, 'comms')
#     pdf.cell(55, ht, 'Exit Point:', 1, 0, 'comms')
#     pdf.cell(15, ht, 'Tracked:', 1, 0, 'comms')
#     pdf.cell(20, ht, 'PLB #:', 1, 1, 'comms')

#     pdf.cell(*__ft_txt(pdf, 22, ht, start_date, 'V', False, 1, 0, 'L'))
#     pdf.cell(*__ft_txt(pdf, 55, ht, entry_point, 'V', False, 1, 0, 'L'))
#     pdf.cell(*__ft_txt(pdf, 22, ht, end_date, 'V', False, 1, 0, 'L'))
#     pdf.cell(*__ft_txt(pdf, 55, ht, exit_point, 'V', False, 1, 0, 'L'))
#     pdf.cell(*__ft_txt(pdf, 15, ht, 'Yes' if tracked else 'No', 'V', False, 1, 0, 'L'))
#     pdf.cell(*__ft_txt(pdf, 20, ht, plb, 'V', False, 1, 1, 'L'))

#     pdf.cell(10, 2, '', ln=1)

#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(22, ht, 'Trip Leader:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(55, ht, trip_leader_name, 1, 0, 'L')
#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(30, ht, 'Radio Call Sign:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(47, ht, call_sign0, 1, 0, 'L')
#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(19, ht, 'Pack Color:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(16, ht, pack_color0, 1, 1, 'L')

#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(22, ht, 'Name:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(55, ht, name1, 1, 0, 'L')
#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(30, ht, 'Radio Call Sign:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(47, ht, call_sign1, 1, 0, 'L')
#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(19, ht, 'Pack Color:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(16, ht, pack_color1, 1, 1, 'L')

#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(22, ht, 'Name:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(55, ht, name2, 1, 0, 'L')
#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(30, ht, 'Radio Call Sign:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(47, ht, call_sign2, 1, 0, 'L')
#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(19, ht, 'Pack Color:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(16, ht, pack_color2, 1, 1, 'L')

#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(22, ht, 'Name:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(55, ht, name3, 1, 0, 'L')
#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(30, ht, 'Radio Call Sign:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(47, ht, call_sign3, 1, 0, 'L')
#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(19, ht, 'Pack Color:', 1, 0, 'L')
#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(16, ht, pack_color3, 1, 1, 'L')

#     pdf.cell(10, 2, '', ln=1)

#     pdf.set_font("Arial", 'B', size=8)
#     pdf.cell(22, ht, 'Date:', 1, 0, 'comms')
#     pdf.cell(46, ht, 'Starting Point:', 1, 0, 'comms')
#     pdf.cell(46, ht, 'Ending Point:', 1, 0, 'comms')
#     pdf.cell(40, ht, 'Route:', 1, 0, 'comms')
#     pdf.cell(35, ht, 'Mode: (foot/stock/boat)', 1, 1, 'comms')

#     pdf.set_font("Arial", '', size=10)
#     pdf.cell(22, ht, date0, 1, 0, 'L')
#     pdf.cell(46, ht, start0, 1, 0, 'L')
#     pdf.cell(46, ht, end0, 1, 0, 'L')
#     pdf.cell(40, ht, route0, 1, 0, 'L')
#     pdf.cell(35, ht, mode0, 1, 1, 'L')
#     pdf.cell(22, ht, date1, 1, 0, 'L')
#     pdf.cell(46, ht, start1, 1, 0, 'L')
#     pdf.cell(46, ht, end1, 1, 0, 'L')
#     pdf.cell(40, ht, route1, 1, 0, 'L')
#     pdf.cell(35, ht, mode1, 1, 1, 'L')
#     pdf.cell(22, ht, date2, 1, 0, 'L')
#     pdf.cell(46, ht, start2, 1, 0, 'L')
#     pdf.cell(46, ht, end2, 1, 0, 'L')
#     pdf.cell(40, ht, route2, 1, 0, 'L')
#     pdf.cell(35, ht, mode2, 1, 1, 'L')

#     pdf.cell(10, 2, '', ln=1)

#     y = pdf.get_y()
#     pdf.cell(20, ht, 'hello', 1, 0, 'L')
#     pdf.cell(20, ht, 'hello', 1, 0, 'L')
#     pdf.cell(20, ht, 'hello', 1, 1, 'L')
#     pdf.cell(20, ht, 'hello', 1, 0, 'L')
#     pdf.cell(20, ht, 'hello', 1, 0, 'L')
#     pdf.cell(20, ht, 'hello', 1, 1, 'L')
#     pdf.cell(20, ht, 'hello', 1, 0, 'L')
#     pdf.cell(20, ht, 'hello', 1, 0, 'L')
#     pdf.cell(20, ht, 'hello', 1, 0, 'L')
#     x = pdf.get_x()
#     pdf.set_xy(x, y)
#     pdf.cell(20, 18, 'hello', 1, 1, 'L')

#     return pdf


# def __ft_txt(pdf: FPDF, width: int, height: int = 0, text: str = '', roll: str = 'V', wrap: bool = False,
#              border: int = 0, ln: int = 0, align: str = '', fill: int = 0, link: str = ''):
#     '''
#     Fits and formats the text to the cell that it's supposed to fit into.

#     :param width: Width of the cell in mm.
#     :type width: int
#     :param height: Height of the cell in mm.
#     :type height: int
#     :param text: The string that is to be put in the cell
#     :type text: str
#     :param roll: Specifies whether the text is a Label or Value: "L" or "V" is expected
#     :type roll:
#     :param wrap: Whether or not the text should wrap within the cell.
#     :return:
#     :rtype:
#     '''

#     mm_per_letter = {1.667: 10,
#                      1.486: 9,
#                      1.31: 8,
#                      1.122: 7,
#                      0.932: 6
#                      }

#     if roll.strip().lower() == 'l':
#         font_size = 8
#         font_style = 'B'
#     elif roll.strip().lower() == 'v':
#         font_size = 5
#         font_style = ''

#         if not wrap:
#             space_per_letter = width / len(text)
#             for mm, size in mm_per_letter.items():
#                 if space_per_letter > mm:
#                     font_size = size
#                     break
#         else:
#             pass

#     pdf.set_font("Arial", font_style, size=font_size)

#     return width, height, text, border, ln, align, fill, link
