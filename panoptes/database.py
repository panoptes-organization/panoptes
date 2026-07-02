import os

from sqlalchemy import create_engine, inspect, text
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
    _migrate()


def _migrate(target_engine=None):
    # create_all() only creates missing tables; it never alters existing ones.
    # Databases created by older panoptes versions therefore need any columns
    # added since to be bolted on here.
    target_engine = target_engine if target_engine is not None else engine
    inspector = inspect(target_engine)
    if 'workflows' in inspector.get_table_names():
        columns = {c['name'] for c in inspector.get_columns('workflows')}
        if 'updated_at' not in columns:
            with target_engine.begin() as conn:
                conn.execute(text('ALTER TABLE workflows ADD COLUMN updated_at DATETIME'))
