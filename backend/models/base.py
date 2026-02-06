from sqlalchemy import Column, String, Integer, DateTime
import uuid
import time
import datetime

class BaseModel:
    id = Column(String(36), primary_key=True)
    created = Column(DateTime)
    updated = Column(DateTime)

    def __init__(self, id=None):
        self.id = id if id else str(uuid.uuid4())
        now = datetime.datetime.now().replace(microsecond=0)
        self.created = now
        self.updated = now