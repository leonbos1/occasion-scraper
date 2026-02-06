# Spec: scrape-brand-model-catalog

## ADDED Requirements

### Requirement: Discover all brands from AutoScout24
The system SHALL scrape AutoScout24 to enumerate all available car brands.

#### Scenario: Successfully discover brands
- **WHEN** the catalog scraper is triggered
- **THEN** system fetches the AutoScout24 brand listing page
- **THEN** system extracts all brand names and their URL slugs
- **THEN** system stores each brand in the brands table with enabled=true by default

#### Scenario: Handle scraping failures
- **WHEN** AutoScout24 is unreachable or returns an error
- **THEN** system logs the error with details
- **THEN** system does not modify existing brand data
- **THEN** system returns failure status to the caller

### Requirement: Discover all models for each brand
The system SHALL scrape AutoScout24 to enumerate all available models for each discovered brand.

#### Scenario: Successfully discover models for a brand
- **WHEN** brand discovery completes successfully
- **THEN** system iterates through each discovered brand
- **THEN** system fetches the model listing for that brand
- **THEN** system extracts all model names and their URL slugs
- **THEN** system stores each model in the models table linked to its brand with enabled=true by default

#### Scenario: Handle partial model discovery failures
- **WHEN** model discovery fails for a specific brand
- **THEN** system logs the error with brand details
- **THEN** system continues discovering models for remaining brands
- **THEN** system reports partial success with failed brand list

### Requirement: Store brand metadata
The system SHALL persist brand information with display names and API slugs.

#### Scenario: Store new brand
- **WHEN** a brand is discovered that doesn't exist in the database
- **THEN** system creates a new brand record with name, slug, and enabled=true
- **THEN** system records the discovery timestamp

#### Scenario: Update existing brand
- **WHEN** a brand is discovered that already exists in the database
- **THEN** system updates the slug if it has changed
- **THEN** system does not change the enabled status
- **THEN** system does not change the display_name if it was customized
- **THEN** system updates the last_seen timestamp

### Requirement: Store model metadata
The system SHALL persist model information with display names, API slugs, and brand associations.

#### Scenario: Store new model
- **WHEN** a model is discovered that doesn't exist for the given brand
- **THEN** system creates a new model record with name, slug, brand_id, and enabled=true
- **THEN** system records the discovery timestamp

#### Scenario: Update existing model
- **WHEN** a model is discovered that already exists for the given brand
- **THEN** system updates the slug if it has changed
- **THEN** system does not change the enabled status
- **THEN** system does not change the display_name if it was customized
- **THEN** system updates the last_seen timestamp

### Requirement: Provide scraper triggering endpoint
The system SHALL expose an API endpoint to trigger the catalog scraper.

#### Scenario: Authenticated admin triggers scraper
- **WHEN** an authenticated admin user calls POST /api/admin/scrape-catalog
- **THEN** system validates the user has admin role
- **THEN** system starts the catalog scraper in the background
- **THEN** system returns 202 Accepted with scraping session ID

#### Scenario: Non-admin attempts to trigger scraper
- **WHEN** a non-admin user calls POST /api/admin/scrape-catalog
- **THEN** system returns 403 Forbidden
- **THEN** system does not start the scraper

### Requirement: Rate limit scraping requests
The system SHALL implement rate limiting to avoid being blocked by AutoScout24.

#### Scenario: Apply delay between requests
- **WHEN** scraper makes multiple requests to AutoScout24
- **THEN** system waits at least 1 second between consecutive requests
- **THEN** system varies the delay randomly between 1-3 seconds

#### Scenario: Respect robots.txt
- **WHEN** scraper initializes
- **THEN** system fetches and parses AutoScout24's robots.txt
- **THEN** system only accesses allowed paths
