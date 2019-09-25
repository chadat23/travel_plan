from datetime import datetime

from travel_plan import db
from travel_plan.services import location_services


class TravelDay(db.Model):
    __tablename__ = 'travel_days'
    # TODO: needs work
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date = db.Column(db.DateTime, default=datetime.now, index=True)

    travel_id: int = db.Column(db.Integer, db.ForeignKey('travels.id'))

    date = db.Column(db.Date, nullable=False)
    starting_point_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    starting_point = db.relationship('Location', foreign_keys=[starting_point_id])
    ending_point_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    ending_point = db.relationship('Location', foreign_keys=[ending_point_id])
    route = db.Column(db.String, index=True)
    mode = db.Column(db.String, index=True)

    def __init__(self, date: str, starting_point: str, ending_point: str, route: str, mode: str):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.starting_point_id = location_services.get_id_from_name(starting_point)
        self.ending_point_id = location_services.get_id_from_name(ending_point)
        self.route = route
        self.mode = mode

    def __lt__(self, other):
        return self.date < other.date

    def __repr__(self):
        return f'{str(self.date)} {self.starting_point} {self.ending_point} {self.route} {self.mode}'
