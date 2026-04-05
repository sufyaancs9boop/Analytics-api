#from pydantic import BaseModel, Field
from typing import List, Optional
import sqlmodel
from sqlmodel import SQLModel, Field
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now
from datetime import datetime, timezone
"""
id
path
description
"""

#def get_utc_now():
    #return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

# pagevisits we want to track at any given time
class EventModel(TimescaleModel, table=True):
    
    #id: int | None = Field(default=None, description="Unique identifier for the event", primary_key=True)
    page: str = Field(index=True)
    description: Optional[str] = ""
    #created_at: datetime = Field(
        #default_factory=get_utc_now,
        #sa_type=sqlmodel.DateTime,  # ← no space, no type annotation here
        
        #description="Timestamp when the event was created",
        #nullable=False
    #)

    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime,  # ← no space, no type annotation here
        description="Timestamp when the event was created",
        nullable=False
    )
    __chunk_time_interval__= "INTERVAL '1 day'"
    __drop_after__ = "INTERVAL '3 months'"
    
    
class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")

class EventUpdateSchema(SQLModel):  
    description: str
    

class EventListSchema(SQLModel):
    results: list[EventModel]