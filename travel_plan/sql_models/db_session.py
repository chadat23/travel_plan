import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from travel_plan.sql_models.modelbase import SqlAlchemyBase

__factory_existing = None
__factory_patrol = None


def global_init_existing(db_existing: str):
    global __factory_existing

    if __factory_existing:
        return

    if not db_existing.strip():
        raise Exception("You must specify db files.")

    conn_str_existing = 'sqlite:///' + db_existing.strip()
    print("Connecting to Existing DB with {}".format(conn_str_existing))

    engine_existing = sa.create_engine(conn_str_existing, echo=False)
    __factory_existing = orm.sessionmaker(bind=engine_existing)

    # noinspection PyUnresolvedReferences
    import travel_plan.sql_models.__all_models_existing

    SqlAlchemyBase.metadata.create_all(engine_existing)


def global_init_patrol(db_patrol: str):
    global __factory_patrol

    if __factory_patrol:
        return

    if not db_patrol.strip():
        raise Exception("You must specify db files.")

    conn_str_patrol = 'sqlite:///' + db_patrol.strip()
    print("Connecting to Existing DB with {}".format(conn_str_patrol))

    engine_patrol = sa.create_engine(conn_str_patrol, echo=False)
    __factory_patrol = orm.sessionmaker(bind=engine_patrol)

    # noinspection PyUnresolvedReferences
    import travel_plan.sql_models.__all_models_patrol

    SqlAlchemyBase.metadata.create_all(engine_patrol)


def create_session_existing() -> Session:
    global __factory_existing

    session: Session = __factory_existing()

    session.expire_on_commit = False

    return session


def create_session_patrol() -> Session:
    global __factory_patrol

    session: Session = __factory_patrol()

    session.expire_on_commit = False

    return session
