from fastapi import APIRouter
from .schemas import EventListSchema, EventSchema
router = APIRouter()

@router.get("/")
def read_events()-> EventListSchema:
    return EventListSchema(
        results=[EventSchema(id=1), EventSchema(id=2), EventSchema(id=3)],
        count=3
    )
    
#get data here
@router.get("/{event_id}")
def read_event(event_id: int) -> EventSchema:
    return EventSchema(id=event_id)

#post data here
@router.post("/")
def create_event(data: dict = {}) -> EventSchema:
    print(data)
    return EventSchema(id=123)
