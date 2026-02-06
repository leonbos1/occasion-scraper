## 1. Addon Configuration Files

- [x] 1.1 Create addon/config.yaml with metadata (name, version, slug, description, arch)
- [x] 1.2 Define addon options schema in config.yaml (mysql credentials, admin user, scraping settings)
- [x] 1.3 Configure startup, boot, ports, and ingress settings in config.yaml
- [x] 1.4 Define Home Assistant services in config.yaml (trigger_scrape, get_scrape_status, list_cars, get_car_details)
- [x] 1.5 Create addon/icon.png (256x256 image for addon store)
- [x] 1.6 Create addon/logo.png (larger image for addon details page)
- [x] 1.7 Create addon/DOCS.md with user-facing documentation
- [x] 1.8 Create addon/README.md with developer documentation

## 2. Multi-Container Setup

- [x] 2.1 Create addon/docker-compose.yml with three services (backend, frontend, mysql)
- [x] 2.2 Configure mysql service with official MySQL 8.x image
- [x] 2.3 Configure mysql data volume mount to /data/mysql
- [x] 2.4 Configure mysql environment variables (MYSQL_ROOT_PASSWORD, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD)
- [x] 2.5 Add mysql healthcheck using mysqladmin ping command
- [x] 2.6 Configure backend service based on backend/Dockerfile
- [x] 2.7 Configure backend environment variables from addon options
- [x] 2.8 Add backend dependency on mysql service health
- [x] 2.9 Add backend healthcheck using /api/health endpoint
- [x] 2.10 Configure frontend service based on frontend/Dockerfile
- [x] 2.11 Configure frontend environment variables (VITE_BASE_URL, VITE_API_URL)
- [x] 2.12 Add frontend dependency on backend service
- [x] 2.13 Create internal Docker network for inter-container communication
- [x] 2.14 Expose frontend port for ingress (but not to host network)

## 3. Startup Script

- [x] 3.1 Create addon/run.sh with executable permissions
- [x] 3.2 Add logic to read /data/options.json in run.sh
- [x] 3.3 Add logic to generate backend .env file from options
- [x] 3.4 Add logic to generate frontend .env file from options
- [x] 3.5 Add logic to export docker-compose environment variables
- [x] 3.6 Add database initialization check (wait for mysql to be ready)
- [x] 3.7 Add logic to create/update admin user from addon options
- [x] 3.8 Add database migration check and execution
- [x] 3.9 Add docker-compose up command with --build flag
- [x] 3.10 Add logging of startup progress to stdout

## 4. Backend Modifications

- [x] 4.1 Add /api/health endpoint to backend/main.py for healthcheck
- [x] 4.2 Modify backend/main.py to read configuration from environment variables
- [x] 4.3 Update DATABASE_URL construction to use env vars (MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_HOST)
- [x] 4.4 Add script to create/update admin user from environment variables
- [x] 4.5 Ensure backend runs database migrations on startup
- [ ] 4.6 Test backend healthcheck endpoint returns 200 OK

## 5. Frontend Modifications

- [x] 5.1 Update frontend/vite.config.js to use VITE_BASE_URL environment variable for base path
- [x] 5.2 Update frontend/src/main.js router to use base path from import.meta.env.VITE_BASE_URL
- [x] 5.3 Update frontend API calls to use VITE_API_URL from environment
- [x] 5.4 Update frontend/dockerfile to accept build-time VITE_BASE_URL argument
- [ ] 5.5 Test frontend routing works with ingress base path
- [ ] 5.6 Test frontend API calls work through ingress proxy

## 6. Database Modifications

- [x] 6.1 Create database initialization script for first-time setup
- [x] 6.2 Add logic to create application database if not exists
- [x] 6.3 Add logic to create application user with configured credentials
- [ ] 6.4 Test database persistence across container restarts
- [ ] 6.5 Test database accessible from backend using internal docker network

## 7. Addon Services Implementation

- [x] 7.1 Create addon service handler script (addon/services.py or equivalent)
- [x] 7.2 Implement trigger_scrape service to call backend API
- [x] 7.3 Implement get_scrape_status service to query backend API
- [x] 7.4 Implement list_cars service to query backend API with filters
- [x] 7.5 Implement get_car_details service to query backend API
- [x] 7.6 Add service call logging for debugging
- [ ] 7.7 Test each service call from Home Assistant Services UI

## 8. Ingress Configuration

- [x] 8.1 Verify ingress: true is set in config.yaml
- [x] 8.2 Verify ingress_port matches frontend container port in docker-compose.yml
- [ ] 8.3 Test frontend accessible via Home Assistant ingress URL
- [ ] 8.4 Test frontend assets load correctly with ingress base path
- [ ] 8.5 Test Vue router navigation works under ingress path
- [ ] 8.6 Test API calls from frontend work through ingress
- [ ] 8.7 Test authentication flow works with ingress

## 9. Authentication Integration

- [x] 9.1 Add enable_ha_auth option to config.yaml schema (default: false)
- [x] 9.2 Ensure admin user auto-creation logic runs on every startup
- [ ] 9.3 Test admin user created with credentials from addon options
- [ ] 9.4 Test admin user password updates when option changes
- [ ] 9.5 Test admin user has role '1' (admin role)
- [ ] 9.6 Test additional users can be created via UI
- [ ] 9.7 Test authentication tokens persist across addon restarts
- [x] 9.8 Document that HA auth integration is planned for future release

## 10. Documentation

- [x] 10.1 Write addon/DOCS.md with installation instructions
- [x] 10.2 Document configuration options with examples in DOCS.md
- [x] 10.3 Document Home Assistant services usage in DOCS.md
- [x] 10.4 Add troubleshooting section to DOCS.md
- [x] 10.5 Write addon/README.md for developers
- [x] 10.6 Document addon architecture and file structure in README.md
- [x] 10.7 Document how to build and test addon locally
- [x] 10.8 Update main project README.md with addon installation option

## 11. Testing

- [ ] 11.1 Test fresh addon installation from scratch
- [ ] 11.2 Test addon configuration changes via Home Assistant UI
- [ ] 11.3 Test addon restart preserves data and configuration
- [ ] 11.4 Test all scraper functionality works via addon
- [ ] 11.5 Test brand/model management via addon UI
- [ ] 11.6 Test user creation and authentication via addon UI
- [ ] 11.7 Test Home Assistant services from automations
- [ ] 11.8 Test addon update (simulated version bump)
- [ ] 11.9 Test addon uninstall and reinstall
- [ ] 11.10 Test database backup and restore via Home Assistant

## 12. Deployment Preparation

- [x] 12.1 Create GitHub repository for addon (or add to existing repo)
- [x] 12.2 Set up versioning scheme (follow semantic versioning)
- [x] 12.3 Create CHANGELOG.md documenting version history
- [x] 12.4 Add .gitignore for addon-specific files
- [ ] 12.5 Create release workflow (if using GitHub Actions)
- [x] 12.6 Document how to add addon repository URL to Home Assistant
- [ ] 12.7 Test addon installation from custom repository URL
- [ ] 12.8 (Optional) Submit addon to Home Assistant Community Add-ons repository
