import sqlmodel
from .config import DATABASE_URL, DB_TIMEZONE
from sqlmodel import Session, SQLModel, create_engine
import timescaledb
from api.events.models import EventModel

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL is not set.")

# Normalize URL for SQLAlchemy compatibility
_db_url = DATABASE_URL
if _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif _db_url.startswith("postgresql://") and "+psycopg2" not in _db_url:
    _db_url = _db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

# Use sqlalchemy directly instead of timescaledb wrapper for engine creation
from sqlalchemy import create_engine as sa_create_engine
engine = sa_create_engine(_db_url)

def init_db():
    print("Initializing database connection...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created!")
    print("Creating Hypertables")
    timescaledb.metadata.create_all(engine)  # still use timescaledb for hypertables
    print("Hypertables created!")

def get_session():
    with Session(engine) as session:
        yield session