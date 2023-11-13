from sqlalchemy import Column, Integer, String, ForeignKey
from ..models.base import BaseModel
from ..extensions import db
from sqlalchemy.orm import relationship

from flask_restful import fields


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    email = Column(String(50), unique=True)
    password = Column(String(50))

    def __init__(self, email, password):
        self.email = email
        self.password = password
        BaseModel.__init__(self)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, password={self.password}, created={self.created}, updated={self.updated})>"

user_fields = {
    'id': fields.String,
    'email': fields.String,
    'password': fields.String,
    'created': fields.String,
    'updated': fields.String
}