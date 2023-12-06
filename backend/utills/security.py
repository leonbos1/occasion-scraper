from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
import json

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

API_KEY = ''

with open('./credentials.json') as f:
    data = json.load(f)
    API_KEY = data['api_key']

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key