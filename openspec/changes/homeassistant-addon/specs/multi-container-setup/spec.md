## ADDED Requirements

### Requirement: Multi-container addon structure
The system SHALL use Home Assistant's multi-container addon feature to run backend, frontend, and database as separate Docker containers defined in a docker-compose.yml file.

#### Scenario: Three containers defined
- **WHEN** addon starts
- **THEN** docker-compose.yml SHALL define exactly three services: backend, frontend, and mysql

#### Scenario: Containers start in correct order
- **WHEN** addon starts
- **THEN** mysql container SHALL start first, backend SHALL wait for mysql to be healthy, frontend SHALL start after backend is ready

### Requirement: Backend container configuration
The system SHALL define a backend container based on the existing backend Dockerfile with environment variables populated from addon options.

#### Scenario: Backend uses Python image
- **WHEN** backend container is built
- **THEN** it SHALL use the existing backend/Dockerfile with Python base image

#### Scenario: Backend environment variables
- **WHEN** backend container starts
- **THEN** it SHALL receive environment variables for DATABASE_URL, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE from addon options

#### Scenario: Backend connects to mysql service
- **WHEN** backend initializes database connection
- **THEN** it SHALL connect to hostname 'mysql' on port 3306 using credentials from environment variables

### Requirement: Frontend container configuration
The system SHALL define a frontend container based on the existing frontend Dockerfile with ingress base path configuration.

#### Scenario: Frontend uses nginx image
- **WHEN** frontend container is built
- **THEN** it SHALL use the existing frontend/Dockerfile with nginx base image for serving static files

#### Scenario: Frontend ingress base path
- **WHEN** frontend container starts
- **THEN** it SHALL receive VITE_BASE_URL environment variable set to '/api/hassio_ingress/<token>/'

#### Scenario: Frontend proxies API calls to backend
- **WHEN** frontend makes API requests
- **THEN** nginx SHALL proxy requests to http://backend:5000

### Requirement: MySQL container configuration
The system SHALL define a MySQL container with data persistence in the /data directory.

#### Scenario: MySQL uses official image
- **WHEN** mysql container starts
- **THEN** it SHALL use the official MySQL 8.x image

#### Scenario: MySQL data persistence
- **WHEN** mysql container stores data
- **THEN** data SHALL be persisted to /data/mysql directory on the host

#### Scenario: MySQL root password from options
- **WHEN** mysql container initializes
- **THEN** it SHALL use MYSQL_ROOT_PASSWORD from addon options

#### Scenario: Application database auto-creation
- **WHEN** mysql container starts for the first time
- **THEN** it SHALL automatically create the application database specified in MYSQL_DATABASE environment variable

### Requirement: Container networking
The system SHALL configure internal Docker networking for inter-container communication without exposing backend or database ports to the host.

#### Scenario: Internal network created
- **WHEN** docker-compose starts
- **THEN** it SHALL create an internal network for the three containers

#### Scenario: Backend accessible from frontend
- **WHEN** frontend container makes a request to 'backend:5000'
- **THEN** the request SHALL reach the backend container

#### Scenario: MySQL accessible from backend
- **WHEN** backend container connects to 'mysql:3306'
- **THEN** the connection SHALL reach the mysql container

#### Scenario: Backend port not exposed to host
- **WHEN** addon is running
- **THEN** port 5000 SHALL NOT be accessible from the host network (only via ingress)

### Requirement: Container health checks
The system SHALL define health checks for backend and mysql containers to ensure proper startup order and availability.

#### Scenario: MySQL health check
- **WHEN** mysql container is starting
- **THEN** docker-compose SHALL wait for mysqladmin ping to succeed before marking mysql as healthy

#### Scenario: Backend depends on MySQL health
- **WHEN** backend container is starting
- **THEN** docker-compose SHALL wait for mysql service to be healthy before starting backend

#### Scenario: Backend health check
- **WHEN** backend container is running
- **THEN** docker-compose SHALL periodically check /api/health endpoint to verify backend is responding
