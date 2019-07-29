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

    file = save_file(pdf, name0, start_date)

    send_mail([contact0, contact1], file)

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

    cell_height = 6

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, cell_height, 'Start Date:', 1, 0, 'C')
    pdf.cell(55, cell_height, 'Entry Point:', 1, 0, 'C')
    pdf.cell(22, cell_height, 'End Date:', 1, 0, 'C')
    pdf.cell(55, cell_height, 'Exit Point:', 1, 0, 'C')
    pdf.cell(15, cell_height, 'Tracked:', 1, 0, 'C')
    pdf.cell(20, cell_height, 'PLB #:', 1, 1, 'C')

    pdf.set_font("Arial", '', size=10)
    pdf.cell(22, cell_height, start_date, 1, 0, 'L')
    pdf.cell(55, cell_height, entry_point, 1, 0, 'L')
    pdf.cell(22, cell_height, end_date, 1, 0, 'L')
    pdf.cell(55, cell_height, exit_point, 1, 0, 'L')
    pdf.cell(15, cell_height, 'Yes' if tracked else 'No', 1, 0, 'L')
    pdf.cell(20, cell_height, plb, 1, 1, 'L')

    pdf.cell(10, 2, '', ln=1)

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, cell_height, 'Trip Leader:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(55, cell_height, name0, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(30, cell_height, 'Radio Call Sign:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(47, cell_height, call_sign0, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(19, cell_height, 'Pack Color:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(16, cell_height, pack_color0, 1, 1, 'L')

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, cell_height, 'Name:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(55, cell_height, name1, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(30, cell_height, 'Radio Call Sign:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(47, cell_height, call_sign1, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(19, cell_height, 'Pack Color:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(16, cell_height, pack_color1, 1, 1, 'L')

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, cell_height, 'Name:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(55, cell_height, name2, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(30, cell_height, 'Radio Call Sign:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(47, cell_height, call_sign2, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(19, cell_height, 'Pack Color:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(16, cell_height, pack_color2, 1, 1, 'L')

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, cell_height, 'Name:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(55, cell_height, name3, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(30, cell_height, 'Radio Call Sign:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(47, cell_height, call_sign3, 1, 0, 'L')
    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(19, cell_height, 'Pack Color:', 1, 0, 'L')
    pdf.set_font("Arial", '', size=10)
    pdf.cell(16, cell_height, pack_color3, 1, 1, 'L')

    pdf.cell(10, 2, '', ln=1)

    pdf.set_font("Arial", 'B', size=8)
    pdf.cell(22, cell_height, 'Date:', 1, 0, 'C')
    pdf.cell(46, cell_height, 'Starting Point:', 1, 0, 'C')
    pdf.cell(46, cell_height, 'Ending Point:', 1, 0, 'C')
    pdf.cell(40, cell_height, 'Route:', 1, 0, 'C')
    pdf.cell(35, cell_height, 'Mode: (foot/stock/boat)', 1, 1, 'C')

    pdf.set_font("Arial", '', size=10)
    pdf.cell(22, cell_height, date0, 1, 0, 'L')
    pdf.cell(46, cell_height, start0, 1, 0, 'L')
    pdf.cell(46, cell_height, end0, 1, 0, 'L')
    pdf.cell(40, cell_height, route0, 1, 0, 'L')
    pdf.cell(35, cell_height, mode0, 1, 1, 'L')
    pdf.cell(22, cell_height, date1, 1, 0, 'L')
    pdf.cell(46, cell_height, start1, 1, 0, 'L')
    pdf.cell(46, cell_height, end1, 1, 0, 'L')
    pdf.cell(40, cell_height, route1, 1, 0, 'L')
    pdf.cell(35, cell_height, mode1, 1, 1, 'L')
    pdf.cell(22, cell_height, date2, 1, 0, 'L')
    pdf.cell(46, cell_height, start2, 1, 0, 'L')
    pdf.cell(46, cell_height, end2, 1, 0, 'L')
    pdf.cell(40, cell_height, route2, 1, 0, 'L')
    pdf.cell(35, cell_height, mode2, 1, 1, 'L')

    pdf.cell(10, 2, '', ln=1)

    return pdf
