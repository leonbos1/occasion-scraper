from functools import wraps
from flask import request

disallowed_props = ["id", "session_id", "created", "updated"]

def remove_disallowed_properties():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request_json = request.get_json()

            filtered_json = {
                key: value for key, value in request_json.items() if key not in disallowed_props
            }

            request._cached_json = filtered_json

            return func(*args, **kwargs)

        return wrapper

    return decorator
