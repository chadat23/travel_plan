from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
import shutil
import smtplib
from typing import List

from fpdf import FPDF

from travel_plan.config import PDF_FOLDER_PATH
from travel_plan.models.travel_user_units import TravelUserUnit
from travel_plan.models.travels import Travel
from travel_plan.disseminate.pdf import PDF

try:
    from travel_plan.config import EMAIL_ADDRESS, EMAIL_PASSWORD
except:
    print('*' * 10 + ' Did you create a config.py file from the config_example.py file? ' + '*' * 10)


def save_file(pdf: PDF, name: str, start_date: str) -> str:
    name = name.strip().replace(' ', '_').replace(',', '') + '_' + start_date.replace('-', '') + '.pdf'
    # pdf.output(name)
    # save_path = tempfile.mkdtemp()
    save_path = PDF_FOLDER_PATH
    working_directory = os.getcwd()
    try:
        os.chdir(save_path)
        pdf.output(name)
    finally:
        os.chdir(working_directory)

    return os.path.join(save_path, name)


def delete_file(file: str):
    shutil.rmtree(os.path.abspath(os.path.join(file, os.pardir)))


def send_mail(recipients: List[str], file: str):
    COMMASPACE = ', '

    sender = EMAIL_ADDRESS
    gmail_password = EMAIL_PASSWORD
    recipients = recipients

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'EMAIL SUBJECT'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    text = "Here's my email body!"
    outer.attach(MIMEText(text, 'plain'))
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    # attachments = ['FULL PATH TO ATTACHMENTS HERE']
    attachments = [file]

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise


def make_and_email_pdf(travel: Travel):
    pdf = generate_pdf(travel)

    try:
        file = save_file(pdf, travel.trip_leader.name, str(travel.start_date))
        # send_mail([contact0, contact1], file)
    except:
        # delete_file(file)
        pass


def generate_pdf(travel: Travel) -> FPDF:
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
            travel.travelers.remove(leader_unit)
            other_units = travel.travelers
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
        pdf.cell(gar_width, gar_height, ' ', 1, 0)

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

    pdf.set_xy(gar_x, gar_y)
    pdf.add_cell(39, 'Average Team Member Totals', 'L', False, 1, 1, 'C', font_size=7)
    pdf.set_xy(gar_x, gar_y + pdf.height)
    if travel.gar_avg < 35:
        color = 100
    pdf.set_fill_color(color)
    pdf.add_cell(39, str(travel.gar_avg), 'V', False, 1, 0, 'C')
    pdf.set_xy(gar_x, gar_y + 2 * pdf.height + 1)
    pdf.add_cell(39, 'Mitigated GAR', 'L', False, 1, 0, 'C')
    pdf.set_xy(gar_x, gar_y + 3 * pdf.height + 1)
    pdf.add_cell(39, str(travel.mitigated_gar), 'V', False, 1, 0, 'C')

    pdf.cell(10, 2, '', ln=1)



    return pdf


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
    pdf.add_cell(width, str(unit.total_gar_score), 'V', False, 1, 1, 'C')


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
