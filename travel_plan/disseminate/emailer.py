from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
import shutil
import smtplib
import tempfile
from typing import List

from fpdf import FPDF


from travel_plan.disseminate.email_config import email


def save_file(pdf: FPDF, name0: str, start_date: str) -> str:
    name = name0.strip().replace(' ', '_') + '_' + start_date.replace('-', '') + '.pdf'
    # pdf.output(name)
    save_path = tempfile.mkdtemp()
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

    sender = email['address']
    gmail_password = email['password']
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


def email_pdf(start_date: str, entry_point: str, end_date: str, exit_point: str, tracked: str, plb: str,
              name0: str, call_sign0: str, pack_color0: str,
              name1: str, call_sign1: str, pack_color1: str,
              name2: str, call_sign2: str, pack_color2: str,
              name3: str, call_sign3: str, pack_color3: str,
              date0: str, start0: str, end0: str, route0: str, mode0: str,
              date1: str, start1: str, end1: str, route1: str, mode1: str,
              date2: str, start2: str, end2: str, route2: str, mode2: str,
              contact0: str, contact1: str,
              ):
    pdf = generate_pdf(start_date, entry_point, end_date, exit_point, tracked, plb,
                       name0, call_sign0, pack_color0,
                       name1, call_sign1, pack_color1,
                       name2, call_sign2, pack_color2,
                       name3, call_sign3, pack_color3,
                       date0, start0, end0, route0, mode0,
                       date1, start1, end1, route1, mode1,
                       date2, start2, end2, route2, mode2,
                       contact0, contact1, )

    try:
        file = save_file(pdf, name0, start_date)
        print('here')
        print('file', file)
        send_mail([contact0, contact1], file)
    except:
        delete_file(file)


def generate_pdf(start_date: str, entry_point: str, end_date: str, exit_point: str, tracked: str, plb: str,
                 name0: str, call_sign0: str, pack_color0: str,
                 name1: str, call_sign1: str, pack_color1: str,
                 name2: str, call_sign2: str, pack_color2: str,
                 name3: str, call_sign3: str, pack_color3: str,
                 date0: str, start0: str, end0: str, route0: str, mode0: str,
                 date1: str, start1: str, end1: str, route1: str, mode1: str,
                 date2: str, start2: str, end2: str, route2: str, mode2: str,
                 contact0: str, contact1: str,
                 ) -> FPDF:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    ht = 6

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, ht, 'Start Date:', 1, 0, 'C')
    pdf.cell(55, ht, 'Entry Point:', 1, 0, 'C')
    pdf.cell(22, ht, 'End Date:', 1, 0, 'C')
    pdf.cell(55, ht, 'Exit Point:', 1, 0, 'C')
    pdf.cell(15, ht, 'Tracked:', 1, 0, 'C')
    pdf.cell(20, ht, 'PLB #:', 1, 1, 'C')

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
    pdf.cell(55, ht, name0, 1, 0, 'L')
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
    pdf.cell(22, ht, 'Date:', 1, 0, 'C')
    pdf.cell(46, ht, 'Starting Point:', 1, 0, 'C')
    pdf.cell(46, ht, 'Ending Point:', 1, 0, 'C')
    pdf.cell(40, ht, 'Route:', 1, 0, 'C')
    pdf.cell(35, ht, 'Mode: (foot/stock/boat)', 1, 1, 'C')

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
