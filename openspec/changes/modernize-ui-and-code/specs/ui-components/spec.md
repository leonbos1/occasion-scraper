## ADDED Requirements

### Requirement: Blueprint cards have consistent sizing
The system SHALL display blueprint cards with fixed widths that remain consistent regardless of the number of cards present.

#### Scenario: Single card display
- **WHEN** only one blueprint exists
- **THEN** the card SHALL display at 320-384px width, not stretched across the screen

#### Scenario: Multiple cards display
- **WHEN** multiple blueprints exist
- **THEN** cards SHALL wrap to multiple rows maintaining consistent 320-384px width

#### Scenario: Mobile responsive display
- **WHEN** viewed on mobile devices (< 640px width)
- **THEN** cards SHALL be full width with appropriate padding

### Requirement: Components use responsive flexbox layout
The system SHALL use flexbox with gap spacing for component layouts instead of fractional width classes.

#### Scenario: Card container layout
- **WHEN** rendering a collection of cards
- **THEN** the container SHALL use `flex flex-wrap justify-center gap-4`

#### Scenario: Individual card sizing
- **WHEN** rendering a single card component
- **THEN** the card SHALL use fixed width classes (w-80, w-96) not fractional (w-1/2, w-1/3)

### Requirement: Loading states are displayed
The system SHALL display loading indicators during asynchronous operations.

#### Scenario: Data fetching
- **WHEN** components are fetching data
- **THEN** a loading spinner or skeleton SHALL be visible

#### Scenario: Form submission
- **WHEN** forms are being submitted
- **THEN** submit buttons SHALL show loading state and be disabled

### Requirement: Error states are handled gracefully
The system SHALL display user-friendly error messages when operations fail.

#### Scenario: API error
- **WHEN** an API request fails
- **THEN** an error message SHALL be displayed explaining what went wrong

#### Scenario: Network error
- **WHEN** network connection is lost
- **THEN** a retry option SHALL be provided to the user

### Requirement: Datetime displays are formatted consistently
The system SHALL display all datetime values in a consistent, user-friendly format.

#### Scenario: Car listing timestamps
- **WHEN** displaying car created/updated times
- **THEN** datetime SHALL be formatted without microseconds (YYYY-MM-DD HH:MM:SS)

#### Scenario: Blueprint timestamps
- **WHEN** displaying blueprint created times
- **THEN** datetime SHALL be formatted consistently with car listings
