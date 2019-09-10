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
    _traveler(pdf, 'Trip Leader:', leader_unit)

    for unit in other_units:
        _traveler(pdf, 'Name:', unit)

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

    # y = pdf.get_y()
    # pdf.cell(20, ht, 'hello', 1, 0, 'L')
    # pdf.cell(20, ht, 'hello', 1, 0, 'L')
    # pdf.cell(20, ht, 'hello', 1, 1, 'L')
    # pdf.cell(20, ht, 'hello', 1, 0, 'L')
    # pdf.cell(20, ht, 'hello', 1, 0, 'L')
    # pdf.cell(20, ht, 'hello', 1, 1, 'L')
    # pdf.cell(20, ht, 'hello', 1, 0, 'L')
    # pdf.cell(20, ht, 'hello', 1, 0, 'L')
    # pdf.cell(20, ht, 'hello', 1, 0, 'L')
    # x = pdf.get_x()
    # pdf.set_xy(x, y)
    # pdf.cell(20, 18, 'hello', 1, 1, 'L')

    return pdf


def _traveler(pdf: PDF, label: str, unit):
    pdf.add_cell(22, label, 'L', False, 1, 0, 'L')
    pdf.add_cell(55, unit.traveler.name, 'V', False, 1, 0, 'L')
    pdf.add_cell(30, 'Radio Call Sign:', 'L', False, 1, 0, 'L')
    pdf.add_cell(47, unit.call_sign, 'V', False, 1, 0, 'L')
    pdf.add_cell(19, 'Pack Color:', 'L', False, 1, 0, 'L')
    pdf.add_cell(16, unit.pack_color, 'V', False, 1, 1, 'L')


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
