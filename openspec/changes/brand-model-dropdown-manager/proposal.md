# Proposal: Brand and Model Dropdown Manager

## Why

Currently, users must manually type brand and model names when creating blueprints for car scraping. This leads to several problems:

1. **User friction**: Typing exact names is error-prone and time-consuming
2. **Discovery issue**: Users don't know which brands/models are available on AutoScout24
3. **Inconsistency**: Manual entry can lead to typos or incorrect formatting
4. **No visibility**: Administrators cannot control which options appear in dropdowns

The application needs a way to discover all available brands and models from AutoScout24, store them centrally, and present them as curated dropdown options to users.

## What Changes

This change introduces a brand/model master data system with two main components:

### 1. Brand/Model Discovery Scraper
A one-time utility scraper that enumerates all available brand and model combinations from AutoScout24's website structure. This scraper:
- Crawls AutoScout24 to discover all valid brands
- For each brand, discovers all available models
- Stores raw brand/model data in the database
- Can be re-run periodically to update available options

### 2. Management Interface
An administrative UI that allows control over dropdown content:
- View all discovered brands and models
- Enable/disable specific brands or models from appearing in dropdowns
- Customize display text (e.g., show "Alfa Romeo" but use "alfa-romeo" for API calls)
- Override sorting order if needed
- Bulk enable/disable operations

### 3. Frontend Integration
Update blueprint creation/editing forms to:
- Replace text inputs with searchable dropdown selects
- Fetch options from the curated brand/model API
- Display user-friendly text while submitting API-friendly values

## Capabilities

### New Capabilities
- `scrape-brand-model-catalog`: Discover all available brands and models from AutoScout24
- `manage-brand-model-dropdowns`: Administrative UI for curating dropdown options
- `fetch-dropdown-options`: API endpoint providing curated brand/model lists for frontend dropdowns

### Modified Capabilities
- `create-blueprint`: Blueprint creation form uses dropdowns instead of text inputs
- `edit-blueprint`: Blueprint editing form uses dropdowns instead of text inputs

## Impact

### Database Schema
New tables required:
- `brands`: Store discovered brands with display names and enabled status
- `models`: Store discovered models linked to brands with display names and enabled status

### API Endpoints
- `GET /api/brands` - List all enabled brands for dropdowns
- `GET /api/models?brand={brand}` - List enabled models for a specific brand
- `GET /api/admin/brands` - Admin view of all brands (enabled/disabled)
- `POST /api/admin/brands/{id}` - Update brand display name or enabled status
- `GET /api/admin/models` - Admin view of all models (enabled/disabled)
- `POST /api/admin/models/{id}` - Update model display name or enabled status
- `POST /api/admin/scrape-catalog` - Trigger the brand/model discovery scraper

### User Experience
- Blueprint creation becomes faster and more intuitive
- Users can discover available options without guessing
- Reduced errors from typos or incorrect formatting
- Administrators gain control over which options are presented

### Technical Considerations
- Discovery scraper may need rate limiting to avoid blocking by AutoScout24
- Dropdown data should be cached on frontend to reduce API calls
- Management UI requires admin-level authentication
- Initial population of brands/models requires one-time scraper run
