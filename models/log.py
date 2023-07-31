from sqlalchemy import Column, Integer, String, ForeignKey, BLOB
from ..models.base import BaseModel
from ..extensions import db
from sqlalchemy.dialects.mysql import LONGTEXT
from flask_restful import fields


class Log(BaseModel, db.Model):
    __tablename__ = 'logs'

    message = Column(String(1000))
    level = Column(String(50))
    session_id = Column(String(36))#, ForeignKey('sessions.id'))

    def __init__(self, message, level, session_id):
        self.message = message
        self.level = level
        self.session_id = session_id
        BaseModel.__init__(self)

    def __repr__(self):
        return f"<Log(id={self.id}, message={self.message}, level={self.level}, session_id={self.session_id}, created={self.created}, updated={self.updated})>"
    
log_fields = {
    'id': fields.String,
    'message': fields.String,
    'level': fields.String,
    'session_id': fields.String,
    'created': fields.Integer,
    'updated': fields.Integer
}