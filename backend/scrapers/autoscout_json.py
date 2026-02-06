"""
AutoScout24 JSON API Scraper
Uses the NextJS data API for faster and more reliable scraping
"""
from time import sleep
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..utills import mail, logger
from ..extensions import db
from ..models.car import Car
from ..models.car_image import CarImage
from ..models.scrape_session import ScrapeSession
from ..models.blueprint import BluePrint
from ..models.subscription import Subscription
from ..utills.database import get_new_cars, save_cars_to_db, save_session_to_db
import datetime
import base64

# AutoScout24 JSON API endpoint
JSON_API_BASE = 'https://www.autoscout24.nl/_next/data/as24-search-funnel_main-20260130135042'
IMAGE_DOWNLOAD_WORKERS = 6
MAX_IMAGES_PER_CAR = None


def slugify(value: str):
    return '-'.join(value.lower().strip().replace('&', 'and').split())


def build_list_path(blueprint: BluePrint):
    if blueprint.brand and blueprint.model:
        return f"/lst/{slugify(blueprint.brand)}/{slugify(blueprint.model)}.json"
    if blueprint.brand:
        return f"/lst/{slugify(blueprint.brand)}.json"
    return "/lst.json"


def get_json_api_url(blueprint: BluePrint):
    return f"{JSON_API_BASE}{build_list_path(blueprint)}"


def start():
    """Start scraping all blueprints"""
    global _logger
    
    blueprints = db.session.query(BluePrint).all()
    
    for blueprint in blueprints:
        scrape_blueprint(blueprint)


def scrape_blueprint(blueprint: BluePrint):
    """Scrape cars for a specific blueprint"""
    global _logger
    
    scrape_session = ScrapeSession()
    _logger = logger.Logger(scrape_session.id)
    _logger.log_info(f"Scrape session started for autoscout with blueprint: {blueprint.name}")
    
    save_session_to_db(scrape_session, _logger)
    
    try:
        all_new_cars = []
        
        # Scrape multiple pages
        for page in range(1, 21):  # Max 20 pages
            cars = scrape_page_json(blueprint, page, scrape_session)
            
            if not cars:
                _logger.log_info(f"No more cars found at page {page}")
                break
            
            new_cars = get_new_cars(cars)
            all_new_cars.extend(new_cars)
            
            save_cars_to_db(new_cars, _logger)
            scrape_session.ended = datetime.datetime.now()
            scrape_session.new_cars = len(all_new_cars)
            save_session_to_db(scrape_session, _logger)
            
            sleep(1)  # Be nice to the server
        
        # Send email notifications
        try:
            emails = get_emails(blueprint)
            if emails and all_new_cars:
                mail.send_email(all_new_cars, emails, blueprint.name)
                _logger.log_info("Email sent")
        except Exception as e:
            _logger.log_error(f"Could not send email: {str(e)}")
        
        _logger.log_info(f"Scrape session ended. Total new cars: {len(all_new_cars)}")
        
    except Exception as e:
        # Truncate error message to avoid DB issues
        error_msg = f"Error while scraping autoscout: {str(e)}"[:500]
        _logger.log_error(error_msg)
        print(e)


def scrape_page_json(blueprint: BluePrint, page: int, scrape_session: ScrapeSession):
    """Scrape a single page using the JSON API"""
    params = build_query_params(blueprint, page)
    url = get_json_api_url(blueprint)
    
    try:
        _logger.log_info(f"Fetching page {page} with url: {url} params: {params}")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            _logger.log_error(f"HTTP {response.status_code} error")
            return []
        
        data = response.json()
        listings = data.get('pageProps', {}).get('listings', [])
        
        if not listings:
            return []
        
        cars = []
        for listing in listings:
            try:
                car = extract_car_from_listing(listing, scrape_session)
                if car:
                    cars.append(car)
            except Exception as e:
                car_id = listing.get('id', 'unknown')
                # Truncate error message to avoid DB issues
                error_msg = f"Error extracting car {car_id}: {str(e)}"[:500]
                _logger.log_error(error_msg)
        
        _logger.log_info(f"Successfully scraped {len(cars)} cars from page {page}")
        return cars
        
    except Exception as e:
        # Truncate error message to avoid DB issues
        error_msg = f"Error fetching page {page}: {str(e)}"[:500]
        _logger.log_error(error_msg)
        return []


def build_query_params(blueprint: BluePrint, page: int):
    """Build query parameters from blueprint"""
    params = {
        'cy': 'NL',
        'atype': 'C',
        'ustate': 'N,U',
        'page': page,
        'sort': 'standard',
        'desc': 0
    }
    
    # Price range
    if blueprint.min_price and blueprint.min_price > 0:
        params['pricefrom'] = blueprint.min_price
    if blueprint.max_price and blueprint.max_price > 0:
        params['priceto'] = blueprint.max_price
    
    # Mileage
    if blueprint.max_mileage and blueprint.max_mileage > 0:
        params['kmto'] = blueprint.max_mileage
    
    # First registration year
    if blueprint.max_first_registration and blueprint.max_first_registration > 0:
        params['fregto'] = blueprint.max_first_registration
    
    # Location
    if blueprint.city and blueprint.max_distance_from_home and blueprint.max_distance_from_home > 0:
        params['zip'] = blueprint.city
        params['zipr'] = blueprint.max_distance_from_home
    
    return params


