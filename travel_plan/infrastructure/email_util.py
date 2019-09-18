from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
import smtplib
from typing import List

from travel_plan.config import DEFAULT_EMAIL_LIST
from travel_plan.models.travels import Travel

try:
    from travel_plan.config import EMAIL_ADDRESS, EMAIL_PASSWORD
except:
    print('*' * 10 + ' Did you create a config.py file from the config_example.py file? ' + '*' * 10)


def email_files(travel: Travel, files: List[str], path: str):
    email_list = list(DEFAULT_EMAIL_LIST)
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

    sender = EMAIL_ADDRESS
    gmail_password = EMAIL_PASSWORD
    recipients = recipients

    # Create the enclosing (outer) message
    print(1)
    outer = MIMEMultipart()
    print(2)
    outer['Subject'] = subject
    print(3)
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    print(4)
    outer.attach(MIMEText(body, 'plain'))
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    # attachments = ['FULL PATH TO ATTACHMENTS HERE']
    attachments = files
    # Add the attachments to the message
    for file in attachments:
        try:
            print(str(file))
            with open(file, 'rb') as fp:
                print(6)
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            print(7)
            encoders.encode_base64(msg)
            print(8)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise
    print(9)
    composed = outer.as_string()

    print(20)
    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            print(21)
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
        print(subject)

    return subject[:-2]


def _make_body(travel: Travel) -> str:
    body = "Here's the travel itinerary for "
    for traveler in travel.travelers:
        body += f"{traveler.traveler.name} ({traveler.call_sign}), "

    body = body[:-2] + '.'

    body += '\n Thanks'

    return body
