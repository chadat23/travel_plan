import datetime

from travel_plan import db


class Note(db.Model):
    """
    A note for a Car
    
    :param created_date: when the note was created
    :type created_date: datetime
    :param text: the body of the note
    :type text: str
    :param car_id: the id of the car that the note's to be added to
    :type car_id: int
    """
    __tablename__ = 'notes'

    id: int = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    text: str = db.Column(db.String, unique=True, nullable=False)
    car_id: int = db.Column(db.Integer, db.ForeignKey('cars.id'))

    def __init__(self, text: str):
        """Initiates a Note object with a text body"""
        self.text = text

    def __lt__(self, other):
        return str(self) < str(other)

    def __repr__(self):
        return f'{self.text}'
