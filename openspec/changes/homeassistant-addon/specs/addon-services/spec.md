## ADDED Requirements

### Requirement: Addon services manifest
The system SHALL define Home Assistant services in config.yaml that allow users to trigger scraping and manage data via Home Assistant automations.

#### Scenario: Service definitions in config.yaml
- **WHEN** addon is installed
- **THEN** config.yaml SHALL define services under the `services:` key

#### Scenario: Services appear in Home Assistant
- **WHEN** addon is started
- **THEN** the defined services SHALL be available in Home Assistant's Services developer tool

### Requirement: Trigger scrape service
The system SHALL provide a `trigger_scrape` service that initiates a scraping session for all enabled scrapers.

#### Scenario: Service accepts scraper list parameter
- **WHEN** user calls `trigger_scrape` service with `scrapers` parameter
- **THEN** the addon SHALL start scraping jobs for the specified scrapers

#### Scenario: Service defaults to all enabled scrapers
- **WHEN** user calls `trigger_scrape` service without parameters
- **THEN** the addon SHALL start scraping jobs for all scrapers enabled in addon options

#### Scenario: Service returns job ID
- **WHEN** scraping is triggered via service
- **THEN** the service SHALL return a scrape session ID that can be used to track progress

### Requirement: Get scrape status service
The system SHALL provide a `get_scrape_status` service that returns the current status of a scraping session.

#### Scenario: Service accepts session ID parameter
- **WHEN** user calls `get_scrape_status` service with `session_id` parameter
- **THEN** the addon SHALL return the status, progress, and results of the specified scrape session

#### Scenario: Service returns completed session data
- **WHEN** user queries a completed scrape session
- **THEN** the service SHALL return total cars scraped, duration, and any errors

### Requirement: List cars service
The system SHALL provide a `list_cars` service that returns a list of cars matching filter criteria.

#### Scenario: Service accepts filter parameters
- **WHEN** user calls `list_cars` service with parameters like `brand`, `model`, `max_price`
- **THEN** the addon SHALL return a list of cars matching all specified filters

#### Scenario: Service limits result count
- **WHEN** user calls `list_cars` service
- **THEN** the addon SHALL return a maximum of 100 results by default, configurable via `limit` parameter

### Requirement: Get car details service
The system SHALL provide a `get_car_details` service that returns detailed information about a specific car.

#### Scenario: Service accepts car ID parameter
- **WHEN** user calls `get_car_details` service with `car_id` parameter
- **THEN** the addon SHALL return all stored information about the car including price, mileage, images, and source URL

#### Scenario: Service handles non-existent car
- **WHEN** user requests details for a car ID that doesn't exist
- **THEN** the service SHALL return an error indicating the car was not found

### Requirement: Service call authorization
The system SHALL require Home Assistant authentication for all service calls, but SHALL NOT enforce application-level role checking for service calls.

#### Scenario: Authenticated HA user can call services
- **WHEN** an authenticated Home Assistant user calls an addon service
- **THEN** the service SHALL execute successfully

#### Scenario: Unauthenticated user cannot call services
- **WHEN** an unauthenticated user attempts to call an addon service
- **THEN** Home Assistant SHALL reject the call before it reaches the addon
