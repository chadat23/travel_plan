import datetime

import sqlalchemy as sa

from travel_plan.sql_models.modelbase_existing import SqlAlchemyBaseExisting


class User(SqlAlchemyBaseExisting):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)

    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, index=True, unique=True, nullable=True)
