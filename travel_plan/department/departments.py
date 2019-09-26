import datetime

from travel_plan import db


class Department(db.Model):
    __tablename__ = 'departments'

    id: int = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    name: str = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f'{self.name}'
