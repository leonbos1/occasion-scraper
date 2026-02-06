"""
Brand/Model Catalog Builder
Extracts brands and models from existing cars in the database
"""
from datetime import datetime
from sqlalchemy import func
from ..extensions import db
from ..models.brand import Brand
from ..models.model import BrandModel
from ..models.car import Car


def _log(message, level="INFO"):
    """Simple logging function for catalog builder"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {message}")


def extract_brands_from_cars():
    """
    Extract unique brands from cars table
    Returns: List of dicts with 'name' and 'slug' keys
    """
    _log("Extracting brands from cars table...")
    
    try:
        # Query distinct brands from cars, excluding NULL and empty strings
        brands_data = db.session.query(
            Car.brand,
            func.count(Car.id).label('car_count')
        ).filter(
            Car.brand.isnot(None),
            Car.brand != ''
        ).group_by(Car.brand).all()
        
        brands = []
        for brand_name, car_count in brands_data:
            # Clean up brand name
            brand_name = brand_name.strip()
            if not brand_name:
                continue
                
            # Create slug (lowercase, replace spaces with hyphens)
            slug = brand_name.lower().replace(' ', '-').replace('_', '-')
            
            brands.append({
                'name': brand_name,
                'slug': slug,
                'car_count': car_count
            })
        
        _log(f"Extracted {len(brands)} unique brands from cars")
        return brands
        
    except Exception as e:
        _log(f"Failed to extract brands: {e}", "ERROR")
        return []


def extract_models_for_brand(brand_name):
    """
    Extract unique models for a specific brand from cars table
    Args: brand_name (str): Brand name as stored in cars table
    Returns: List of dicts with 'name' and 'slug' keys
    """
    _log(f"Extracting models for brand: {brand_name}")
    
    try:
        # Query distinct models for this brand
        models_data = db.session.query(
            Car.model,
            func.count(Car.id).label('car_count')
        ).filter(
            Car.brand == brand_name,
            Car.model.isnot(None),
            Car.model != ''
        ).group_by(Car.model).all()
        
        models = []
        for model_name, car_count in models_data:
            # Clean up model name
            model_name = model_name.strip()
            if not model_name:
                continue
                
            # Create slug (lowercase, replace spaces with hyphens)
            slug = model_name.lower().replace(' ', '-').replace('_', '-')
            
            models.append({
                'name': model_name,
                'slug': slug,
                'car_count': car_count
            })
        
        _log(f"Extracted {len(models)} unique models for {brand_name}")
        return models
        
    except Exception as e:
        _log(f"Failed to extract models for {brand_name}: {e}", "ERROR")
        return []


def upsert_brand(brand_data):
    """
    Insert or update a brand in the database
    Args: brand_data (dict): Dict with 'name' and 'slug' keys
    Returns: (brand_id, was_new) tuple
    """
    try:
        # Check if brand already exists
        existing_brand = db.session.query(Brand).filter_by(slug=brand_data['slug']).first()
        
        if existing_brand:
            # Update last_seen timestamp
            existing_brand.last_seen = datetime.now()
            db.session.commit()
            return existing_brand.id, False
        else:
            # Insert new brand
            new_brand = Brand(
                name=brand_data['name'],
                slug=brand_data['slug'],
                display_name=brand_data['name'],  # Use name as display_name initially
                enabled=True,
                last_seen=datetime.now()
            )
            db.session.add(new_brand)
            db.session.commit()
            
            _log(f"Inserted new brand: {brand_data['name']} ({brand_data['slug']})")
            return new_brand.id, True
            
    except Exception as e:
        db.session.rollback()
        _log(f"Failed to upsert brand {brand_data['slug']}: {e}", "ERROR")
        return None, False


def upsert_model(model_data, brand_id):
    """
    Insert or update a model in the database
    Args:
        model_data (dict): Dict with 'name' and 'slug' keys
        brand_id (str): UUID of the brand
    Returns: (model_id, was_new) tuple
    """
    try:
        # Check if model already exists for this brand
        existing_model = db.session.query(BrandModel).filter_by(
            brand_id=brand_id,
            slug=model_data['slug']
        ).first()
        
        if existing_model:
            # Update last_seen timestamp
            existing_model.last_seen = datetime.now()
            db.session.commit()
            return existing_model.id, False
        else:
            # Insert new model
            new_model = BrandModel(
                brand_id=brand_id,
                name=model_data['name'],
                slug=model_data['slug'],
                display_name=model_data['name'],  # Use name as display_name initially
                enabled=True,
                last_seen=datetime.now()
            )
            db.session.add(new_model)
            db.session.commit()
            
            _log(f"Inserted new model: {model_data['name']} ({model_data['slug']}) for brand {brand_id}")
            return new_model.id, True
            
    except Exception as e:
        db.session.rollback()
        _log(f"Failed to upsert model {model_data['slug']} for brand {brand_id}: {e}", "ERROR")
        return None, False


def scrape_catalog():
    """
    Main catalog extraction function
    Extracts brands and models from cars table and updates catalog
    Returns: Summary dict with counts
    """
    summary = {'brands_added': 0, 'brands_updated': 0, 'brands_failed': 0,
               'models_added': 0, 'models_updated': 0, 'models_failed': 0}
    
    _log("Starting catalog extraction from cars table...")
    
    # Extract brands from cars
    brands = extract_brands_from_cars()
    
    if not brands:
        _log("No brands found in cars table.", "WARNING")
        return summary
    
    _log(f"Processing {len(brands)} brands...")
    
    # Process each brand
    for brand_data in brands:
        try:
            # Upsert brand
            brand_id, is_new = upsert_brand(brand_data)
            
            if brand_id is None:
                summary['brands_failed'] += 1
                continue
            
            if is_new:
                summary['brands_added'] += 1
            else:
                summary['brands_updated'] += 1
            
            # Extract models for this brand
            models = extract_models_for_brand(brand_data['name'])
            
            if not models:
                _log(f"No models found for {brand_data['name']}", "WARNING")
                continue
            
            _log(f"Processing {len(models)} models for {brand_data['name']}...")
            
            # Upsert each model
            for model_data in models:
                try:
                    model_id, is_new = upsert_model(model_data, brand_id)
                    
                    if model_id is None:
                        summary['models_failed'] += 1
                        continue
                    
                    if is_new:
                        summary['models_added'] += 1
                    else:
                        summary['models_updated'] += 1
                        
                except Exception as e:
                    _log(f"Error processing model {model_data['slug']}: {e}", "ERROR")
                    summary['models_failed'] += 1
            
        except Exception as e:
            _log(f"Error processing brand {brand_data['slug']}: {e}", "ERROR")
            summary['brands_failed'] += 1
    
    _log(f"Catalog extraction complete. Summary: {summary}")
    return summary
