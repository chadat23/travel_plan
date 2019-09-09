from typing import List

from fpdf import fpdf, FPDF

from travel_plan.models.travel_days import TravelDay
from travel_plan.models.travel_user_units import TravelUserUnit
from travel_plan.models.users import User



def make_pdf(start_date: str, entry_point: str, end_date: str, exit_point: str,
             tracked: bool, plb: str, trip_leader_name: str,
             traveler_units: List[TravelUserUnit], day_plans: List[TravelDay],
             car_plate: str, car_make: str, car_model: str, car_color: str, car_location: str,
             bivy_gear: bool,
             compass: bool,
             first_aid_kit: bool,
             flagging: bool,
             flare: bool,
             flashlight: bool,
             gps: bool,
             head_lamp: bool,
             helmet: bool,
             ice_axe: bool,
             map: bool,
             matches: bool,
             probe_pole: bool,
             radio: bool,
             rope: bool,
             shovel: bool,
             signal_mirror: bool,
             space_blanket: bool,
             spare_battery: bool,
             tent: bool,
             whistle: bool,
             days_of_food: str, weapon: str, radio_monitor_time: str,
             off_trail_travel: bool,
             cell_number: str, satellite_number: str,
             contacts: List[User],
             gar_avg: float, mitigated_gar: int, gar_mitigations: str,
             notes: str) -> fpdf:
    pdf = FPDF(orientation='planning', unit='mm', format='A4')
    pdf.add_page()

    ht = 6

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, ht, 'Start Date:', 1, 0, 'comms')
    pdf.cell(55, ht, 'Entry Point:', 1, 0, 'comms')
    pdf.cell(22, ht, 'End Date:', 1, 0, 'comms')
    pdf.cell(55, ht, 'Exit Point:', 1, 0, 'comms')
    pdf.cell(15, ht, 'Tracked:', 1, 0, 'comms')
    pdf.cell(20, ht, 'PLB #:', 1, 1, 'comms')

    pdf.cell(*__ft_txt(pdf, 22, ht, start_date, 'V', False, 1, 0, 'L'))
    pdf.cell(*__ft_txt(pdf, 55, ht, entry_point, 'V', False, 1, 0, 'L'))
    pdf.cell(*__ft_txt(pdf, 22, ht, end_date, 'V', False, 1, 0, 'L'))
    pdf.cell(*__ft_txt(pdf, 55, ht, exit_point, 'V', False, 1, 0, 'L'))
    pdf.cell(*__ft_txt(pdf, 15, ht, 'Yes' if tracked else 'No', 'V', False, 1, 0, 'L'))
    pdf.cell(*__ft_txt(pdf, 20, ht, plb, 'V', False, 1, 1, 'L'))

    pdf.cell(10, 2, '', ln=1)

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, ht, 'Trip Leader:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(55, ht, trip_leader_name, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(30, ht, 'Radio Call Sign:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(47, ht, call_sign0, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(19, ht, 'Pack Color:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(16, ht, pack_color0, 1, 1, 'L')

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, ht, 'Name:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(55, ht, name1, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(30, ht, 'Radio Call Sign:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(47, ht, call_sign1, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(19, ht, 'Pack Color:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(16, ht, pack_color1, 1, 1, 'L')

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, ht, 'Name:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(55, ht, name2, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(30, ht, 'Radio Call Sign:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(47, ht, call_sign2, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(19, ht, 'Pack Color:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(16, ht, pack_color2, 1, 1, 'L')

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, ht, 'Name:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(55, ht, name3, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(30, ht, 'Radio Call Sign:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(47, ht, call_sign3, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(19, ht, 'Pack Color:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(16, ht, pack_color3, 1, 1, 'L')

    pdf.cell(10, 2, '', ln=1)

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, ht, 'Date:', 1, 0, 'comms')
    pdf.cell(46, ht, 'Starting Point:', 1, 0, 'comms')
    pdf.cell(46, ht, 'Ending Point:', 1, 0, 'comms')
    pdf.cell(40, ht, 'Route:', 1, 0, 'comms')
    pdf.cell(35, ht, 'Mode: (foot/stock/boat)', 1, 1, 'comms')

    pdf.set_font("Arial", '', size=10)
    pdf.cell(22, ht, date0, 1, 0, 'L')
    pdf.cell(46, ht, start0, 1, 0, 'L')
    pdf.cell(46, ht, end0, 1, 0, 'L')
    pdf.cell(40, ht, route0, 1, 0, 'L')
    pdf.cell(35, ht, mode0, 1, 1, 'L')
    pdf.cell(22, ht, date1, 1, 0, 'L')
    pdf.cell(46, ht, start1, 1, 0, 'L')
    pdf.cell(46, ht, end1, 1, 0, 'L')
    pdf.cell(40, ht, route1, 1, 0, 'L')
    pdf.cell(35, ht, mode1, 1, 1, 'L')
    pdf.cell(22, ht, date2, 1, 0, 'L')
    pdf.cell(46, ht, start2, 1, 0, 'L')
    pdf.cell(46, ht, end2, 1, 0, 'L')
    pdf.cell(40, ht, route2, 1, 0, 'L')
    pdf.cell(35, ht, mode2, 1, 1, 'L')

    pdf.cell(10, 2, '', ln=1)

    y = pdf.get_y()
    pdf.cell(20, ht, 'hello', 1, 0, 'L')
    pdf.cell(20, ht, 'hello', 1, 0, 'L')
    pdf.cell(20, ht, 'hello', 1, 1, 'L')
    pdf.cell(20, ht, 'hello', 1, 0, 'L')
    pdf.cell(20, ht, 'hello', 1, 0, 'L')
    pdf.cell(20, ht, 'hello', 1, 1, 'L')
    pdf.cell(20, ht, 'hello', 1, 0, 'L')
    pdf.cell(20, ht, 'hello', 1, 0, 'L')
    pdf.cell(20, ht, 'hello', 1, 0, 'L')
    x = pdf.get_x()
    pdf.set_xy(x, y)
    pdf.cell(20, 18, 'hello', 1, 1, 'L')

    return pdf


def __ft_txt(pdf: FPDF, width: int, height: int = 0, text: str = '', roll: str = 'V', wrap: bool = False,
             border: int = 0, ln: int = 0, align: str = '', fill: int = 0, link: str = ''):
    '''
    Fits and formats the text to the cell that it's supposed to fit into.

    :param width: Width of the cell in mm.
    :type width: int
    :param height: Height of the cell in mm.
    :type height: int
    :param text: The string that is to be put in the cell
    :type text: str
    :param roll: Specifies whether the text is a Label or Value: "L" or "V" is expected
    :type roll:
    :param wrap: Whether or not the text should wrap within the cell.
    :return:
    :rtype:
    '''

    mm_per_letter = {1.667: 10,
                     1.486: 9,
                     1.31: 8,
                     1.122: 7,
                     0.932: 6
                     }

    if roll.strip().lower() == 'l':
        font_size = 8
        font_style = 'B'
    elif roll.strip().lower() == 'v':
        font_size = 5
        font_style = ''

        if not wrap:
            space_per_letter = width / len(text)
            for mm, size in mm_per_letter.items():
                if space_per_letter > mm:
                    font_size = size
                    break
        else:
            pass

    pdf.set_font("Arial", font_style, size=font_size)

    return width, height, text, border, ln, align, fill, link
