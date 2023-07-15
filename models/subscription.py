from sqlalchemy import Column, String, ForeignKey
from models.base import BaseModel
from extensions import Base

class Subscription(Base, BaseModel):
    __tablename__ = 'subscriptions'

    email = Column(String(50), ForeignKey('users.email'))
    blueprint_id = Column(String(36), ForeignKey('blueprints.id'))