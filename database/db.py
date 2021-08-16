# The database access here is based on the example in the SQL Alchemy documentation (SQL Alchemy 1.3 Documentation:
# Session Basics). As stated in the documentation, SQLAlchemy and its documentation are licensed under the MIT license.
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from models import Base
from config import DATABASE_URI

engine = create_engine(DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == '__main__':
    with session_scope() as session:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
