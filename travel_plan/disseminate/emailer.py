from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
import shutil
import smtplib
from typing import List

from travel_plan.disseminate.pdf_generater import generate_pdf
from travel_plan.config import PDF_FOLDER_PATH, DEFAULT_EMAIL_LIST
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
    print('saving')
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


def send_mail(recipients: List[str], files: List[str], subject: str, body: str):
    COMMASPACE = ', '

    sender = EMAIL_ADDRESS
    gmail_password = EMAIL_PASSWORD
    recipients = recipients

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.attach(MIMEText(body, 'plain'))
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    # attachments = ['FULL PATH TO ATTACHMENTS HERE']
    attachments = files
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


def make_and_email_pdf(travel: Travel, files: List[str]):
    pdf = generate_pdf(travel)
    email_list = list(DEFAULT_EMAIL_LIST)
    [email_list.append(e.traveler.email) for e in travel.travelers if hasattr(e.traveler, 'email')]
    [email_list.append(c.email) for c in travel.contacts if hasattr(c, 'email')]

    try:
        # file =
        files.append(save_file(pdf, travel.trip_leader.name, str(travel.start_date)))
        subject = _make_subject(travel)
        body = _make_body(travel)
        send_mail(email_list, files, subject, body)
    except:
        # delete_file(file)
        pass


def _make_subject(travel: Travel) -> str:
    subject = 'Travel itinarary for : '
    print(subject)
    for traveler in travel.travelers:
        subject += traveler.call_sign + ', '
        print(subject)

    return subject[:-2]


def _make_body(travel: Travel) -> str:
    body = "Here's the travel itinarary for "
    for traveler in travel.travelers:
        body += f"{traveler.traveler.name} ({traveler.call_sign}), "

    body = body[:-2] + '.'

    body += '\n Thanks'

    return body
