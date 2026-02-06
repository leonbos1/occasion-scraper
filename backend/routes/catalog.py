from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.brand import Brand
from ..models.model import BrandModel
from ..scrapers import catalog_scraper
from ..routes.users import logged_in_required, admin_required
from ..utills.responses import success_response, error_response, ErrorCodes

catalog_bp = Blueprint('catalog', __name__, url_prefix='/api')


# Public Endpoints

@catalog_bp.route('/brands', methods=['GET'])
def get_brands():
    """Get all enabled brands for dropdowns"""
    try:
        brands = db.session.query(Brand).filter_by(enabled=True).order_by(Brand.display_name).all()
        
        result = [{
            'id': brand.id,
            'display_name': brand.display_name,
            'slug': brand.slug
        } for brand in brands]
        
        return success_response(result)
    except Exception as e:
        return error_response(ErrorCodes.INTERNAL_ERROR, str(e), 500)


@catalog_bp.route('/models', methods=['GET'])
def get_models():
    """Get all enabled models for a specific brand"""
    brand_slug = request.args.get('brand_slug')
    
    if not brand_slug:
        return error_response(ErrorCodes.INVALID_INPUT, "brand_slug parameter is required", 400)
    
    try:
        # Find the brand first
        brand = db.session.query(Brand).filter_by(slug=brand_slug).first()
        
        if not brand:
            return error_response(ErrorCodes.NOT_FOUND, f"Brand not found: {brand_slug}", 404)
        
        # Get enabled models for this brand (only if brand is also enabled)
        if not brand.enabled:
            return success_response([])
        
        models = db.session.query(BrandModel).filter_by(
            brand_id=brand.id,
            enabled=True
        ).order_by(BrandModel.display_name).all()
        
        result = [{
            'id': model.id,
            'display_name': model.display_name,
            'slug': model.slug
        } for model in models]
        
        return success_response(result)
    except Exception as e:
        return error_response(ErrorCodes.INTERNAL_ERROR, str(e), 500)


# Admin Endpoints

@catalog_bp.route('/admin/scrape-catalog', methods=['POST'])
@logged_in_required
@admin_required
def trigger_catalog_scrape(user):
    """Trigger the catalog scraper to discover brands and models"""
    try:
        summary = catalog_scraper.scrape_catalog()
        return success_response(summary)
    except Exception as e:
        return error_response(ErrorCodes.INTERNAL_ERROR, str(e), 500)


@catalog_bp.route('/admin/brands', methods=['GET'])
@logged_in_required
@admin_required
def get_admin_brands(user):
    """Get all brands (enabled and disabled) for admin management"""
    try:
        brands = db.session.query(Brand).order_by(Brand.display_name).all()
        
        result = [brand.to_dict() for brand in brands]
        
        return success_response(result)
    except Exception as e:
        return error_response(ErrorCodes.INTERNAL_ERROR, str(e), 500)


@catalog_bp.route('/admin/brands/<brand_id>', methods=['POST'])
@logged_in_required
@admin_required
def update_brand(user, brand_id):
    """Update brand display_name and/or enabled status"""
    data = request.get_json()
    
    if not data:
        return error_response(ErrorCodes.INVALID_INPUT, "Request body is required", 400)
    
    try:
        brand = db.session.query(Brand).filter_by(id=brand_id).first()
        
        if not brand:
            return error_response(ErrorCodes.NOT_FOUND, f"Brand not found: {brand_id}", 404)
        
        # Validate display_name if provided
        if 'display_name' in data:
            display_name = data['display_name']
            if not display_name or not display_name.strip():
                return error_response(ErrorCodes.INVALID_INPUT, "display_name cannot be empty", 400)
            brand.display_name = display_name.strip()
        
        # Validate enabled if provided
        if 'enabled' in data:
            enabled = data['enabled']
            if not isinstance(enabled, bool):
                return error_response(ErrorCodes.INVALID_INPUT, "enabled must be a boolean", 400)
            brand.enabled = enabled
        
        db.session.commit()
        
        return success_response(brand.to_dict())
    except Exception as e:
        db.session.rollback()
        return error_response(ErrorCodes.INTERNAL_ERROR, str(e), 500)


@catalog_bp.route('/admin/models', methods=['GET'])
@logged_in_required
@admin_required
def get_admin_models(user):
    """Get all models (enabled and disabled) for admin management"""
    brand_id = request.args.get('brand_id', type=int)
    
    try:
        query = db.session.query(BrandModel)
        
        if brand_id:
            query = query.filter_by(brand_id=brand_id)
        
        models = query.order_by(BrandModel.brand_id, BrandModel.display_name).all()
        
        result = [model.to_dict(include_brand=True) for model in models]
        
        return success_response(result)
    except Exception as e:
        return error_response(ErrorCodes.INTERNAL_ERROR, str(e), 500)


@catalog_bp.route('/admin/models/<model_id>', methods=['POST'])
@logged_in_required
@admin_required
def update_model(user, model_id):
    """Update model display_name and/or enabled status"""
    data = request.get_json()
    
    if not data:
        return error_response(ErrorCodes.INVALID_INPUT, "Request body is required", 400)
    
    try:
        model = db.session.query(BrandModel).filter_by(id=model_id).first()
        
        if not model:
            return error_response(ErrorCodes.NOT_FOUND, f"Model not found: {model_id}", 404)
        
        # Validate display_name if provided
        if 'display_name' in data:
            display_name = data['display_name']
            if not display_name or not display_name.strip():
                return error_response(ErrorCodes.INVALID_INPUT, "display_name cannot be empty", 400)
            model.display_name = display_name.strip()
        
        # Validate enabled if provided
        if 'enabled' in data:
            enabled = data['enabled']
            if not isinstance(enabled, bool):
                return error_response(ErrorCodes.INVALID_INPUT, "enabled must be a boolean", 400)
            model.enabled = enabled
        
        db.session.commit()
        
        return success_response(model.to_dict(include_brand=True))
    except Exception as e:
        db.session.rollback()
        return error_response(ErrorCodes.INTERNAL_ERROR, str(e), 500)
