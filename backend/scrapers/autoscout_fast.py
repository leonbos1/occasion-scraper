from time import sleep
import requests
import os
from sqlalchemy.orm import Session
from ..utills import mail, logger
from ..extensions import session
from ..models.car import Car
from ..models.scrape_session import ScrapeSession
from ..models.blueprint import BluePrint
from ..models.subscription import Subscription
from ..utills.database import get_new_cars, save_cars_to_db, save_session_to_db
import datetime
from bs4 import BeautifulSoup

BASE_URL = 'https://www.autoscout24.nl/'


def debug(text):
    with open("./log.txt", "a") as f:
        f.write(text + "\n")


def start():
    global _logger

    cars = []

    sleep(0.5)

    blueprints = session.query(BluePrint).all()

    for blueprint in blueprints:
        scrape_blueprint(cars, blueprint)


def scrape_blueprint(cars: list, blueprint: BluePrint):
    global _logger

    url = BASE_URL + "lst"

    scrape_session = ScrapeSession()

    _logger = logger.Logger(scrape_session.id)
    _logger.log_info(
        "Scrape session started for autoscout with blueprint: " + blueprint.name)

    save_session_to_db(scrape_session, _logger)

    try:

        if blueprint.brand != None:
            url += f"/{blueprint.brand}"

        if blueprint.model != None:
            url += f"/{blueprint.model}"

        url += "?cy=NL"

        url += f"&pricefrom={blueprint.min_price}"

        if blueprint.max_price and blueprint.max_price > 0:
            url += f"&priceto={blueprint.max_price}"

        if blueprint.max_mileage and blueprint.max_mileage > 0:
            url += f"&kmto={blueprint.max_mileage}"

        if blueprint.max_first_registration and blueprint.max_first_registration > 0:
            url += f"&fregto={blueprint.max_first_registration}"

        url += "&ustate=N%2CU"

        if blueprint.city != None and blueprint.max_distance_from_home and blueprint.max_distance_from_home > 0:
            url += f"&zip={blueprint.city}&zipr={blueprint.max_distance_from_home}"

        new_cars_found = []

        for i in range(1, 20):
            cars = scrape_page(url + f"&page={i}", scrape_session)

            if len(cars) == 0:
                break

            new_cars = get_new_cars(cars)

            new_cars_found += new_cars

            save_cars_to_db(new_cars, _logger)
            scrape_session.ended = datetime.datetime.now()
            scrape_session.new_cars = len(new_cars)
            save_session_to_db(scrape_session, _logger)

        try:
            emails = get_emails(blueprint)
            for e in emails:
                _logger.log_info("Email: " + e)

        except Exception as e:
            _logger.log_error("Could not get emails" + str(e))
            emails = []

        try:
            mail.send_email(new_cars_found, emails, blueprint.name)
        except Exception as e:
            _logger.log_error("Could not send email" + str(e))

        _logger.log_info("Email sent")

        _logger.log_info("Scrape session ended")

    except Exception as e:
        _logger.log_error("Error while scraping autoscout" + str(e))
        print(e)


def scrape_page(url: str, scrape_session: ScrapeSession) -> list:
    """Scrape a single page of car listings"""
    print(url)

    cars = []

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            _logger.log_error(f"HTTP {response.status_code} error while fetching page: {url}")
            return []  # Return empty list on failure
    except requests.exceptions.RequestException as e:
        _logger.log_error(f"Network error while fetching page: {url} - {str(e)}")
        return []  # Return empty list on network failure

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        # Prioritize element type (article) over class names for flexibility
        articles = soup.find_all("article")
    except Exception as e:
        _logger.log_error(f"Error parsing HTML: {str(e)}")
        return []  # Return empty list on parse failure

    if len(articles) == 0:
        _logger.log_info(f"No article elements found on page: {url}")
        return []  # Return empty list when no cars found

    for article in articles:
        try:
            car = extract_car_from_article(article, scrape_session)
            if car:
                cars.append(car)
        except Exception as e:
            # Log context for debugging but don't crash the whole scrape
            car_id = article.get("data-guid", "unknown")
            _logger.log_error(f"Error scraping car {car_id}: {str(e)}")
            continue

    _logger.log_info(f"Successfully scraped {len(cars)} cars from page")
    return cars


