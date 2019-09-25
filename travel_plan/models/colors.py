import sqlalchemy as sa

from travel_plan import db


class Color(db.Model):
    __tablename__ = 'colors'

    id: str = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String, nullable=False)

    def __init__(self, name: str):
        self.name = name.lower().strip().title()

    def __lt__(self, other):
        return self.name < other.name
