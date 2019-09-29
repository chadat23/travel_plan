import datetime

from travel_plan import db


class Department(db.Model):
    '''
    An object representing a component of an orginization's structure.

    Typically used to represent which portion of an orginizaiton
    that an employee works for or a piece of equipment belongs to.

    :param id: the database key
    :type id: int
    :param created_date: the date on which the Department is added
    to the database
    :type created_date: datetime
    :param name: the name of the department
    :type name: str
    '''

    __tablename__ = 'departments'

    id: int = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    name: str = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, name: str):
        '''
        Initializes a Department object

        :param name: the name of the department
        :type name: str
        '''
        self.name = name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f'{self.name}'
