from flask import current_app

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
import smtplib
from typing import List

from travel_plan.models.travels import Travel


def email_files(travel: Travel, files: List[str], path: str):
    email_list = list(current_app.config['DEFAULT_EMAIL_LIST'])
    [email_list.append(e.traveler.email) for e in travel.travelers if hasattr(e.traveler, 'email')]
    [email_list.append(c.email) for c in travel.contacts if hasattr(c, 'email')]

    subject = _make_subject(travel)
    body = _make_body(travel)

    try:
        _send_mail(email_list, [os.path.join(path, file) for file in files], subject, body)
    except:
        # delete_file(file)
        pass

# def delete_file(file: str):
#     shutil.rmtree(os.path.abspath(os.path.join(file, os.pardir)))


def _send_mail(recipients: List[str], files: List[str], subject: str, body: str):
    COMMASPACE = ', '

    sender = current_app.config['EMAIL_ADDRESS']
    gmail_password = current_app.config['EMAIL_PASSWORD']
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


def _make_subject(travel: Travel) -> str:
    subject = 'Travel itinerary for : '
    print(subject)
    for traveler in travel.travelers:
        subject += traveler.call_sign + ', '

    return subject[:-2]


def _make_body(travel: Travel) -> str:
    body = "Here's the travel itinerary for "
    for traveler in travel.travelers:
        body += f"{traveler.traveler.name} ({traveler.call_sign}), "

    body = body[:-2] + '.'

    body += '\n Thanks'

    return body
