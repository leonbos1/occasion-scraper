from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from ..models.base import BaseModel
from ..extensions import db
from datetime import datetime


class BrandModel(BaseModel, db.Model):
    __tablename__ = 'models'

    brand_id = Column(String(36), ForeignKey('brands.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    display_name = Column(String(100))
    enabled = Column(Boolean, default=True, index=True)
    last_seen = Column(DateTime)

    # Unique constraint on brand_id + slug
    __table_args__ = (
        db.UniqueConstraint('brand_id', 'slug', name='unique_brand_model'),
    )

    def __init__(self, brand_id, name, slug, display_name=None, enabled=True, last_seen=None):
        super().__init__()
        self.brand_id = brand_id
        self.name = name
        self.slug = slug
        self.display_name = display_name or name
        self.enabled = enabled
        self.last_seen = last_seen or datetime.now()

    def to_dict(self, include_brand=False):
        """Serialize model to dictionary for API responses"""
        data = {
            'id': self.id,
            'brand_id': self.brand_id,
            'name': self.name,
            'slug': self.slug,
            'display_name': self.display_name,
            'enabled': self.enabled,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'created': self.created.isoformat() if self.created else None,
            'updated': self.updated.isoformat() if self.updated else None
        }
        
        if include_brand and self.brand:
            data['brand_name'] = self.brand.display_name
        
        return data
