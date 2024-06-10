# Dependency
from database import SessionLocal


def get_db():
    """Provide a database session for dependency injection.

    This generator function creates a new database session using `SessionLocal` and provides it to
    the caller. The session
    is yielded to the caller and closed after the request is completed, ensuring that the database
    connection is properly managed and released.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
