## ADDED Requirements

### Requirement: Ingress proxy configuration
The system SHALL configure Home Assistant ingress to proxy requests from the Home Assistant UI to the frontend container.

#### Scenario: Ingress enabled in config
- **WHEN** addon config.yaml has `ingress: true`
- **THEN** Home Assistant SHALL create an ingress proxy endpoint for the addon

#### Scenario: Ingress panel in sidebar
- **WHEN** ingress is enabled
- **THEN** Home Assistant SHALL display an addon entry in the sidebar navigation

#### Scenario: Ingress URL pattern
- **WHEN** user clicks the addon sidebar entry
- **THEN** they SHALL be navigated to `/api/hassio_ingress/<unique-token>/`

### Requirement: Frontend base path configuration
The system SHALL configure the Vue.js frontend to work correctly under the ingress base path.

#### Scenario: Vite base configuration
- **WHEN** frontend is built
- **THEN** vite.config.js SHALL be configured to use the VITE_BASE_URL environment variable as the base path

#### Scenario: Router base path
- **WHEN** Vue Router initializes
- **THEN** it SHALL use the ingress base path for all route navigation

#### Scenario: Asset paths
- **WHEN** frontend loads static assets (CSS, JS, images)
- **THEN** asset paths SHALL be relative to the ingress base path

### Requirement: API request proxying
The system SHALL configure the frontend to make API requests through the ingress proxy to the backend container.

#### Scenario: API base URL configuration
- **WHEN** frontend makes API requests
- **THEN** it SHALL use the VITE_API_URL environment variable pointing to the backend service

#### Scenario: CORS not required
- **WHEN** frontend and backend are accessed through ingress
- **THEN** CORS configuration SHALL NOT be needed because all requests appear to come from the same origin

### Requirement: Ingress authentication passthrough
The system SHALL leverage Home Assistant's ingress authentication to ensure only authenticated Home Assistant users can access the addon UI.

#### Scenario: Unauthenticated access blocked
- **WHEN** an unauthenticated user attempts to access the ingress URL
- **THEN** Home Assistant SHALL redirect them to the login page

#### Scenario: Authenticated access granted
- **WHEN** an authenticated Home Assistant user accesses the ingress URL
- **THEN** the frontend UI SHALL load successfully

### Requirement: Ingress port mapping
The system SHALL configure docker-compose to expose the frontend container port for ingress to connect to.

#### Scenario: Frontend port exposed to ingress
- **WHEN** ingress proxies requests to the addon
- **THEN** it SHALL connect to the frontend container on the configured port (default 80)

#### Scenario: Frontend port not exposed to host
- **WHEN** addon is running with ingress only
- **THEN** the frontend port SHALL NOT be published to the host network
