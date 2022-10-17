from sqlalchemy import create_engine, func, Table, MetaData, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class Connection():
    """
    pg_engine = create_engine('postgresql://postgres:DEPgroep1@vichogent.be:40032')
    pg_conn = pg_engine.connect()
    metadata = MetaData(pg_engine)

    Base = declarative_base(pg_engine)
    Base.metadata.reflect(pg_engine)

    __engine__ = pg_engine
    __conn__ = pg_conn
    __Base__ = Base
    """
    pass