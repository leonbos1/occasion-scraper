# Spec: manage-brand-model-dropdowns

## ADDED Requirements

### Requirement: List all brands for administration
The system SHALL provide an API endpoint to retrieve all brands including disabled ones.

#### Scenario: Admin fetches all brands
- **WHEN** an authenticated admin calls GET /api/admin/brands
- **THEN** system returns all brands with id, name, slug, display_name, enabled, last_seen
- **THEN** brands are sorted alphabetically by display_name
- **THEN** response includes both enabled and disabled brands

#### Scenario: Non-admin attempts to fetch admin brand list
- **WHEN** a non-admin user calls GET /api/admin/brands
- **THEN** system returns 403 Forbidden

### Requirement: List all models for administration
The system SHALL provide an API endpoint to retrieve all models including disabled ones.

#### Scenario: Admin fetches all models
- **WHEN** an authenticated admin calls GET /api/admin/models
- **THEN** system returns all models with id, name, slug, display_name, brand_id, brand_name, enabled, last_seen
- **THEN** models are sorted alphabetically by brand_name then display_name

#### Scenario: Admin fetches models for specific brand
- **WHEN** an authenticated admin calls GET /api/admin/models?brand_id={id}
- **THEN** system returns only models for that brand
- **THEN** models are sorted alphabetically by display_name

### Requirement: Update brand display name
The system SHALL allow administrators to customize the text shown in dropdowns for a brand.

#### Scenario: Admin updates brand display name
- **WHEN** admin calls POST /api/admin/brands/{id} with display_name field
- **THEN** system validates display_name is not empty
- **THEN** system updates the brand's display_name
- **THEN** system returns the updated brand record

#### Scenario: Empty display name provided
- **WHEN** admin provides empty or whitespace-only display_name
- **THEN** system returns 400 Bad Request
- **THEN** system does not modify the brand

### Requirement: Enable or disable brands
The system SHALL allow administrators to control which brands appear in user-facing dropdowns.

#### Scenario: Admin disables a brand
- **WHEN** admin calls POST /api/admin/brands/{id} with enabled=false
- **THEN** system updates the brand's enabled status to false
- **THEN** brand no longer appears in GET /api/brands endpoint
- **THEN** all models for that brand are hidden from dropdowns regardless of their enabled status

#### Scenario: Admin enables a brand
- **WHEN** admin calls POST /api/admin/brands/{id} with enabled=true
- **THEN** system updates the brand's enabled status to true
- **THEN** brand appears in GET /api/brands endpoint
- **THEN** enabled models for that brand appear in model dropdowns

### Requirement: Update model display name
The system SHALL allow administrators to customize the text shown in dropdowns for a model.

#### Scenario: Admin updates model display name
- **WHEN** admin calls POST /api/admin/models/{id} with display_name field
- **THEN** system validates display_name is not empty
- **THEN** system updates the model's display_name
- **THEN** system returns the updated model record

### Requirement: Enable or disable models
The system SHALL allow administrators to control which models appear in user-facing dropdowns.

#### Scenario: Admin disables a model
- **WHEN** admin calls POST /api/admin/models/{id} with enabled=false
- **THEN** system updates the model's enabled status to false
- **THEN** model no longer appears in GET /api/models endpoint

#### Scenario: Admin enables a model
- **WHEN** admin calls POST /api/admin/models/{id} with enabled=true
- **THEN** system updates the model's enabled status to true
- **THEN** model appears in GET /api/models endpoint if its brand is also enabled

### Requirement: Display management UI for brands
The system SHALL provide an administrative interface to view and manage brands.

#### Scenario: Admin views brand management screen
- **WHEN** admin navigates to the brand management page
- **THEN** system displays a table of all brands
- **THEN** table shows name, display_name, enabled status, last_seen date
- **THEN** table provides edit and enable/disable actions for each brand

#### Scenario: Admin searches for brands
- **WHEN** admin types in the brand search box
- **THEN** system filters the brand table to match the search term
- **THEN** search matches against name and display_name fields

#### Scenario: Admin bulk enables brands
- **WHEN** admin selects multiple brands and clicks "Enable Selected"
- **THEN** system enables all selected brands
- **THEN** table refreshes to show updated status

#### Scenario: Admin bulk disables brands
- **WHEN** admin selects multiple brands and clicks "Disable Selected"
- **THEN** system disables all selected brands
- **THEN** table refreshes to show updated status

### Requirement: Display management UI for models
The system SHALL provide an administrative interface to view and manage models.

#### Scenario: Admin views model management screen
- **WHEN** admin navigates to the model management page
- **THEN** system displays a table of all models
- **THEN** table shows brand_name, name, display_name, enabled status, last_seen date
- **THEN** table provides edit and enable/disable actions for each model

#### Scenario: Admin filters models by brand
- **WHEN** admin selects a brand from the filter dropdown
- **THEN** system displays only models for that brand

#### Scenario: Admin bulk enables models
- **WHEN** admin selects multiple models and clicks "Enable Selected"
- **THEN** system enables all selected models
- **THEN** table refreshes to show updated status

#### Scenario: Admin bulk disables models
- **WHEN** admin selects multiple models and clicks "Disable Selected"
- **THEN** system disables all selected models
- **THEN** table refreshes to show updated status

### Requirement: Navigate between brand and model management
The system SHALL provide navigation between brand and model management screens.

#### Scenario: View models for a specific brand from brand list
- **WHEN** admin clicks "View Models" for a brand
- **THEN** system navigates to model management screen
- **THEN** model list is pre-filtered to show only that brand's models
