from functools import wraps
from flask import request

disallowed_props = ["id", "session_id", "created", "updated"]

def remove_disallowed_properties():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the original request JSON
            request_json = request.get_json()

            # Remove disallowed properties from the request JSON
            filtered_json = {
                key: value for key, value in request_json.items() if key not in disallowed_props
            }

            # Set the modified request JSON
            request._cached_json = filtered_json

            return func(*args, **kwargs)

        return wrapper

    return decorator
