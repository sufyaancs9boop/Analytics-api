import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select


from api.db.sessions import get_session
from .models import EventListSchema, EventModel, EventCreateSchema, EventUpdateSchema,get_utc_now
from api.db.config import DATABASE_URL  # will now get the correct value

router = APIRouter()
# GET /api/events/
@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_session)):
    print(DATABASE_URL)
    query = select(EventModel).limit(10)
    results = session.exec(query).all()
    return{
        "results": results,
        "count": len(results)
    }

#get data here
# GET /api/events/12   
@router.get("/{event_id}", response_model=EventModel)
def read_event(event_id: int, session: Session = Depends(get_session)):
    #a single row
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result

#post data here
#Create view
# POST /api/events
@router.post("/", response_model=EventModel)
def create_event(
    payload: EventCreateSchema, 
    session: Session = Depends(get_session)):
    data= payload.model_dump()
    obj= EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.put("/{event_id}", response_model=EventModel)
def update_event(event_id: int, payload: EventUpdateSchema, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    data = payload.model_dump()
    for key, value in data.items():
            setattr(obj, key, value)
    obj.updated_at = get_utc_now()  # Update the timestamp
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj