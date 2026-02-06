# Tasks: Brand and Model Dropdown Manager

## 1. Database Setup

- [x] 1.1 Create Alembic migration for brands table with columns: id, name, slug, display_name, enabled, last_seen, created_at, updated_at
- [x] 1.2 Create Alembic migration for models table with columns: id, brand_id, name, slug, display_name, enabled, last_seen, created_at, updated_at
- [x] 1.3 Add indexes: brands(slug), brands(enabled), models(brand_id), models(enabled), unique constraint on models(brand_id, slug)
- [ ] 1.4 Run migration to apply schema changes to database

## 2. Backend Models

- [x] 2.1 Create backend/models/brand.py with Brand SQLAlchemy model matching schema
- [x] 2.2 Create backend/models/model.py with Model SQLAlchemy model matching schema
- [x] 2.3 Add relationship from Brand to Model (one-to-many)
- [x] 2.4 Define serialization methods (to_dict) for API responses
- [x] 2.5 Import new models in backend/models/__init__.py

## 3. Catalog Scraper

- [x] 3.1 Create backend/scrapers/catalog_scraper.py module
- [x] 3.2 Implement fetch_brands() function to scrape AutoScout24 brand listing page
- [x] 3.3 Implement fetch_models_for_brand(brand_slug) function to scrape brand-specific model page
- [x] 3.4 Implement upsert_brand() function to insert/update brand records in database
- [x] 3.5 Implement upsert_model() function to insert/update model records in database
- [x] 3.6 Add rate limiting with random 1-3 second delays between requests
- [x] 3.7 Add robots.txt parser to respect AutoScout24's crawling rules
- [x] 3.8 Implement scrape_catalog() orchestrator function that calls fetch_brands, then fetch_models for each brand
- [x] 3.9 Add error handling with logging for scraping failures (continue on error)
- [x] 3.10 Return summary dict with success/failure counts and failed brands list

## 4. Backend API Routes - Public Endpoints

- [x] 4.1 Create backend/routes/catalog.py for catalog-related routes
- [x] 4.2 Add GET /api/brands endpoint that returns enabled brands only (id, display_name, slug) sorted by display_name
- [x] 4.3 Add GET /api/models endpoint with brand_slug query parameter, returns enabled models for that brand
- [x] 4.4 Add validation for brand_slug parameter (return 400 if missing, 404 if brand not found)
- [x] 4.5 Register catalog routes blueprint in backend/__init__.py

## 5. Backend API Routes - Admin Endpoints

- [x] 5.1 Add POST /api/admin/scrape-catalog endpoint to trigger catalog scraper
- [x] 5.2 Add admin role check middleware to /api/admin/scrape-catalog endpoint
- [x] 5.3 Add GET /api/admin/brands endpoint that returns all brands (enabled and disabled) with full details
- [x] 5.4 Add POST /api/admin/brands/<id> endpoint to update brand display_name and/or enabled status
- [x] 5.5 Add validation for POST /api/admin/brands/<id> (display_name not empty, enabled is boolean)
- [x] 5.6 Add GET /api/admin/models endpoint that returns all models with optional brand_id filter
- [x] 5.7 Add POST /api/admin/models/<id> endpoint to update model display_name and/or enabled status
- [x] 5.8 Add validation for POST /api/admin/models/<id> (display_name not empty, enabled is boolean)
- [x] 5.9 Add admin role checks to all /api/admin/brands and /api/admin/models endpoints

## 6. Frontend Dependencies and Utilities

- [x] 6.1 Install vue-select package: npm install vue-select@4
- [x] 6.2 Create frontend/src/utils/catalogCache.js with get/set functions for sessionStorage caching
- [x] 6.3 Implement cache TTL checking (1 hour expiration) in catalogCache.js
- [x] 6.4 Create frontend/src/services/CatalogRepository.js with API methods: getBrands(), getModels(brandSlug)

## 7. Frontend Dropdown Components

- [x] 7.1 Create frontend/src/components/shared/BrandDropdown.vue using vue-select
- [x] 7.2 Implement brand fetching with cache in BrandDropdown.vue (use catalogCache.js)
- [x] 7.3 Add searchable filtering by display_name in BrandDropdown.vue
- [x] 7.4 Emit brand slug value when selection changes in BrandDropdown.vue
- [x] 7.5 Handle empty state ("No brands available") in BrandDropdown.vue
- [x] 7.6 Create frontend/src/components/shared/ModelDropdown.vue using vue-select
- [x] 7.7 Accept brand_slug prop in ModelDropdown.vue, disable if not provided
- [x] 7.8 Implement model fetching with cache in ModelDropdown.vue (use catalogCache.js with brand-specific key)
- [x] 7.9 Add searchable filtering by display_name in ModelDropdown.vue
- [x] 7.10 Emit model slug value when selection changes in ModelDropdown.vue
- [x] 7.11 Handle empty state ("No models available for {brand}") in ModelDropdown.vue
- [x] 7.12 Clear model selection when brand changes in ModelDropdown.vue

