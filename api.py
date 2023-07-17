from fastapi import FastAPI
from extensions import Base, url, get_session
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models.car import Car
import datetime
import uvicorn
from endpoints import router as endpoints_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(endpoints_router)

origins = [
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "X-API-Key"],
)