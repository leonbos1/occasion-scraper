from sqlalchemy import Column, String, Integer
import uuid
import time
import datetime

class BaseModel:
    id = Column(String(36), primary_key=True)
    created = Column(Integer)
    updated = Column(Integer)

    def __init__(self, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.created = datetime.datetime.now()
        self.updated = datetime.datetime.now()