from flask import Blueprint, jsonify, request
from flask_restful import abort, marshal_with, marshal
from sqlalchemy import func, inspect, and_

from ..extensions import db
from ..middleware import remove_disallowed_properties
from ..utills.responses import success_response, error_response, not_found_error, validation_error, ErrorCodes

from ..models.car import Car, car_fields

from time import sleep

cars = Blueprint("cars", __name__)


@cars.route("", methods=["GET"])
def get_cars():
    """Get all cars (without base_image for performance)"""
    try:
        columns = [c_attr for c_attr in inspect(
            Car).attrs if c_attr.key != 'base_image']

        cars_query = Car.query.with_entities(*columns).all()

        print(f"{len(cars_query)} cars fetched from db")

        cars_list = [car._asdict() for car in cars_query]
        
        # Convert datetime objects to strings
        for car in cars_list:
            if car.get('created'):
                car['created'] = str(car['created']).split('.')[0]
            if car.get('updated'):
                car['updated'] = str(car['updated']).split('.')[0]

        return success_response(cars_list)
    except Exception as e:
        print(f"Error fetching cars: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch cars", 500)


@cars.route("/filters", methods=["GET"])
def get_filters():
    """Get available filter fields"""
    filters = [
        "brand",
        "model",
        "min_first_registration",
        "max_first_registration",
        "min_mileage",
        "max_mileage",
        "min_price",
        "max_price"
    ]

    return success_response(filters)


@cars.route("/<int:page_number>/<int:per_page>", methods=["POST"])
def get_cars_page(page_number, per_page):
    """Get paginated cars with filtering and sorting"""
    try:
        request_json = request.json

        order_by = request_json.get("order_by", "created")
        order_direction = request_json.get("order_direction", "desc")
        filters = request_json.get("filters", {})

        # Validate order_by field
        if not hasattr(Car, order_by):
            return validation_error(f"Invalid order_by field: {order_by}")

        query = Car.query

        for filter_name, filter_value in filters.items():
            print(filter_name, filter_value)
            if filter_value is not None:
                if type(filter_value) == str and len(filter_value) == 0:
                    continue
                if filter_name.startswith("min_"):
                    actual_filter = filter_name[4:]
                    if hasattr(Car, actual_filter):
                        query = query.filter(
                            getattr(Car, actual_filter) >= filter_value)
                elif filter_name.startswith("max_"):
                    actual_filter = filter_name[4:]
                    if hasattr(Car, actual_filter):
                        query = query.filter(
                            getattr(Car, actual_filter) <= filter_value)
                elif hasattr(Car, filter_name):
                    query = query.filter(getattr(Car, filter_name).like(f"%{filter_value}%"))

        query = query.order_by(getattr(Car, order_by).desc(
        ) if order_direction == "desc" else getattr(Car, order_by))
        page = query.paginate(page=page_number, per_page=per_page)

        cars_list = []
        for car in page.items:
            car_dict = marshal(car, car_fields)
            # Convert datetime to string
            car_dict['created'] = str(car.created).split('.')[0]
            car_dict['updated'] = str(car.updated).split('.')[0]
            cars_list.append(car_dict)

        print(f"{len(cars_list)} cars fetched from db")
        
        return success_response(cars_list, metadata={
            "page": page_number,
            "per_page": per_page,
            "total": page.total,
            "pages": page.pages
        })
    except Exception as e:
        print(f"Error fetching car page: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch cars", 500)


@cars.route("/max_page/<int:per_page>", methods=["GET"])
def get_max_page(per_page):
    """Get maximum page number for pagination"""
    try:
        max_page = Car.query.paginate(per_page=per_page).pages
        return success_response({"max_page": max_page})
    except Exception as e:
        print(f"Error getting max page: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to calculate pages", 500)


@cars.route("/<string:id>", methods=["GET"])
def get_car(id):
    """Get a single car by ID"""
    car = Car.query.filter_by(id=id).first()

    if not car:
        return not_found_error("Car not found")
    
    car_dict = marshal(car, car_fields)
    car_dict['created'] = str(car.created).split('.')[0]
    car_dict['updated'] = str(car.updated).split('.')[0]

    return success_response(car_dict)


@cars.route("/recent/<int:count>", methods=["GET"])
def get_recent_cars(count):
    """Get most recently created cars"""
    try:
        cars = Car.query.order_by(Car.created.desc()).limit(count).all()
        cars_list = []
        for car in cars:
            car_dict = marshal(car, car_fields)
            car_dict['created'] = str(car.created).split('.')[0]
            car_dict['updated'] = str(car.updated).split('.')[0]
            cars_list.append(car_dict)
        return success_response(cars_list)
    except Exception as e:
        print(f"Error fetching recent cars: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch recent cars", 500)

