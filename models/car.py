from sqlalchemy import Column, Integer, String, ForeignKey, BLOB
from ..models.base import BaseModel
from ..extensions import db
import base64
from sqlalchemy.dialects.mysql import LONGTEXT
from flask_restful import fields


class Car(BaseModel, db.Model):
    __tablename__ = 'cars'

    brand = Column(String(50))
    model = Column(String(50))
    price = Column(Integer)
    mileage = Column(Integer)
    first_registration = Column(Integer)
    vehicle_type = Column(String(50))
    location = Column(String(450))
    condition = Column(String(50))
    url = Column(String(1000))
    base_image = Column(LONGTEXT)
    session_id = Column(String(36), ForeignKey('sessions.id'))

    def __init__(self, id, brand, model, price, mileage, first_registration, vehicle_type, location, condition, url, session_id, image):
        self.brand = brand
        self.model = model
        self.price = price
        self.mileage = mileage
        self.first_registration = first_registration
        self.vehicle_type = vehicle_type
        self.location = location
        self.condition = condition
        self.url = url
        self.base_image = "data:image/jpeg;base64," + \
            base64.b64encode(image).decode("utf-8")
        self.session_id = session_id

        BaseModel.__init__(self, id)

    def __repr__(self):
        return f"<Car(id={self.id}, brand={self.brand}, model={self.model}, price={self.price}, mileage={self.mileage}, first_registration={self.first_registration}, vehicle_type={self.vehicle_type}, location={self.location}, condition={self.condition}, url={self.url}, session_id={self.session_id}, created={self.created}, updated={self.updated})>"


car_fields = {
    'id': fields.String,
    'brand': fields.String,
    'model': fields.String,
    'price': fields.String,
    'mileage': fields.Integer,
    'first_registration': fields.Integer,
    'vehicle_type': fields.String,
    'location': fields.String,
    'condition': fields.String,
    'url': fields.String,
    'base_image': fields.String,
    'session_id': fields.String,
    'created': fields.Integer,
    'updated': fields.Integer
}
