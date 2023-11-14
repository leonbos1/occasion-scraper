from sqlalchemy import Column, Integer, String
from ..models.base import BaseModel
from ..extensions import db
from flask_restful import fields

class ScrapeSession(db.Model, BaseModel):
    __tablename__ = 'sessions'

    started = Column(Integer)
    ended = Column(String)
    new_cars = Column(Integer)
    
    def __init__(self):
        BaseModel.__init__(self)

    def __repr__(self):
        return f"<ScrapeSession(id={self.id}, started={self.started}, ended={self.ended}, new_cars={self.new_cars}, created={self.created}, updated={self.updated})>"
    
scrape_session_fields = {
    'id': fields.String,
    'started': fields.Integer,
    'ended': fields.String,
    'new_cars': fields.Integer,
    'created': fields.String,
    'updated': fields.String
}