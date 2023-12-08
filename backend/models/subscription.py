from sqlalchemy import Column, String, ForeignKey
from ..models.base import BaseModel
from ..extensions import db
from flask_restful import fields

from .user import user_fields


class Subscription(db.Model, BaseModel):
    __tablename__ = 'subscriptions'

    user_id = Column(String(36), ForeignKey('users.id'))
    blueprint_id = Column(String(36), ForeignKey('blueprints.id'))

    user = db.relationship('User', backref='subscriptions')


subscription_fields = {
    'id': fields.String,
    'user': fields.Nested(user_fields),
    'created': fields.String,
    'updated': fields.String
}