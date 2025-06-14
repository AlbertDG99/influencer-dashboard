from sqlmodel import create_engine, Session

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session():
    """
    Dependency to get a database session.
    """
    with Session(engine) as session:
        yield session 