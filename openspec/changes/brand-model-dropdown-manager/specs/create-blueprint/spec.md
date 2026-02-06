# Spec: create-blueprint

## ADDED Requirements

### Requirement: Replace brand text input with dropdown
The system SHALL replace the brand text input field with a searchable dropdown populated from the brand catalog.

#### Scenario: Display brand dropdown on form load
- **WHEN** user opens the blueprint creation form
- **THEN** brand field displays as a searchable dropdown
- **THEN** dropdown is populated with enabled brands from GET /api/brands
- **THEN** brands are displayed using display_name values

#### Scenario: User selects brand from dropdown
- **WHEN** user clicks on the brand dropdown
- **THEN** dropdown displays all enabled brands
- **WHEN** user clicks a brand option
- **THEN** brand field is populated with selected brand's display_name
- **THEN** brand slug is stored for form submission
- **THEN** model dropdown becomes enabled

### Requirement: Replace model text input with dropdown
The system SHALL replace the model text input field with a searchable dropdown populated based on selected brand.

#### Scenario: Display model dropdown after brand selection
- **WHEN** user selects a brand
- **THEN** model dropdown is enabled
- **THEN** dropdown is populated with enabled models for selected brand from GET /api/models?brand_slug={slug}
- **THEN** models are displayed using display_name values

#### Scenario: Model dropdown disabled when no brand selected
- **WHEN** user has not selected a brand
- **THEN** model dropdown is disabled
- **THEN** dropdown shows placeholder "Select a brand first"

#### Scenario: User changes brand selection
- **WHEN** user changes the selected brand
- **THEN** model dropdown is cleared
- **THEN** model dropdown is repopulated with models for new brand

### Requirement: Submit slug values to backend
The system SHALL submit slug values rather than display names when creating a blueprint.

#### Scenario: Create blueprint with selected brand and model
- **WHEN** user submits the blueprint creation form
- **THEN** system submits brand slug (not display_name) to backend
- **THEN** system submits model slug (not display_name) to backend
- **THEN** backend receives slug values compatible with existing scraper logic

### Requirement: Maintain backward compatibility with existing blueprints
The system SHALL continue to work with blueprints created before dropdown implementation.

#### Scenario: Display existing blueprint with text values
- **WHEN** system loads an existing blueprint that has brand/model as text values
- **THEN** system attempts to match text values to brands/models in catalog
- **THEN** if match found, dropdown shows the corresponding display_name
- **THEN** if no match found, system displays the original text value with warning "Not in catalog"

#### Scenario: Edit existing blueprint with non-catalog values
- **WHEN** user edits a blueprint with brand/model not in catalog
- **THEN** brand dropdown shows current value as custom option marked "(custom)"
- **THEN** user can select a catalog value to replace it
- **THEN** if user submits without changing, custom value is preserved
