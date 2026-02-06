# Spec: edit-blueprint

## ADDED Requirements

### Requirement: Load existing brand and model into dropdowns
The system SHALL populate brand and model dropdowns with the blueprint's current values when editing.

#### Scenario: Edit blueprint with catalog brand and model
- **WHEN** user opens edit form for existing blueprint
- **THEN** brand dropdown is pre-selected with blueprint's current brand
- **THEN** model dropdown is enabled and pre-selected with blueprint's current model
- **THEN** both dropdowns display using display_name values

#### Scenario: Edit blueprint with non-catalog brand
- **WHEN** user opens edit form for blueprint with brand not in catalog
- **THEN** brand dropdown shows current brand value as custom option marked "(custom - not in catalog)"
- **THEN** user can keep custom value or select a catalog brand
- **THEN** model dropdown remains disabled until catalog brand is selected

### Requirement: Allow changing brand selection
The system SHALL allow users to change the brand when editing a blueprint.

#### Scenario: Change brand to different catalog brand
- **WHEN** user selects a different brand from dropdown
- **THEN** model dropdown is cleared
- **THEN** model dropdown is repopulated with models for newly selected brand
- **THEN** user must select a new model

#### Scenario: Preserve model if changing brand with same model
- **WHEN** user changes brand to one that has the same model slug
- **THEN** model dropdown is repopulated
- **THEN** previous model is pre-selected if it exists for new brand
- **THEN** if model doesn't exist for new brand, dropdown is cleared

### Requirement: Allow changing model selection
The system SHALL allow users to change the model when editing a blueprint.

#### Scenario: Change model to different catalog model
- **WHEN** user selects a different model from dropdown
- **THEN** form updates with new model selection
- **THEN** new model slug is stored for submission

### Requirement: Update blueprint with slug values
The system SHALL submit updated slug values when saving edited blueprint.

#### Scenario: Save edited blueprint with new selections
- **WHEN** user submits the edit form with changed brand or model
- **THEN** system submits brand slug to backend
- **THEN** system submits model slug to backend
- **THEN** backend updates blueprint with new slug values
- **THEN** updated blueprint works with existing scraper logic

### Requirement: Validate dropdown selections before save
The system SHALL validate that required dropdown fields are selected before allowing save.

#### Scenario: Attempt to save without brand selection
- **WHEN** user clears brand selection and attempts to save
- **THEN** system displays validation error "Brand is required"
- **THEN** system prevents form submission

#### Scenario: Attempt to save without model selection
- **WHEN** user clears model selection and attempts to save
- **THEN** system displays validation error "Model is required"
- **THEN** system prevents form submission

### Requirement: Preserve custom values if not changed
The system SHALL preserve non-catalog brand/model values when editing other blueprint fields.

#### Scenario: Edit blueprint fields without changing custom brand/model
- **WHEN** user edits a blueprint with custom brand/model values
- **WHEN** user changes other fields (like search filters) but not brand/model
- **WHEN** user saves the form
- **THEN** system preserves the original custom brand/model values
- **THEN** system does not force user to select catalog values
