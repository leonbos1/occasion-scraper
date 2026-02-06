## ADDED Requirements

### Requirement: Scraper extracts car data from listing pages
The system SHALL extract all car information directly from listing page article elements without navigating to detail pages.

#### Scenario: Car ID extraction
- **WHEN** parsing a listing page
- **THEN** car IDs SHALL be extracted from article data-guid attributes

#### Scenario: Car URL construction
- **WHEN** a car ID is available
- **THEN** the URL SHALL be constructed as `/offers/{car_id}`

#### Scenario: Location extraction with fallback
- **WHEN** parsing car location data
- **THEN** the system SHALL attempt to parse from SellerInfo_address span and fall back to last span element if unavailable

### Requirement: Images are fetched from listing page
The system SHALL extract car images directly from the listing page picture elements.

#### Scenario: Picture element parsing
- **WHEN** parsing a car article
- **THEN** the system SHALL locate the picture element and extract the img src attribute

#### Scenario: Image URL validation
- **WHEN** an image URL is found
- **THEN** it SHALL only be fetched if it matches the pattern `prod.pictures.autoscout24.net/listing-images`

#### Scenario: Image fetch failure handling
- **WHEN** image fetching fails
- **THEN** the system SHALL return empty bytes (b"") and log the error without crashing

### Requirement: Scraper handles HTML structure changes gracefully
The system SHALL use flexible selectors that tolerate HTML structure changes.

#### Scenario: Element type selection
- **WHEN** searching for elements
- **THEN** selectors SHALL prioritize element types (article, picture, img) over specific class names

#### Scenario: Multiple fallback strategies
- **WHEN** primary selector fails
- **THEN** the system SHALL attempt alternative selectors before returning default values

#### Scenario: Parsing failure logging
- **WHEN** data extraction fails
- **THEN** the system SHALL log the failure with context for debugging

### Requirement: Datetime values are compatible with database
The system SHALL create datetime objects without microseconds to prevent database truncation errors.

#### Scenario: Session creation timestamp
- **WHEN** creating a scrape session
- **THEN** created and updated timestamps SHALL have microseconds removed via replace(microsecond=0)

#### Scenario: Car creation timestamp
- **WHEN** creating a car record
- **THEN** BaseModel SHALL ensure timestamps have no microseconds

### Requirement: Scraper returns empty data gracefully
The system SHALL return empty collections instead of None when no data is found.

#### Scenario: No cars found on page
- **WHEN** a listing page has no article elements
- **THEN** the scraper SHALL return an empty list []

#### Scenario: Page fetch failure
- **WHEN** HTTP request returns non-200 status
- **THEN** the scraper SHALL log error and return empty list
