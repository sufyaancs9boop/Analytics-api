from pydantic import BaseModel, Field

class EventSchema(BaseModel):
    id: int = Field(..., description="Unique identifier for the event")