def get_emails(blueprint: BluePrint):
    subscriptions = session.query(Subscription).filter_by(
        blueprint_id=blueprint.id).all()

    emails = []

    for subscription in subscriptions:
        emails.append(subscription.user.email)

    return emails


def car_is_new(car_id: int):
    car = session.query(Car).filter_by(id=car_id).first()

    if car == None:
        return True

    return False


def extract_car_from_article(article, scrape_session: ScrapeSession):
    """
    Extract car information from article element with fallback strategies.
    Prioritizes element types over class names for flexibility.
    
    Returns Car object or None if extraction fails.
    """
    try:
        # Extract car ID from data-guid attribute (prioritize data attributes)
        car_id = article.get("data-guid")
        if not car_id:
            _logger.log_error("No data-guid found in article")
            return None
        
        # Extract brand and model from data attributes (primary strategy)
        brand = article.get("data-make", "Unknown")
        model = article.get("data-model", "Unknown")
        
        # Extract price - try data attribute, fallback to element search
        try:
            price = int(article.get("data-price", 0))
        except (ValueError, TypeError):
            _logger.log_warning(f"Could not parse price for car {car_id}, using 0")
            price = 0
        
        # Extract mileage (condition)
        mileage = get_condition(article)
        
        # Extract first registration year - try data attribute first
        try:
            first_reg_str = article.get("data-first-registration", "2010")
            first_registration = convert_to_year(first_reg_str)
        except Exception as e:
            _logger.log_warning(f"Could not parse first registration for car {car_id}: {str(e)}")
            first_registration = 2010
        
        # Extract vehicle type
        vehicle_type = article.get("data-vehicle-type", "Unknown")
        
        # Extract location with fallback
        location = get_location(article)
        
        # Build URL from car ID
        url = f"{BASE_URL}offers/{car_id}"
        
        # Extract image from article (prioritize element types)
        image = get_image_from_article(article)
        
        # Create car object
        car = Car(
            id=car_id,
            brand=brand,
            model=model,
            price=price,
            mileage=mileage,
            first_registration=first_registration,
            vehicle_type=vehicle_type,
            location=location,
            condition=mileage,
            url=url,
            session_id=scrape_session.id,
            image=image
        )
        
        return car
        
    except Exception as e:
        car_id = article.get("data-guid", "unknown")
        _logger.log_error(f"Failed to extract car {car_id}: {str(e)}")
        # Log context for debugging
        _logger.log_error(f"Article attributes: {article.attrs if hasattr(article, 'attrs') else 'N/A'}")
        return None


def get_href(article):
    try:
        a_element = article.find(
            "a", {"class": "ListItem_title__ndA4s ListItem_title_new_design__QIU2b Link_link__Ajn7I"})
        href = a_element["href"]

        return href

    except Exception as e:
        _logger.log_error("Could not find href")
        return ""


def get_condition(article):
    """Extract condition (mileage), return default if unavailable"""
    try:
        mileage = int(article.get("data-mileage", 0))
        return mileage if mileage > 0 else 100420
    except (ValueError, TypeError) as e:
        _logger.log_error(f"Error parsing condition/mileage: {str(e)}")
        return 100420


def get_location(article):
    """
    Extract location with multiple fallback strategies.
    
    Strategies (in order):
    1. SellerInfo_address span with text splitting
    2. Any span containing location-like patterns
    3. Last span element (common pattern)
    4. Default to "Unknown"
    """
    try:
        # Strategy 1: Primary - look for SellerInfo_address span
        location_span = article.find("span", {"class": "SellerInfo_address__txoNV"})
        if location_span:
            location_text = location_span.text.split("•")
            if len(location_text) > 1:
                return location_text[1].strip()
            # If no bullet separator, try comma
            location_text = location_span.text.split(",")
            if len(location_text) > 0:
                return location_text[0].strip()
        
        # Strategy 2: Look for any span elements (flexible selector)
        all_spans = article.find_all("span")
        if all_spans:
            # Strategy 2a: Try to find span with location-like content (contains letters and spaces)
            for span in reversed(all_spans):  # Check from end as location often near the bottom
                text = span.text.strip()
                if len(text) > 3 and any(c.isalpha() for c in text):
                    # Likely a location
                    return text
            
            # Strategy 2b: Fallback to last span element
            return all_spans[-1].text.strip()
        
        _logger.log_warning(f"Could not extract location from article, no span elements found")
        return "Unknown"
    except Exception as e:
        _logger.log_error(f"Error extracting location with context: {str(e)}")
        return "Unknown"


