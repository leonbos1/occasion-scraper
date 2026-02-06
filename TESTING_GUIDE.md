# Testing Guide for Brand/Model Dropdown Manager

## Prerequisites

1. **Start MySQL Database**
   ```bash
   # If using Docker
   docker-compose up -d mysql
   
   # Or start MySQL service locally
   ```

2. **Start Backend Server**
   ```bash
   cd backend
   python main.py
   # Database tables will be created automatically via db.create_all()
   ```

3. **Start Frontend Dev Server**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Log in as Admin User**
   - Navigate to http://localhost:5173
   - Log in with admin credentials (role === '1')

## Testing Checklist

### 1. Catalog Scraper (Task 13.1)

**Test:** Trigger catalog scraper and verify data

1. Navigate to "Brand Catalog" in admin menu
2. Click "🔄 Run Catalog Scraper" button
3. Wait for scraper to complete (may take several minutes)
4. Verify success message shows brands/models added
5. Check database tables:
   ```sql
   SELECT COUNT(*) FROM brands;
   SELECT COUNT(*) FROM models;
   SELECT * FROM brands LIMIT 10;
   ```

**Expected:** Multiple brands and models inserted with `enabled=1`, `last_seen` timestamp populated

### 2. Public API Endpoints (Tasks 13.2-13.3)

**Test GET /api/brands**
```bash
curl http://localhost:5000/api/brands
```
**Expected:** 
- Returns only enabled brands
- Sorted by display_name
- JSON array with id, name, slug, display_name, enabled, last_seen

**Test GET /api/models**
```bash
# Replace 'bmw' with actual brand slug from database
curl http://localhost:5000/api/models?brand_slug=bmw
```
**Expected:** 
- Returns only enabled models for specified brand
- Sorted by display_name
- Returns 404 if brand not found
- Returns 400 if brand_slug missing

### 3. Blueprint Creation (Task 13.4)

**Test:** Create new blueprint with dropdowns

1. Navigate to Blueprints → Create Blueprint
2. Verify brand dropdown loads and is searchable
3. Select a brand (e.g., "BMW")
4. Verify model dropdown enables and loads models for BMW
5. Select a model (e.g., "3 Series")
6. Fill other required fields
7. Submit blueprint
8. Check database:
   ```sql
   SELECT brand, model FROM blueprints ORDER BY id DESC LIMIT 1;
   ```

**Expected:** Brand and model columns contain slugs (e.g., "bmw", "3-series"), not display names

### 4. Blueprint Editing (Tasks 13.5-13.6)

**Test:** Edit blueprint with catalog values

1. Edit the blueprint created in test #3
2. Verify brand dropdown pre-populates with "BMW"
3. Verify model dropdown pre-populates with "3 Series"
4. Change brand to "Audi"
5. Verify model dropdown clears and loads Audi models
6. Select new model
7. Save changes
8. Verify database updated with new slugs

**Test:** Edit blueprint with non-catalog values

1. Create a blueprint via API with custom values:
   ```bash
   curl -X POST http://localhost:5000/blueprints \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"name":"Test","brand":"custom-brand","model":"custom-model",...}'
   ```
2. Edit this blueprint in UI
3. Verify brand dropdown shows "(custom: custom-brand)"
4. Verify model field shows "(custom: custom-model)"

**Expected:** Custom values displayed but not selectable from dropdown

### 5. Brand Management UI (Tasks 13.7-13.8)

**Test:** Enable/disable brands

1. Navigate to Brand Catalog
2. Find an enabled brand, click toggle
3. Verify brand becomes disabled (gray)
4. Go to Blueprints → Create Blueprint
5. Verify disabled brand does NOT appear in dropdown
6. Return to Brand Catalog, re-enable brand
7. Refresh Create Blueprint page
8. Verify brand now appears in dropdown

**Test:** Update display name

1. Find a brand (e.g., "bmw" with display_name "BMW")
2. Click edit icon, change display_name to "BMW Motors"
3. Save changes
4. Go to Create Blueprint page
5. Verify dropdown shows "BMW Motors"
6. Create blueprint with this brand
7. Verify database still stores slug "bmw", not "BMW Motors"

### 6. Model Management UI (Task 13.9)

**Test:** Enable/disable models

1. Navigate to Model Catalog
2. Filter by a brand (e.g., BMW)
3. Disable a model (e.g., "3 Series")
4. Go to Create Blueprint
5. Select BMW brand
6. Verify "3 Series" does NOT appear in model dropdown
7. Re-enable model in Model Catalog
8. Verify it appears in dropdown

### 7. Bulk Operations (Task 13.10)

**Test:** Bulk enable/disable

1. In Brand Catalog, select 3-5 brands using checkboxes
2. Click "Disable Selected"
3. Verify all selected brands become disabled
4. Select same brands again
5. Click "Enable Selected"
6. Verify all selected brands become enabled

Repeat for Model Catalog.

### 8. Frontend Caching (Task 13.11)

**Test:** Cache behavior

1. Open browser DevTools → Application → Session Storage
2. Navigate to Create Blueprint page
3. Verify `catalog_brands` key appears in sessionStorage
4. Select a brand (e.g., BMW)
5. Verify `catalog_models_bmw` key appears
6. Check timestamp in cached data:
   ```javascript
   JSON.parse(sessionStorage.getItem('catalog_brands')).timestamp
   ```
7. Refresh page within 1 hour
8. Verify no network requests to /api/brands (check Network tab)
9. Clear sessionStorage or wait 1 hour
10. Refresh page
11. Verify new network request to /api/brands

### 9. Car Scraper Integration (Task 13.12)

**Test:** Existing scraper compatibility

1. Create a blueprint with dropdowns (stores slugs)
2. Start car scraper for this blueprint:
   ```bash
   curl -X POST http://localhost:5000/scrape/blueprint/1
   ```
3. Verify scraper runs successfully
4. Check scraped cars in database:
   ```sql
   SELECT brand, model FROM cars WHERE blueprint_id = 1 LIMIT 5;
   ```

**Expected:** Cars are scraped and stored correctly using slug values from blueprint

## Common Issues

### Scraper finds no brands
- AutoScout24 site structure may have changed
- Check HTML manually at https://www.autoscout24.nl/lst
- Update parsing logic in `catalog_scraper.py` if needed

### Dropdowns not loading
- Check browser console for errors
- Verify backend is running and /api/brands returns data
- Check CORS settings if frontend on different port

### Cache not clearing
- Manually clear: `sessionStorage.clear()`
- Check TTL calculation in `catalogCache.js`
- Verify timestamp is Date.now() (milliseconds)

### Admin routes not accessible
- Verify user role is "1" (admin)
- Check token is valid and included in Authorization header
- Verify @admin_required decorator is present on routes

## Completion Criteria

All 12 testing tasks (13.1-13.12) should pass before considering the feature production-ready.
