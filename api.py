from fastapi import FastAPI
from extensions import Base, url, get_session
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models.car import Car
import datetime
import uvicorn
from endpoints import router as endpoints_router

app = FastAPI()
app.include_router(endpoints_router)