def get_image_from_article(article):
    """
    Get the car image directly from the article listing with multiple fallback strategies.
    
    Strategies (in order):
    1. Find picture element and extract img src
    2. Find any img element directly in article
    3. Search for img with specific class patterns
    4. Return empty bytes on all failures
    
    Uses flexible selectors prioritizing element types (picture, img) over classes.
    Returns empty bytes (b"") on failure to maintain compatibility.
    """
    try:
        # Strategy 1: Find picture element (prioritize element type over classes)
        picture = article.find("picture")
        if picture:
            img = picture.find("img")
            if img and img.get('src'):
                img_url = img.get('src')
                # Validate and fetch
                if _validate_and_fetch_image(img_url):
                    return _validate_and_fetch_image(img_url)
        
        # Strategy 2: Find any img element in article
        img = article.find("img")
        if img and img.get('src'):
            img_url = img.get('src')
            result = _validate_and_fetch_image(img_url)
            if result:
                return result
        
        # Strategy 3: Try finding img with common class patterns (less flexible but worth trying)
        for class_pattern in ["Gallery", "Image", "img", "Img"]:
            img = article.find("img", {"class": lambda c: c and class_pattern in c})
            if img and img.get('src'):
                img_url = img.get('src')
                result = _validate_and_fetch_image(img_url)
                if result:
                    return result
        
        _logger.log_warning("No valid image found in article after all fallback strategies")
        return b""
        
    except Exception as e:
        _logger.log_error(f"Unexpected error extracting image with context: {str(e)}")
        return b""


def _validate_and_fetch_image(img_url: str):
    """
    Validate image URL and fetch if valid.
    Returns image bytes or None on failure.
    """
    try:
        # Validate URL before fetching (only autoscout24 listing images)
        if 'prod.pictures.autoscout24.net/listing-images' not in img_url:
            # Try alternative CDN patterns
            if 'autoscout24' not in img_url.lower():
                _logger.log_warning(f"Image URL not from autoscout24: {img_url}")
                return None
        
        response = requests.get(img_url, timeout=5)
        if response.status_code == 200:
            return response.content
        else:
            _logger.log_warning(f"HTTP {response.status_code} fetching image: {img_url}")
            return None
            
    except requests.exceptions.RequestException as e:
        _logger.log_error(f"Network error fetching image: {str(e)}")
        return None
    except Exception as e:
        _logger.log_error(f"Error validating/fetching image: {str(e)}")
        return None


def get_image(url):
    try:
        response = requests.get(BASE_URL + url)

        if response.status_code != 200:
            _logger.log_error("Could not find image")
            return b""  # Return empty bytes instead of empty string

        soup = BeautifulSoup(response.text, "html.parser")
        link_element = soup.find("link")
        image_url = link_element["href"]

        image_response = requests.get(image_url)

        if image_response.status_code != 200:
            _logger.log_error("Could not find image")
            return b""  # Return empty bytes instead of empty string

        return image_response.content

    except Exception as e:
        _logger.log_error("Could not find image")
        return b""  # Return empty bytes instead of empty string


def convert_to_year(first_registration: str):
    try:
        lowered_registration = first_registration.lower()

        if lowered_registration == "new":
            return 2023

        if lowered_registration == "used":
            return 2010

        if lowered_registration[2] == "-":
            return int(lowered_registration[3:])

        if lowered_registration[2] == "/":
            return int(lowered_registration[3:])

        else:
            return 2010

    except:
        return 2010


if __name__ == "__main__":
    start()
