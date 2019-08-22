import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

from travel_plan.models.modelbase import SqlAlchemyBasePatrol


class Patrol(SqlAlchemyBasePatrol):
    __tablename__ = 'patrols'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, index=True)

    start_date = sa.Column(sa.Date, index=True, unique=False, nullable=False)
    entry_point_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    entry_point = orm.relationship('Location', foreign_keys=[entry_point_id])
    end_date = sa.Column(sa.Date, index=True, unique=False, nullable=False)
    exit_point_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))
    exit_point = orm.relationship('Location', foreign_keys=[exit_point_id])

    tracked = sa.Column(sa.Boolean, index=False, unique=False, nullable=True)
    plb = sa.Column(sa.String, index=False, unique=False, nullable=True)

    trip_leader_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    trip_leader = orm.relationship('User', foreign_keys=[trip_leader_id])

    patrollers = orm.relationship('PatrolUserUnit', backref='patrol')

    def __repr__(self):
        return f'{self.start_date} - {self.entry_point}, {self.entry_point} - {self.exit_point}'

    # name0 = Column(String, index=False, unique=False, nullable=True)
    # call_sign0 = Column(String, index=False, unique=False, nullable=True)
    # pack_color0 = Column(String, index=False, unique=False, nullable=True)
    # name1 = Column(String, index=False, unique=False, nullable=True)
    # call_sign1 = Column(String, index=False, unique=False, nullable=True)
    # pack_color1 = Column(String, index=False, unique=False, nullable=True)
    # name2 = Column(String, index=False, unique=False, nullable=True)
    # call_sign2 = Column(String, index=False, unique=False, nullable=True)
    # pack_color2 = Column(String, index=False, unique=False, nullable=True)
    # name3 = Column(String, index=False, unique=False, nullable=True)
    # call_sign3 = Column(String, index=False, unique=False, nullable=True)
    # pack_color3 = Column(String, index=False, unique=False, nullable=True)

    # date0 = Column(Date, index=False, unique=False, nullable=True)
    # start0 = Column(String, index=False, unique=False, nullable=True)
    # end0 = Column(String, index=False, unique=False, nullable=True)
    # route0 = Column(String, index=False, unique=False, nullable=True)
    # mode0 = Column(String, index=False, unique=False, nullable=True)
    # date1 = Column(Date, index=False, unique=False, nullable=True)
    # start1 = Column(String, index=False, unique=False, nullable=True)
    # end1 = Column(String, index=False, unique=False, nullable=True)
    # route1 = Column(String, index=False, unique=False, nullable=True)
    # mode1 = Column(String, index=False, unique=False, nullable=True)
    # date2 = Column(Date, index=False, unique=False, nullable=True)
    # start2 = Column(String, index=False, unique=False, nullable=True)
    # end2 = Column(String, index=False, unique=False, nullable=True)
    # route2 = Column(String, index=False, unique=False, nullable=True)
    # mode2 = Column(String, index=False, unique=False, nullable=True)
    #
    # contact0 = Column(String, index=False, unique=False, nullable=True)
    # contact1 = Column(String, index=False, unique=False, nullable=True)
