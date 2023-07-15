from sqlalchemy import Column, Integer
from models.base import BaseModel
from extensions import Base

class ScrapeSession(Base, BaseModel):
    __tablename__ = 'sessions'

    started = Column(Integer)
    ended = Column(Integer)
    new_cars = Column(Integer)
    
    def __init__(self):
        BaseModel.__init__(self)

    def __repr__(self):
        return f"<ScrapeSession(id={self.id}, started={self.started}, ended={self.ended}, new_cars={self.new_cars}, created={self.created}, updated={self.updated})>"