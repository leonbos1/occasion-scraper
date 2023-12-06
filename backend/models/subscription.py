from sqlalchemy import Column, String, ForeignKey
from ..models.base import BaseModel
from ..extensions import db
from flask_restful import fields

from .blueprint import blueprint_fields
from .user import user_fields


class Subscription(db.Model, BaseModel):
    __tablename__ = 'subscriptions'

    user_id = Column(String(36), ForeignKey('users.id'))
    blueprint_id = Column(String(36), ForeignKey('blueprints.id'))

    blueprint = db.relationship('BluePrint', backref='subscriptions')
    user = db.relationship('User', backref='subscriptions')


subscription_fields = {
    'id': fields.String,
    'user': fields.Nested(user_fields),
    'blueprint': fields.Nested(blueprint_fields),
    'created': fields.String,
    'updated': fields.String
}