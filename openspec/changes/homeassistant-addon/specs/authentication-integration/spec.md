## ADDED Requirements

### Requirement: Existing authentication preserved
The system SHALL continue to use the application's existing token-based authentication system and SHALL NOT require integration with Home Assistant's authentication for application access.

#### Scenario: Login with application credentials
- **WHEN** user accesses the addon UI via ingress
- **THEN** they SHALL be required to log in with application credentials (email/password)

#### Scenario: Token stored in browser
- **WHEN** user successfully logs in
- **THEN** the authentication token SHALL be stored in localStorage for subsequent requests

#### Scenario: Admin role required for admin features
- **WHEN** user with role !== '1' attempts to access admin features
- **THEN** the application SHALL deny access and show unauthorized message

### Requirement: Admin user auto-creation
The system SHALL create or update the admin user specified in addon options on every startup.

#### Scenario: Admin user created on first startup
- **WHEN** addon starts for the first time
- **THEN** it SHALL create an admin user with email and password from addon options

#### Scenario: Admin password updated on startup
- **WHEN** addon starts and admin user already exists
- **THEN** it SHALL update the admin user's password to match the current addon option value

#### Scenario: Admin user has role 1
- **WHEN** admin user is created or updated
- **THEN** the user SHALL have role set to '1' to grant admin access

### Requirement: Multiple user support
The system SHALL allow creation of additional non-admin users through the application UI, independent of addon configuration.

#### Scenario: Creating additional users via UI
- **WHEN** admin user creates a new user through the application UI
- **THEN** the new user SHALL be stored in the database with their specified role

#### Scenario: Non-admin users cannot access admin features
- **WHEN** a user with role !== '1' accesses the UI
- **THEN** they SHALL NOT see admin menu items or be able to access admin routes

### Requirement: Session persistence across restarts
The system SHALL preserve user authentication tokens and sessions across addon restarts as long as the tokens have not expired.

#### Scenario: Valid token works after restart
- **WHEN** user has a valid authentication token and addon restarts
- **THEN** the token SHALL remain valid and user SHALL stay logged in

#### Scenario: Expired token requires re-login
- **WHEN** user's authentication token expires
- **THEN** they SHALL be redirected to the login page

### Requirement: Optional Home Assistant auth integration
The system SHALL provide a configuration option to enable experimental Home Assistant authentication integration as a future enhancement, but SHALL default to disabled.

#### Scenario: HA auth disabled by default
- **WHEN** addon is installed
- **THEN** the `enable_ha_auth` option SHALL default to false

#### Scenario: Application auth used when HA auth disabled
- **WHEN** `enable_ha_auth` is false
- **THEN** the application SHALL use its token-based authentication system

#### Scenario: Documentation notes future HA auth support
- **WHEN** user reads addon documentation
- **THEN** it SHALL mention that Home Assistant authentication integration is planned for a future release
