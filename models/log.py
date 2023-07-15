from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from models.base import BaseModel
from extensions import Base

class Log(Base, BaseModel):
    __tablename__ = 'logs'

    message = Column(String(1000))
    level = Column(String(50))
    session_id = Column(String(36), ForeignKey('sessions.id'))

    def __init__(self, message, level, session_id):
        self.message = message
        self.level = level
        self.session_id = session_id
        BaseModel.__init__(self)

    def __repr__(self):
        return f"<Log(id={self.id}, message={self.message}, level={self.level}, session_id={self.session_id}, created={self.created}, updated={self.updated})>"