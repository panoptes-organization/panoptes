from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from panoptes.db_properties import db_conf_init
# sqlite://<nohostname>/<path>

database, nohostname, path, sqlite_thread = db_conf_init()
print(database+ '://' +nohostname+ '/' +path+ '' +sqlite_thread+ '')
engine = create_engine( database+ '://' +nohostname+ '/' +path+ '' +sqlite_thread+ '', convert_unicode=True)
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
