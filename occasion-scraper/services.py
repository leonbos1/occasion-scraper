#!/usr/bin/env python3
"""
Home Assistant Addon Service Handler

This script handles service calls from Home Assistant via stdin/stdout.
It receives JSON commands and proxies them to the backend API.
"""

import sys
import json
import requests
from typing import Dict, Any

BACKEND_URL = "http://backend:5000"

def log(message: str):
    """Log to stderr so it doesn't interfere with stdout responses"""
    print(f"[services.py] {message}", file=sys.stderr)

def send_response(success: bool, data: Any = None, error: str = None):
    """Send JSON response to Home Assistant via stdout"""
    response = {
        "success": success,
        "data": data,
        "error": error
    }
    print(json.dumps(response))
    sys.stdout.flush()

def trigger_scrape(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Trigger a scraping session
    
    Args:
        params: {
            "scrapers": ["autoscout", "marktplaats"] (optional, defaults to all enabled)
        }
    
    Returns:
        {
            "session_id": "uuid",
            "message": "Scraping started"
        }
    """
    try:
        scrapers = params.get('scrapers', [])
        
        # Call backend API to start scraping
        response = requests.post(
            f"{BACKEND_URL}/api/scrape",
            json={"scrapers": scrapers},
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        log(f"Scraping triggered: {data}")
        
        return {
            "session_id": data.get("session_id"),
            "message": "Scraping started successfully"
        }
        
    except requests.RequestException as e:
        log(f"Error triggering scrape: {e}")
        raise Exception(f"Failed to trigger scrape: {str(e)}")

def get_scrape_status(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get scraping session status
    
    Args:
        params: {
            "session_id": "uuid"
        }
    
    Returns:
        {
            "status": "running" | "completed" | "failed",
            "progress": "50%",
            "cars_found": 123,
            "duration": 300
        }
    """
    try:
        session_id = params.get('session_id')
        if not session_id:
            raise ValueError("session_id is required")
        
        response = requests.get(
            f"{BACKEND_URL}/api/scrape-sessions/{session_id}",
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        log(f"Scrape status retrieved: {data}")
        
        return data
        
    except requests.RequestException as e:
        log(f"Error getting scrape status: {e}")
        raise Exception(f"Failed to get scrape status: {str(e)}")

def list_cars(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    List cars with filters
    
    Args:
        params: {
            "brand": "volkswagen" (optional),
            "model": "golf" (optional),
            "max_price": 15000 (optional),
            "min_price": 5000 (optional),
            "max_mileage": 100000 (optional),
            "limit": 50 (optional, default 100)
        }
    
    Returns:
        {
            "cars": [...],
            "count": 50
        }
    """
    try:
        # Build query parameters
        query_params = {}
        
        if 'brand' in params:
            query_params['brand'] = params['brand']
        if 'model' in params:
            query_params['model'] = params['model']
        if 'max_price' in params:
            query_params['max_price'] = params['max_price']
        if 'min_price' in params:
            query_params['min_price'] = params['min_price']
        if 'max_mileage' in params:
            query_params['max_mileage'] = params['max_mileage']
        
        limit = params.get('limit', 100)
        query_params['limit'] = limit
        
        response = requests.get(
            f"{BACKEND_URL}/api/cars",
            params=query_params,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        cars = data.get('data', [])
        
        log(f"Retrieved {len(cars)} cars")
        
        return {
            "cars": cars,
            "count": len(cars)
        }
        
    except requests.RequestException as e:
        log(f"Error listing cars: {e}")
        raise Exception(f"Failed to list cars: {str(e)}")

def get_car_details(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get details for a specific car
    
    Args:
        params: {
            "car_id": "uuid"
        }
    
    Returns:
        {
            "car": {...}
        }
    """
    try:
        car_id = params.get('car_id')
        if not car_id:
            raise ValueError("car_id is required")
        
        response = requests.get(
            f"{BACKEND_URL}/api/cars/{car_id}",
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        log(f"Car details retrieved: {car_id}")
        
        return {
            "car": data.get('data', data)
        }
        
    except requests.RequestException as e:
        log(f"Error getting car details: {e}")
        raise Exception(f"Failed to get car details: {str(e)}")

# Service handler mapping
SERVICE_HANDLERS = {
    'trigger_scrape': trigger_scrape,
    'get_scrape_status': get_scrape_status,
    'list_cars': list_cars,
    'get_car_details': get_car_details,
}

def handle_service_call(service_name: str, params: Dict[str, Any]):
    """Handle a service call and send response"""
    log(f"Handling service: {service_name} with params: {params}")
    
    if service_name not in SERVICE_HANDLERS:
        send_response(
            success=False,
            error=f"Unknown service: {service_name}. Available: {', '.join(SERVICE_HANDLERS.keys())}"
        )
        return
    
    try:
        handler = SERVICE_HANDLERS[service_name]
        result = handler(params)
        send_response(success=True, data=result)
        
    except Exception as e:
        log(f"Service call failed: {e}")
        send_response(success=False, error=str(e))

def main():
    """Main loop: read from stdin and handle service calls"""
    log("Service handler started, waiting for commands...")
    
    for line in sys.stdin:
        try:
            # Parse JSON command from stdin
            command = json.loads(line.strip())
            
            service_name = command.get('service')
            params = command.get('params', {})
            
            if not service_name:
                send_response(success=False, error="No service specified")
                continue
            
            handle_service_call(service_name, params)
            
        except json.JSONDecodeError as e:
            log(f"Invalid JSON: {e}")
            send_response(success=False, error=f"Invalid JSON: {str(e)}")
            
        except Exception as e:
            log(f"Unexpected error: {e}")
            send_response(success=False, error=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
