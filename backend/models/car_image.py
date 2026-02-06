from sqlalchemy import Column, Integer, String, ForeignKey, Text
from ..models.base import BaseModel
from ..extensions import db
from flask_restful import fields


class CarImage(BaseModel, db.Model):
    __tablename__ = 'car_images'

    car_id = Column(String(36), ForeignKey('cars.id'))
    image_data = Column(Text)  # Base64 encoded image data
    order = Column(Integer)  # Order of the image (0 = first/primary)

    def __init__(self, car_id=None, image_data=None, order=0):
        BaseModel.__init__(self)
        self.car_id = car_id
        self.image_data = image_data
        self.order = order


car_image_fields = {
    'id': fields.String,
    'car_id': fields.String,
    'image_url': fields.String,
    'order': fields.Integer,
    'created': fields.String,
    'updated': fields.String
}
