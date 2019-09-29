import sqlalchemy as sa

from travel_plan import db


class Color(db.Model):
    '''
    An object respresenting an items color.

    :prop id: the database key
    :prop name: the name of the color
    '''

    __tablename__ = 'colors'

    id: str = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String, nullable=False)

    def __init__(self, name: str):
        '''
        Initialize a color object.

        All colors are to have "title" capitalization.
        (This Is An Example Of Title Capitalization)

        :prop name: the name of the color
        :type name: str
        '''
        self.name = name.lower().strip().title()

    def __lt__(self, other):
        return self.name < other.name
