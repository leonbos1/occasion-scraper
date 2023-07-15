from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import BaseModel
from extensions import Base
from sqlalchemy.orm import relationship

class User(Base, BaseModel):
    __tablename__ = 'users'

    email = Column(String(50), unique=True)
    password = Column(String(50))
    blueprints = relationship("BluePrint", backref="user")

    def __init__(self, email, password):
        self.email = email
        self.password = password
        BaseModel.__init__(self)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, password={self.password}, created={self.created}, updated={self.updated})>"
