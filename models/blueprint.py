from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import BaseModel
from extensions import Base

class BluePrint(Base, BaseModel):
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
    owner_id = Column(String(36), ForeignKey('users.id'))

    def __init__(self, brand, model, min_price, max_price, min_mileage, max_mileage, min_first_registration, max_first_registration, vehicle_type, city, max_distance_from_home, owner_id):
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
        self.owner_id = owner_id
        BaseModel.__init__(self)

    def __repr__(self):
        return f"<BluePrint(id={self.id}, brand={self.brand}, model={self.model}, min_price={self.min_price}, max_price={self.max_price}, min_mileage={self.min_mileage}, max_mileage={self.max_mileage}, min_first_registration={self.min_first_registration}, max_first_registration={self.max_first_registration}, vehicle_type={self.vehicle_type}, owner_id={self.owner_id}, created={self.created}, updated={self.updated})>"
  