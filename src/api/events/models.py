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
    page: str = Field(index=True) # /about, /contact, # pricing
    user_agent: Optional[str] = Field(default="", index=True) # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True) 
    session_id: Optional[str] = Field(default=None, index=True)
    duration: Optional[int] = Field(default=0) 

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"
 
    #created_at: datetime = Field(
        #default_factory=get_utc_now,
        #sa_type=sqlmodel.DateTime,  # ← no space, no type annotation here
        
        #description="Timestamp when the event was created",
        #nullable=False
    #)

    #updated_at: datetime = Field(
        #default_factory=get_utc_now,
        #sa_type=sqlmodel.DateTime,  # ← no space, no type annotation here
        #description="Timestamp when the event was created",
        #nullable=False
    #)
 
    
    
class EventCreateSchema(SQLModel):
    page: str
    user_agent: Optional[str] = Field(default="", index=True) # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True) 
    session_id: Optional[str] = Field(default=None, index=True)
    duration: Optional[int] = Field(default=0)

#class EventUpdateSchema(SQLModel):  
    #description: str
    

class EventListSchema(SQLModel):
    results: list[EventModel]
    
class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    ua: Optional[str] = ""
    operating_system: Optional[str] = ""
    avg_duration: Optional[float] = 0.0
    count: int