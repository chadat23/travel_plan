import sqlalchemy.ext.declarative.base as sqlalchemybase
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from travel_plan.sql_models.modelbase import SqlAlchemyBaseExternal, SqlAlchemyBasePatrol

__factory_external = None
__factory_patrol = None


def global_init(db_external: str, db_patrol: str = ''):
    global __factory_external, __factory_patrol

    if not __factory_external and db_external != '':
        __initiate_base('external', db_external, SqlAlchemyBaseExternal)

    if not __factory_patrol and db_patrol != '':
        __initiate_base('patrol', db_patrol, SqlAlchemyBasePatrol)


def __initiate_base(factory: str, db_name: str, sql_alchemy_base: sqlalchemybase):
    global __factory_external, __factory_patrol

    if not db_name.strip():
        raise Exception("You must specify db files.")

    conn_str = 'sqlite:///' + db_name.strip()
    print("Connecting to Existing DB with {}".format(conn_str))

    engine = sa.create_engine(conn_str, echo=False)
    if factory == 'external':
        __factory_external = orm.sessionmaker(bind=engine)
    elif factory == 'patrol':
        __factory_patrol = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import travel_plan.sql_models.__all_models

    sql_alchemy_base.metadata.create_all(engine)


def create_session_external() -> Session:
    global __factory_external

    session: Session = __factory_external()

    session.expire_on_commit = False

    return session


def create_session_patrol() -> Session:
    global __factory_patrol

    session: Session = __factory_patrol()

    session.expire_on_commit = False

    return session
