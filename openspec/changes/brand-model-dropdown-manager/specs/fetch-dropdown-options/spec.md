# Spec: fetch-dropdown-options

## ADDED Requirements

### Requirement: Provide enabled brands for dropdowns
The system SHALL expose an API endpoint that returns only enabled brands for user-facing dropdowns.

#### Scenario: Fetch enabled brands
- **WHEN** a user calls GET /api/brands
- **THEN** system returns all brands where enabled=true
- **THEN** response includes id, display_name, slug for each brand
- **THEN** brands are sorted alphabetically by display_name

#### Scenario: No enabled brands available
- **WHEN** a user calls GET /api/brands and no brands are enabled
- **THEN** system returns empty array
- **THEN** system returns 200 OK status

### Requirement: Provide enabled models for a brand
The system SHALL expose an API endpoint that returns only enabled models for a specific brand.

#### Scenario: Fetch enabled models for a brand
- **WHEN** a user calls GET /api/models?brand_slug={slug}
- **THEN** system finds the brand by slug
- **THEN** system returns all models where brand_id matches and both brand.enabled=true and model.enabled=true
- **THEN** response includes id, display_name, slug for each model
- **THEN** models are sorted alphabetically by display_name

#### Scenario: Fetch models for disabled brand
- **WHEN** a user calls GET /api/models?brand_slug={slug} for a disabled brand
- **THEN** system returns empty array
- **THEN** system returns 200 OK status

#### Scenario: Invalid brand slug provided
- **WHEN** a user calls GET /api/models?brand_slug={slug} with non-existent slug
- **THEN** system returns 404 Not Found
- **THEN** error message indicates brand not found

#### Scenario: Missing brand parameter
- **WHEN** a user calls GET /api/models without brand_slug parameter
- **THEN** system returns 400 Bad Request
- **THEN** error message indicates brand_slug is required

### Requirement: Cache dropdown data on frontend
The system SHALL implement client-side caching to minimize API calls for dropdown data.

#### Scenario: Initial brand dropdown load
- **WHEN** user opens a page with brand dropdown for the first time
- **THEN** frontend fetches brands from API
- **THEN** frontend caches the response for 1 hour
- **THEN** subsequent brand dropdown loads use cached data

#### Scenario: Initial model dropdown load
- **WHEN** user selects a brand in the dropdown
- **THEN** frontend fetches models for that brand from API
- **THEN** frontend caches the response for 1 hour keyed by brand_slug
- **THEN** subsequent loads for same brand use cached data

#### Scenario: Cache expiration
- **WHEN** cached data is older than 1 hour
- **THEN** frontend fetches fresh data from API
- **THEN** frontend updates the cache with new data

### Requirement: Support searchable dropdowns
The system SHALL provide dropdown components that allow users to search and filter options.

#### Scenario: User searches in brand dropdown
- **WHEN** user types in the brand dropdown search box
- **THEN** dropdown filters brands by display_name matching the search term
- **THEN** search is case-insensitive
- **THEN** matching brands are displayed in the dropdown list

#### Scenario: User searches in model dropdown
- **WHEN** user types in the model dropdown search box
- **THEN** dropdown filters models by display_name matching the search term
- **THEN** search is case-insensitive
- **THEN** matching models are displayed in the dropdown list

### Requirement: Handle empty dropdown states
The system SHALL display appropriate messages when no options are available.

#### Scenario: No brands available
- **WHEN** brand dropdown has no options (all disabled or none scraped)
- **THEN** dropdown displays "No brands available"
- **THEN** dropdown is disabled

#### Scenario: No models available for selected brand
- **WHEN** model dropdown has no options for the selected brand
- **THEN** dropdown displays "No models available for {brand}"
- **THEN** dropdown is disabled

### Requirement: Maintain slug values for API calls
The system SHALL use display_name for UI but submit slug values in API calls.

#### Scenario: User selects brand from dropdown
- **WHEN** user selects a brand from the dropdown
- **THEN** frontend displays the brand's display_name
- **THEN** frontend stores the brand's slug for API submission
- **THEN** when form is submitted, slug is sent to backend

#### Scenario: User selects model from dropdown
- **WHEN** user selects a model from the dropdown
- **THEN** frontend displays the model's display_name
- **THEN** frontend stores the model's slug for API submission
- **THEN** when form is submitted, slug is sent to backend
