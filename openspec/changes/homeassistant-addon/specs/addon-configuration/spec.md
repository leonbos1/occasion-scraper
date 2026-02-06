## ADDED Requirements

### Requirement: Addon manifest file
The system SHALL provide a `config.yaml` file in the addon root directory that defines metadata, configuration options, and runtime requirements according to Home Assistant addon specifications.

#### Scenario: Valid config.yaml structure
- **WHEN** Home Assistant reads the config.yaml file
- **THEN** the file SHALL contain all required fields (name, version, slug, description, arch, startup, boot, ports, ingress)

#### Scenario: Configuration schema validation
- **WHEN** user edits addon configuration in Home Assistant UI
- **THEN** the options SHALL be validated against the schema defined in config.yaml

### Requirement: Database configuration options
The system SHALL expose database root password and application database credentials as configurable options in config.yaml schema.

#### Scenario: Setting MySQL root password
- **WHEN** user sets `mysql_root_password` option
- **THEN** the addon SHALL use this value to initialize the MySQL root user password

#### Scenario: Setting application database credentials
- **WHEN** user sets `db_user`, `db_password`, and `db_name` options
- **THEN** the addon SHALL create the application database with these credentials and configure the backend to use them

### Requirement: Admin user initialization
The system SHALL expose admin user credentials as configurable options in config.yaml schema.

#### Scenario: Setting admin credentials
- **WHEN** user sets `admin_email` and `admin_password` options
- **THEN** the addon SHALL create or update an admin user in the application database with these credentials on startup

#### Scenario: Admin user with role 1
- **WHEN** admin user is created from addon options
- **THEN** the user SHALL have role set to '1' (admin role)

### Requirement: Scraping configuration options
The system SHALL expose scraping-related settings as configurable options in config.yaml schema.

#### Scenario: Configuring scraping interval
- **WHEN** user sets `scrape_interval_minutes` option
- **THEN** the addon SHALL configure the backend to run scraping jobs at the specified interval

#### Scenario: Enabling/disabling scraper sources
- **WHEN** user sets boolean options for each scraper source (e.g., `enable_autoscout`, `enable_marktplaats`)
- **THEN** the addon SHALL configure the backend to only use enabled scrapers

### Requirement: Port and ingress configuration
The system SHALL configure port mappings and ingress settings in config.yaml to expose the frontend UI through Home Assistant.

#### Scenario: Frontend accessible via ingress
- **WHEN** addon is started with `ingress: true` in config.yaml
- **THEN** the frontend UI SHALL be accessible at Home Assistant's ingress path

#### Scenario: Optional direct port access
- **WHEN** user enables `expose_frontend_port` option
- **THEN** the addon SHALL expose the frontend container port to the host network

### Requirement: Addon icon and logo
The system SHALL provide icon.png and logo.png files in the addon root directory for display in Home Assistant UI.

#### Scenario: Icon displayed in addon list
- **WHEN** user views addon in Home Assistant Add-on Store
- **THEN** the icon.png file SHALL be displayed as the addon's icon

#### Scenario: Logo displayed on addon details page
- **WHEN** user opens addon details page
- **THEN** the logo.png file SHALL be displayed at the top of the page
