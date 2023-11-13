from sqlalchemy import Column, String, ForeignKey
from ..models.base import BaseModel
from ..extensions import db
from flask_restful import fields

class Subscription(db.Model, BaseModel):
    __tablename__ = 'subscriptions'

    email = Column(String(50), ForeignKey('users.email'))
    blueprint_id = Column(String(36), ForeignKey('blueprints.id'))

subscription_fields = {
    'id': fields.String,
    'email': fields.String,
    'blueprint_id': fields.String,
    'created': fields.String,
    'updated': fields.String
}