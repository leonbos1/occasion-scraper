# API Documentation

## Catalog Management Endpoints

### Public Catalog Endpoints

#### GET /api/brands
Get all enabled brands for dropdown menus.

**Response:**
```json
[
  {
    "id": 1,
    "name": "alfa-romeo",
    "slug": "alfa-romeo",
    "display_name": "Alfa Romeo",
    "enabled": true,
    "last_seen": "2024-01-20T10:30:00"
  }
]
```

**Sorting:** Results are sorted by `display_name` ascending.

#### GET /api/models
Get all enabled models for a specific brand.

**Query Parameters:**
- `brand_slug` (required): The brand slug (e.g., "bmw")

**Response:**
```json
[
  {
    "id": 42,
    "brand_id": 5,
    "name": "3-series",
    "slug": "3-series",
    "display_name": "3 Series",
    "enabled": true,
    "last_seen": "2024-01-20T10:35:00"
  }
]
```

**Sorting:** Results are sorted by `display_name` ascending.

**Error Cases:**
- 400 Bad Request: Missing `brand_slug` parameter
- 404 Not Found: Brand not found

### Admin Catalog Endpoints

All admin endpoints require authentication with admin role (role === '1').

#### POST /api/admin/scrape-catalog
Trigger the catalog scraper to discover brands and models from AutoScout24.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Catalog scrape completed",
  "summary": {
    "brands_added": 45,
    "brands_updated": 12,
    "brands_failed": 0,
    "models_added": 523,
    "models_updated": 87,
    "models_failed": 2,
    "duration_seconds": 245
  }
}
```

**Notes:**
- Respects robots.txt rules
- Applies rate limiting (1-3 second delays between requests)
- Updates `last_seen` timestamp for existing entries
- New brands/models are enabled by default

#### GET /api/admin/brands
Get all brands (including disabled) for management.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** Same format as public endpoint, but includes disabled brands.

#### POST /api/admin/brands/:id
Update a brand's display name or enabled status.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "display_name": "Alfa Romeo",  // optional
  "enabled": true                // optional
}
```

**Response:**
```json
{
  "message": "Brand updated successfully",
  "brand": { /* updated brand object */ }
}
```

#### GET /api/admin/models
Get all models (including disabled) for management.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `brand_id` (optional): Filter models by brand

**Response:** Same format as public endpoint, but includes disabled models and brand information:
```json
[
  {
    "id": 42,
    "brand_id": 5,
    "brand_name": "BMW",  // included for admin views
    "name": "3-series",
    "slug": "3-series",
    "display_name": "3 Series",
    "enabled": true,
    "last_seen": "2024-01-20T10:35:00"
  }
]
```

#### POST /api/admin/models/:id
Update a model's display name or enabled status.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "display_name": "3 Series",  // optional
  "enabled": true              // optional
}
```

**Response:**
```json
{
  "message": "Model updated successfully",
  "model": { /* updated model object */ }
}
```

## Frontend Caching

The frontend caches catalog data in `sessionStorage` with a 1-hour TTL:
- Cache key format: `catalog_brands`, `catalog_models_{brandSlug}`
- Cache structure: `{ data: [...], timestamp: Date.now() }`
- TTL: 3600000ms (1 hour)

Cache is automatically cleared:
- After 1 hour
- When user triggers catalog scraper
- When admin updates brand/model data (component-level refresh)

To manually clear cache: `sessionStorage.removeItem('catalog_brands')`
