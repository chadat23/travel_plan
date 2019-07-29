import datetime

import sqlalchemy as sa

from travel_plan.sql_models.modelbase import SqlAlchemyBase


class Patrol(SqlAlchemyBase):
    __tablename__ = 'patrols'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    start_date = sa.Column(sa.DateTime, index=True, unique=False, nullable=False)
    entry_point = sa.Column(sa.String, index=True, unique=False, nullable=False)
    end_date = sa.Column(sa.DateTime, index=True, unique=False, nullable=False)
    exit_point = sa.Column(sa.String, index=True, unique=False, nullable=False)

    tracked = sa.Column(sa.Boolean, index=False, unique=False, nullable=True)
    plb = sa.Column(sa.String, index=False, unique=False, nullable=True)

    name0 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    call_sign0 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    pack_color0 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    name1 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    call_sign1 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    pack_color1 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    name2 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    call_sign2 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    pack_color2 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    name3 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    call_sign3 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    pack_color3 = sa.Column(sa.String, index=False, unique=False, nullable=True)

    date0 = sa.Column(sa.DateTime, index=False, unique=False, nullable=True)
    start0 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    end0 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    route0 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    mode0 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    date1 = sa.Column(sa.DateTime, index=False, unique=False, nullable=True)
    start1 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    end1 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    route1 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    mode1 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    date2 = sa.Column(sa.DateTime, index=False, unique=False, nullable=True)
    start2 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    end2 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    route2 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    mode2 = sa.Column(sa.String, index=False, unique=False, nullable=True)

    contact0 = sa.Column(sa.String, index=False, unique=False, nullable=True)
    contact1 = sa.Column(sa.String, index=False, unique=False, nullable=True)
