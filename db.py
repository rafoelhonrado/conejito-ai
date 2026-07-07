"""
db.py

Database configuration.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///finance.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_session():
    return SessionLocal()


def create_database():
    # Import models here so SQLAlchemy registers them before create_all()
    import models  # noqa: F401

    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_database()
    print("finance.db created successfully.")