def extract_car_from_listing(listing: dict, scrape_session: ScrapeSession):
    """Extract car information from JSON listing"""
    try:
        # Extract basic info
        car_id = listing.get('id')
        if not car_id:
            return None
        
        # Check if car already exists
        existing_car = Car.query.filter_by(id=car_id).first()
        if existing_car:
            _logger.log_info(f"Car {car_id} already exists, skipping")
            return None
        
        vehicle = listing.get('vehicle', {})
        location = listing.get('location', {})
        price_info = listing.get('price', {})
        tracking = listing.get('tracking', {})
        seller = listing.get('seller', {})
        vehicle_details = listing.get('vehicleDetails', [])
        
        # Extract fields
        brand = vehicle.get('make', 'Unknown')
        model = vehicle.get('model', 'Unknown')
        
        # Parse price (remove currency symbols and convert to int)
        price_str = price_info.get('priceFormatted', '0')
        try:
            price = int(''.join(filter(str.isdigit, price_str)))
        except:
            price = 0
        
        # Parse mileage
        mileage_str = vehicle.get('mileageInKm', '0')
        try:
            mileage = int(''.join(filter(str.isdigit, mileage_str)))
        except:
            mileage = 0
        
        # Parse first registration (format: "03/2020")
        first_reg_str = tracking.get('firstRegistration', '2010')
        try:
            if '/' in first_reg_str or '-' in first_reg_str:
                parts = first_reg_str.replace('-', '/').split('/')
                first_registration = int(parts[-1])  # Get year
            else:
                first_registration = int(first_reg_str)
        except:
            first_registration = 2010
        
        # Vehicle type
        vehicle_type = vehicle.get('type', 'Car')

        # Fuel & transmission
        fuel = vehicle.get('fuel')
        transmission = vehicle.get('transmission')

        # Variant / model version
        variant = vehicle.get('modelVersionInput') or vehicle.get('variant')

        # Seller name
        seller_name = seller.get('companyName')

        # Power (kW/HP)
        power_kw, power_hp = extract_power(vehicle_details, tracking)
        
        # Location
        city = location.get('city', 'Unknown')
        country = location.get('countryCode', 'NL')
        loc_str = f"{city}, {country}"
        
        # URL
        url_path = listing.get('url', '')
        url = f"https://www.autoscout24.nl{url_path}"
        
        # Get all images
        image_urls = listing.get('images', [])
        if MAX_IMAGES_PER_CAR:
            image_urls = image_urls[:MAX_IMAGES_PER_CAR]

        # Download images concurrently
        image_data_list = download_images_base64(image_urls)

        # Use first available image for backward compatibility
        first_image_data = next((img for img in image_data_list if img), None)
        
        # Create car object
        car = Car(
            id=car_id,
            brand=brand,
            model=model,
            price=price,
            mileage=mileage,
            first_registration=first_registration,
            vehicle_type=vehicle_type,
            location=loc_str,
            fuel=fuel,
            transmission=transmission,
            power_kw=power_kw,
            power_hp=power_hp,
            variant=variant,
            seller_name=seller_name,
            condition='Used' if vehicle.get('offerType') == 'U' else 'New',
            url=url,
            session_id=scrape_session.id,
            image=None
        )
        
        # Set base_image for backward compatibility
        if first_image_data:
            car.base_image = first_image_data
        
        # Save car first so we can link images to it
        db.session.add(car)
        db.session.flush()  # Get the car ID without committing
        
        # Create CarImage entries for all images
        for idx, image_data in enumerate(image_data_list):
            if not image_data:
                continue
            car_image = CarImage(
                car_id=car.id,
                image_data=image_data,
                order=idx
            )
            db.session.add(car_image)
        
        return car
        
    except Exception as e:
        # Truncate error message to avoid DB issues
        error_msg = f"Failed to extract car: {str(e)}"[:500]
        _logger.log_error(error_msg)
        db.session.rollback()
        return None


def download_images_base64(image_urls):
    if not image_urls:
        return []

    def download_one(url):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return base64.b64encode(response.content).decode('utf-8')
        except Exception as e:
            error_msg = f"Error downloading image: {str(e)}"[:500]
            _logger.log_error(error_msg)
        return None

    results = [None] * len(image_urls)
    with ThreadPoolExecutor(max_workers=IMAGE_DOWNLOAD_WORKERS) as executor:
        future_map = {
            executor.submit(download_one, url): idx
            for idx, url in enumerate(image_urls)
        }
        for future in as_completed(future_map):
            idx = future_map[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                error_msg = f"Error downloading image: {str(e)}"[:500]
                _logger.log_error(error_msg)
    return results


def extract_power(vehicle_details, tracking):
    """Extract power in kW and HP from vehicleDetails or tracking."""
    power_kw = None
    power_hp = None

    try:
        for detail in vehicle_details:
            data = detail.get('data', '')
            if 'kW' in data and 'PK' in data:
                # Example: "110 kW (150 PK)"
                parts = data.replace(')', '').split('(')
                kw_part = parts[0].strip().split(' ')[0]
                hp_part = parts[1].strip().split(' ')[0] if len(parts) > 1 else None
                power_kw = int(''.join(filter(str.isdigit, kw_part))) if kw_part else power_kw
                power_hp = int(''.join(filter(str.isdigit, hp_part))) if hp_part else power_hp
                break
    except Exception:
        pass

    # Fallbacks from tracking if present
    if power_kw is None:
        try:
            power_kw = int(tracking.get('powerKw')) if tracking.get('powerKw') else None
        except Exception:
            power_kw = None
    if power_hp is None:
        try:
            power_hp = int(tracking.get('powerHp')) if tracking.get('powerHp') else None
        except Exception:
            power_hp = None

    return power_kw, power_hp


def get_emails(blueprint: BluePrint):
    """Get email addresses for blueprint subscribers"""
    subscriptions = db.session.query(Subscription).filter_by(
        blueprint_id=blueprint.id).all()
    
    return [sub.user.email for sub in subscriptions]
