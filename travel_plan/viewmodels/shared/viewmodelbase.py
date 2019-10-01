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
        return self.__dict__

    def convert_empty_strings_to_none(self):
        """
        Converts all of the empty strings to None.

        This is done so that the underlying database ends up with
        None rather than '' in places where no value was entered.
        :return: None
        """
        for attr, value in self.__dict__.items():
            if isinstance(value, str):
                if value == '':
                    self.__dict__[attr] = None
