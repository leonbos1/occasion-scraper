from sqlalchemy import Column, Integer, String, ForeignKey
from ..models.base import BaseModel

from ..extensions import db

from flask_restful import fields


class BluePrint(BaseModel, db.Model):
    __tablename__ = 'blueprints'

    brand = Column(String(50))
    model = Column(String(50))
    min_price = Column(Integer)
    max_price = Column(Integer)
    min_mileage = Column(Integer)
    max_mileage = Column(Integer)
    min_first_registration = Column(Integer)
    max_first_registration = Column(Integer)
    vehicle_type = Column(String(50))
    city = Column(String(50))
    max_distance_from_home = Column(Integer)
    name = Column(String(50))
    owner_id = Column(String(36), ForeignKey('users.id'))

    def __init__(self, brand=None, model=None, min_price=None, max_price=None, min_mileage=None, max_mileage=None, min_first_registration=None, max_first_registration=None, vehicle_type=None, city=None, max_distance_from_home=None, name=None, owner_id=None):
        self.brand = brand
        self.model = model
        self.min_price = min_price
        self.max_price = max_price
        self.min_mileage = min_mileage
        self.max_mileage = max_mileage
        self.min_first_registration = min_first_registration
        self.max_first_registration = max_first_registration
        self.vehicle_type = vehicle_type
        self.city = city
        self.max_distance_from_home = max_distance_from_home
        self.name = name
        self.owner_id = owner_id
        BaseModel.__init__(self)

    def __repr__(self):
        return f"<BluePrint(id={self.id}, brand={self.brand}, model={self.model}, min_price={self.min_price}, max_price={self.max_price}, min_mileage={self.min_mileage}, max_mileage={self.max_mileage}, min_first_registration={self.min_first_registration}, max_first_registration={self.max_first_registration}, vehicle_type={self.vehicle_type}, owner_id={self.owner_id}, created={self.created}, updated={self.updated})>"


blueprint_fields = {
    'id': fields.String,
    'brand': fields.String,
    'model': fields.String,
    'min_price': fields.Integer,
    'max_price': fields.Integer,
    'min_mileage': fields.Integer,
    'max_mileage': fields.Integer,
    'min_first_registration': fields.Integer,
    'max_first_registration': fields.Integer,
    'vehicle_type': fields.String,
    'city': fields.String,
    'max_distance_from_home': fields.Integer,
    'name': fields.String,
    'owner_id': fields.String,
    'created': fields.String,
    'updated': fields.String
}