## 8. Update Blueprint Creation Form

- [x] 8.1 Replace brand text input with BrandDropdown component in CreateBlueprint.vue
- [x] 8.2 Replace model text input with ModelDropdown component in CreateBlueprint.vue
- [x] 8.3 Pass selected brand slug to ModelDropdown in CreateBlueprint.vue
- [x] 8.4 Store brand and model slugs (not display names) in form data for submission
- [x] 8.5 Add form validation requiring brand and model selections before submit

## 9. Update Blueprint Edit Form

- [x] 9.1 Replace brand text input with BrandDropdown component in EditBlueprintComponent.vue
- [x] 9.2 Replace model text input with ModelDropdown component in EditBlueprintComponent.vue
- [x] 9.3 Pre-populate BrandDropdown with existing blueprint brand value
- [x] 9.4 Pre-populate ModelDropdown with existing blueprint model value
- [x] 9.5 Handle legacy non-catalog values by showing "(custom - not in catalog)" option
- [x] 9.6 Preserve custom values if user doesn't change them (submit original text if still custom)
- [x] 9.7 Clear and reload models when user changes brand selection

## 10. Admin Brand Management UI

- [ ] 10.1 Create frontend/src/components/admin/BrandManagement.vue page component
- [ ] 10.2 Create frontend/src/services/AdminCatalogRepository.js with methods: getAdminBrands(), updateBrand(id, data), triggerCatalogScrape()
- [ ] 10.3 Implement brand table in BrandManagement.vue showing: name, display_name, enabled, last_seen
- [ ] 10.4 Add search filter input for brands in BrandManagement.vue
- [ ] 10.5 Add inline edit functionality for display_name in brand table
- [ ] 10.6 Add enable/disable toggle button for each brand row
- [ ] 10.7 Add bulk select checkboxes for brands
- [ ] 10.8 Add "Enable Selected" and "Disable Selected" bulk action buttons
- [ ] 10.9 Add "View Models" link/button for each brand that navigates to ModelManagement with brand filter
- [ ] 10.10 Add "Run Catalog Scraper" button at top of page (admin only)
- [ ] 10.11 Show loading state and success/error messages for catalog scraper trigger
- [ ] 10.12 Add route for /admin/brands in frontend router

## 11. Admin Model Management UI

- [ ] 11.1 Create frontend/src/components/admin/ModelManagement.vue page component
- [ ] 11.2 Add getAdminModels(brandId) and updateModel(id, data) methods to AdminCatalogRepository.js
- [ ] 11.3 Implement model table in ModelManagement.vue showing: brand_name, name, display_name, enabled, last_seen
- [ ] 11.4 Add brand filter dropdown at top of model table
- [ ] 11.5 Add inline edit functionality for display_name in model table
- [ ] 11.6 Add enable/disable toggle button for each model row
- [ ] 11.7 Add bulk select checkboxes for models
- [ ] 11.8 Add "Enable Selected" and "Disable Selected" bulk action buttons
- [ ] 11.9 Pre-filter models if brand_id passed via route query parameter
- [ ] 11.10 Add route for /admin/models in frontend router

## 12. Navigation and Integration

- [x] 12.1 Add "Brand Catalog" link to admin navigation menu pointing to /admin/brands
- [x] 12.2 Add "Model Catalog" link to admin navigation menu pointing to /admin/models
- [x] 12.3 Update UserDropdown.vue or admin nav to include catalog management links

## 13. Testing and Validation

- [ ] 13.1 Test catalog scraper manually: POST /api/admin/scrape-catalog and verify brands/models in database
- [ ] 13.2 Test GET /api/brands returns only enabled brands
- [ ] 13.3 Test GET /api/models?brand_slug=alfa-romeo returns correct models
- [ ] 13.4 Test creating new blueprint with dropdowns - verify slugs are submitted
- [ ] 13.5 Test editing existing blueprint with catalog values - verify pre-population
- [ ] 13.6 Test editing existing blueprint with non-catalog values - verify "(custom)" handling
- [ ] 13.7 Test brand management UI - enable/disable brands and verify changes
- [ ] 13.8 Test brand management UI - update display_name and verify change in dropdowns
- [ ] 13.9 Test model management UI - enable/disable models and verify changes
- [ ] 13.10 Test bulk enable/disable operations for brands and models
- [ ] 13.11 Test frontend caching - verify brands/models not re-fetched within 1 hour
- [ ] 13.12 Test that existing car scraper still works with slug values from dropdowns

## 14. Documentation and Cleanup

- [x] 14.1 Document catalog scraper usage in README.md (how to run initial scrape)
- [x] 14.2 Add API endpoint documentation for new catalog routes
- [x] 14.3 Add comments explaining display_name vs slug distinction in admin UI
- [x] 14.4 Remove any debug logging added during development
