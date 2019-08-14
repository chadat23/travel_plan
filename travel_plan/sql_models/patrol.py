import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from travel_plan.sql_models.modelbase_patrol import SqlAlchemyBasePatrol


class Patrol(SqlAlchemyBasePatrol):
    __tablename__ = 'patrols'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.datetime.now, index=True)
    start_date = Column(DateTime, index=True, unique=False, nullable=False)
    entry_point = Column(String, index=True, unique=False, nullable=False)
    end_date = Column(DateTime, index=True, unique=False, nullable=False)
    exit_point = Column(String, index=True, unique=False, nullable=False)

    tracked = Column(Boolean, index=False, unique=False, nullable=True)
    plb = Column(String, index=False, unique=False, nullable=True)

    name0 = Column(String, index=False, unique=False, nullable=True)
    call_sign0 = Column(String, index=False, unique=False, nullable=True)
    pack_color0 = Column(String, index=False, unique=False, nullable=True)
    name1 = Column(String, index=False, unique=False, nullable=True)
    call_sign1 = Column(String, index=False, unique=False, nullable=True)
    pack_color1 = Column(String, index=False, unique=False, nullable=True)
    name2 = Column(String, index=False, unique=False, nullable=True)
    call_sign2 = Column(String, index=False, unique=False, nullable=True)
    pack_color2 = Column(String, index=False, unique=False, nullable=True)
    name3 = Column(String, index=False, unique=False, nullable=True)
    call_sign3 = Column(String, index=False, unique=False, nullable=True)
    pack_color3 = Column(String, index=False, unique=False, nullable=True)

    date0 = Column(DateTime, index=False, unique=False, nullable=True)
    start0 = Column(String, index=False, unique=False, nullable=True)
    end0 = Column(String, index=False, unique=False, nullable=True)
    route0 = Column(String, index=False, unique=False, nullable=True)
    mode0 = Column(String, index=False, unique=False, nullable=True)
    date1 = Column(DateTime, index=False, unique=False, nullable=True)
    start1 = Column(String, index=False, unique=False, nullable=True)
    end1 = Column(String, index=False, unique=False, nullable=True)
    route1 = Column(String, index=False, unique=False, nullable=True)
    mode1 = Column(String, index=False, unique=False, nullable=True)
    date2 = Column(DateTime, index=False, unique=False, nullable=True)
    start2 = Column(String, index=False, unique=False, nullable=True)
    end2 = Column(String, index=False, unique=False, nullable=True)
    route2 = Column(String, index=False, unique=False, nullable=True)
    mode2 = Column(String, index=False, unique=False, nullable=True)

    contact0 = Column(String, index=False, unique=False, nullable=True)
    contact1 = Column(String, index=False, unique=False, nullable=True)
