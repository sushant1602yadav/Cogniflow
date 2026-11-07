
"""
Cogniflow Database Configuration

Creates the database connection and manages sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database location
DATABASE_URL = "sqlite:///./cogniflow.db"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for database models
Base = declarative_base()


def get_db():
    """
    Provides a database session.

    The session is automatically closed
    after the operation is complete.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
