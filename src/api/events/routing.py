import os
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, col
from timescaledb.hyperfunctions import time_bucket
from typing import List, Optional
from sqlalchemy import func, case, String
from datetime import datetime, timedelta, timezone
from .models import EventListSchema, EventModel, EventCreateSchema,EventBucketSchema,get_utc_now

from api.db.sessions import get_session
from api.db.config import DATABASE_URL  # will now get the correct value

router = APIRouter()

DEFAULT_LOOKUP_PAGES = [
        "/", "/about", "/pricing", "/contact", 
        "/blog", "/products", "/login", "/signup",
        "/dashboard", "/settings"
    ]
# GET /api/events/
@router.get("/", response_model=List[EventBucketSchema])
def read_events(
        duration: str = Query(default="1 day"),
        pages: List = Query(default=None),
        session: Session = Depends(get_session)
    ):
    # a bunch of items in a table
    os_case = case(
    (col(EventModel.user_agent).ilike('%windows%'), 'Windows'),
    (col(EventModel.user_agent).ilike('%macintosh%'), 'MacOS'),
    (col(EventModel.user_agent).ilike('%iphone%'), 'iOS'),
    (col(EventModel.user_agent).ilike('%android%'), 'Android'),
    (col(EventModel.user_agent).ilike('%linux%'), 'Linux'),
    else_='Other'
    ).label('operating_system')
    

    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    query = (
        select( #type: ignore
            bucket.label('bucket'),
            os_case,
            col(EventModel.page).label('page'),
            func.avg(EventModel.duration).label("avg_duration"),
            func.count().label('count')
        )
        .where(
            col(EventModel.page).in_(lookup_pages)
        )
        .group_by(
            bucket,
            os_case,
            col(EventModel.page),
        )
        .order_by(
            bucket,
            os_case,
            col(EventModel.page),
        )
    )
    results = session.exec(query).fetchall()
    return results

    

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


#@router.put("/{event_id}", response_model=EventModel)
#def update_event(event_id: int, payload: EventUpdateSchema, session: Session = Depends(get_session)):
    #query = select(EventModel).where(EventModel.id == event_id)
    #obj = session.exec(query).first()
   #if not obj:
        #raise HTTPException(status_code=404, detail="Event not found")
    #data = payload.model_dump()
    #for key, value in data.items():
            #setattr(obj, key, value)
    #obj.updated_at = get_utc_now()  # Update the timestamp
    #session.add(obj)
    #session.commit()
    #session.refresh(obj)
    #return obj