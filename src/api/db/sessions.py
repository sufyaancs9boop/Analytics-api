import sqlmodel
from .config import DATABASE_URL, DB_TIMEZONE
from sqlmodel import Session, SQLModel, create_engine
import timescaledb
from api.events.models import EventModel  # ← import so metadata registers the table

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL is not set.")

engine = timescaledb.create_engine(DATABASE_URL, timezone=DB_TIMEZONE)

def init_db():
    print("Initializing database connection...")
    SQLModel.metadata.create_all(engine)  # ← no yield, just a regular function
    print("Database tables created!")
    print("Creatinng Hypertables")
    timescaledb.metadata.create_all(engine)  # ← create hypertables after regular tables
    print("Hypertables created!")
    
def get_session():
    with Session(engine) as session:
        yield session  # ← yield is correct here, it's a dependency