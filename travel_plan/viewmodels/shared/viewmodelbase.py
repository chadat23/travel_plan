from typing import Optional

import flask
from flask import Request

from travel_plan.infrastructure import request_dict


class ViewModelBase:
    def __init__(self):
        self.request: Request = flask.request
        self.request_dict = request_dict.create('')

        self.error: Optional[str] = None

    def to_dict(self):
        print(self.__dict__)
        return self.__dict__
