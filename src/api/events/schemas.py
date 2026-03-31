from pydantic import BaseModel, Field
from typing import List

class EventSchema(BaseModel):
    id: int = Field(..., description="Unique identifier for the event")
    
class EventListSchema(BaseModel):
    results: list[EventSchema]