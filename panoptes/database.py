import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

# The DB URL is overridable via PANOPTES_DB_URL so tests (and deployments that
# want to relocate the SQLite file) can point at an isolated path without
# patching the source.
_DB_URL = os.environ.get(
    "PANOPTES_DB_URL", "sqlite:///.panoptes.db?check_same_thread=False"
)
engine = create_engine(_DB_URL)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)
