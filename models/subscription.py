from sqlalchemy import Column, String, ForeignKey
from ..models.base import BaseModel
from ..extensions import db
from flask_restful import fields

from .blueprint import blueprint_fields


class Subscription(db.Model, BaseModel):
    __tablename__ = 'subscriptions'

    email = Column(String(50), ForeignKey('users.email'))
    blueprint_id = Column(String(36), ForeignKey('blueprints.id'))

    blueprint = db.relationship('BluePrint', backref='subscriptions')


subscription_fields = {
    'id': fields.String,
    'email': fields.String,
    'blueprint_id': fields.String,
    'created': fields.String,
    'updated': fields.String
}

subscription_fields_with_blueprint = {
    'id': fields.String,
    'email': fields.String,
    'blueprint': fields.Nested(blueprint_fields),
    'created': fields.String,
    'updated': fields.String
}
