from sqlalchemy import Column, Integer, String, Boolean, DateTime
from ..models.base import BaseModel
from ..extensions import db
from datetime import datetime


class Brand(BaseModel, db.Model):
    __tablename__ = 'brands'

    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    display_name = Column(String(100))
    enabled = Column(Boolean, default=True, index=True)
    last_seen = Column(DateTime)

    # Relationship to models
    models = db.relationship('BrandModel', backref='brand', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, name, slug, display_name=None, enabled=True, last_seen=None):
        super().__init__()
        self.name = name
        self.slug = slug
        self.display_name = display_name or name
        self.enabled = enabled
        self.last_seen = last_seen or datetime.now()

    def to_dict(self, include_relationships=False):
        """Serialize brand to dictionary for API responses"""
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'display_name': self.display_name,
            'enabled': self.enabled,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'created': self.created.isoformat() if self.created else None,
            'updated': self.updated.isoformat() if self.updated else None
        }
        
        if include_relationships:
            data['models'] = [model.to_dict() for model in self.models]
        
        return data