@cars.route("/expensive/<int:count>", methods=["GET"])
def get_expensive_cars(count):
    """Get most expensive cars"""
    try:
        cars = Car.query.order_by(Car.price.desc()).limit(count).all()
        cars_list = []
        for car in cars:
            car_dict = marshal(car, car_fields)
            car_dict['created'] = str(car.created).split('.')[0]
            car_dict['updated'] = str(car.updated).split('.')[0]
            cars_list.append(car_dict)
        return success_response(cars_list)
    except Exception as e:
        print(f"Error fetching expensive cars: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch expensive cars", 500)


@cars.route("/image/<string:id>", methods=["GET"])
def get_car_image(id):
    """Get car image (returns raw image bytes, not envelope)"""
    car = Car.query.filter_by(id=id).first()

    if car is None:
        return not_found_error("Car not found")

    # Return raw image bytes for browser display
    return car.base_image


@cars.route("/<id>/images", methods=["GET"])
def get_car_images(id):
    """Get all images for a specific car"""
    from ..models.car_image import CarImage
    
    car = Car.query.filter_by(id=id).first()
    if car is None:
        return not_found_error("Car not found")
    
    images = CarImage.query.filter_by(car_id=id).order_by(CarImage.order).all()
    
    images_list = [{
        'id': img.id,
        'image_data': img.image_data,
        'order': img.order
    } for img in images]
    
    return success_response(images_list)


@cars.route("/", methods=["POST"])
@remove_disallowed_properties()
def create_car():
    """Create a new car"""
    try:
        request_json = request._cached_json

        # Validate required fields
        if not request_json:
            return validation_error("Request body is required")

        car = Car(**request_json)

        db.session.add(car)
        db.session.commit()
        
        car_dict = marshal(car, car_fields)
        car_dict['created'] = str(car.created).split('.')[0]
        car_dict['updated'] = str(car.updated).split('.')[0]

        return success_response(car_dict)
    except TypeError as e:
        return validation_error(f"Invalid car data: {str(e)}")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating car: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to create car", 500)


@cars.route("/<string:id>", methods=["PUT"])
@remove_disallowed_properties()
def update_car(id):
    """Update an existing car"""
    try:
        car = Car.query.filter_by(id=id).first()

        if not car:
            return not_found_error("Car not found")

        request_json = request._cached_json
        
        if not request_json:
            return validation_error("Request body is required")

        car_properties = vars(car)

        for prop in request_json:
            if prop in car_properties:
                setattr(car, prop, request_json[prop])

        db.session.commit()
        
        car_dict = marshal(car, car_fields)
        car_dict['created'] = str(car.created).split('.')[0]
        car_dict['updated'] = str(car.updated).split('.')[0]

        return success_response(car_dict)
    except Exception as e:
        db.session.rollback()
        print(f"Error updating car: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to update car", 500)


@cars.route("/brands", methods=["GET"])
def get_brands():
    """Get all brands with car counts"""
    try:
        brands = db.session.query(Car.brand, func.count(
            Car.brand)).group_by(Car.brand).all()

        return success_response({brand: count for brand, count in brands})
    except Exception as e:
        print(f"Error fetching brands: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch brands", 500)


@cars.route("/models", methods=["GET"])
def get_models():
    """Get all models with car counts"""
    try:
        models = db.session.query(Car.model, func.count(
            Car.model)).group_by(Car.model).all()

        return success_response({model: count for model, count in models})
    except Exception as e:
        print(f"Error fetching models: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch models", 500)

@cars.route("/count", methods=["GET"])
def get_car_count():
    """Get total car count"""
    try:
        car_count = Car.query.count()
        return success_response({"count": car_count})
    except Exception as e:
        print(f"Error counting cars: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to count cars", 500)

@cars.route("/brands_and_models", methods=["GET"])
def get_brands_and_models():
    """
    Returns an object with brands as keys and a list of models as values
    """
    try:
        brands_and_models = db.session.query(Car.brand, Car.model).all()

        brands = {}

        for brand, model in brands_and_models:
            if brand not in brands:
                brands[brand] = []
            if model not in brands[brand]:
                brands[brand].append(model)

        return success_response(brands)
    except Exception as e:
        print(f"Error fetching brands and models: {e}")
        return error_response(ErrorCodes.DATABASE_ERROR, "Failed to fetch brands and models", 500)
