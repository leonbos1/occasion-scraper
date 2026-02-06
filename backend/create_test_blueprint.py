import datetime
import sys
sys.path.insert(0, 'E:/GitHub/occasion-scraper/backend')

from extensions import session, db
from models.blueprint import BluePrint

# Create a test blueprint for Alfa Romeo
bp = BluePrint(
    name='Test Alfa Romeo',
    brand='Alfa Romeo',
    model=None,
    min_price=0,
    max_price=50000,
    max_mileage=150000,
    max_first_registration=None,
    city=None,
    max_distance_from_home=None,
    created=datetime.datetime.now(),
    updated=datetime.datetime.now()
)

session.add(bp)
session.commit()

print(f'Created blueprint: {bp.name} (ID: {bp.id})')
print(f'Brand: {bp.brand}')
print(f'Price range: €{bp.min_price} - €{bp.max_price}')
print(f'Max mileage: {bp.max_mileage} km')
