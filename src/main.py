from dotenv import load_dotenv
load_dotenv()
import logging
from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.events.routing import router as event_router
from api.db.sessions import init_db




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform any startup tasks here
    init_db()
    print("Starting up the application...")
    yield
    # Perform any shutdown tasks here
    print("Shutting down the application...")
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(event_router, prefix= '/api/events')

logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/healthz")
def read_api_health():
    return {"message": "OK"}