import datetime

# from sqlalchemy import Boolean, Column, Date, Integer, String, ForeignKey
import sqlalchemy as sa
import sqlalchemy.orm as orm

from travel_plan.models.modelbase import SqlAlchemyBasePatrol
from travel_plan.models.patrol_units import PatrolUnit


class Patrol(SqlAlchemyBasePatrol):
    __tablename__ = 'patrols'

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, index=True)

    start_date = sa.Column(sa.Date, index=True, unique=False, nullable=False)
    entry_point = sa.Column(sa.String, sa.ForeignKey('locations.name'))
    end_date = sa.Column(sa.Date, index=True, unique=False, nullable=False)
    exit_point = sa.Column(sa.String, sa.ForeignKey('locations.name'))

    tracked = sa.Column(sa.Boolean, index=False, unique=False, nullable=True)
    plb = sa.Column(sa.String, index=False, unique=False, nullable=True)

    # patrol_units = orm.relation("PatrolUnit", order_by=PatrolUnit.user.desc(), back_populates=True)
    patrol_units = orm.relation("PatrolUnit", back_populates='patrol')

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
