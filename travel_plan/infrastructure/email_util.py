import os
from typing import List

from flask import current_app
from flask_mail import Message

from travel_plan import mail
from travel_plan.travel.travels import Travel


def email_travel(email_list: str, files: List[str], path: str):

    subject = _make_subject(travel)
    body = _make_body(travel)

    try:
        _send_mail(email_list, [os.path.join(path, file) for file in files], subject, body)
    except Exception as e:
        pass


def _send_mail(recipients: List[str], files: List[str], subject: str, body: str):
    msg = Message(subject=subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=recipients,
                  body=body)
    for file in files:
        with current_app.open_resource(file) as fp:
            name = os.path.basename(file)
            msg.attach(name, 'text/plain', fp.read())
    mail.send(msg)
    print('Email Sent')


def _make_subject(travel: Travel) -> str:
    subject = 'Travel itinerary for : '
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
