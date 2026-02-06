## Context

The occasion-scraper application is a full-stack web application consisting of:
- **Backend**: Python Flask REST API with SQLAlchemy ORM
- **Frontend**: Vue.js 3 SPA with Vite build system
- **Database**: MySQL for persistent storage

Currently, deployment requires:
1. Manual setup of three separate services (backend, frontend, database)
2. Configuration file editing for connection strings and API keys
3. Reverse proxy setup for frontend access
4. Independent management of each service

Home Assistant OS provides an addon system that allows containerized applications to run within the Home Assistant ecosystem. Addons can:
- Use Home Assistant's Supervisor API for configuration management
- Integrate with Home Assistant's ingress proxy for secure web UI access
- Expose services for automation and integration
- Use persistent storage in `/data` directory
- Access Home Assistant's authentication system

## Goals / Non-Goals

**Goals:**
- Package the entire application stack as a single Home Assistant addon
- Enable users to install and configure the addon through the Home Assistant UI
- Provide frontend access through Home Assistant ingress (embedded in HA UI)
- Support configuration of database credentials, scraping schedules, and API settings via addon options
- Maintain feature parity with standalone deployment
- Ensure data persistence across addon restarts

**Non-Goals:**
- Rewriting application code to use Home Assistant Core APIs (maintain standalone compatibility)
- Deep integration with Home Assistant entities (sensors, switches) - this could be a future enhancement
- Supporting external MySQL instances (addon will bundle its own database)
- Custom authentication integration with Home Assistant (use existing token-based auth for now)

## Decisions

### Decision 1: Multi-Container Addon Architecture

**Choice**: Use Home Assistant's multi-container addon feature with separate containers for backend, frontend, and database.

**Rationale**: 
- Separation of concerns - each service has its own Dockerfile and configuration
- Easier to debug and maintain individual components
- Allows different base images (Python for backend, nginx for frontend, MySQL for database)
- Aligns with existing docker-compose.yaml structure

**Alternatives Considered**:
- Single container with all services: Would require complex process management (supervisord), harder to maintain, larger image size
- Backend+frontend in one container, separate DB: Still requires process management, doesn't align with existing structure

### Decision 2: Ingress for Frontend Access

**Choice**: Configure Home Assistant ingress to proxy requests to the frontend container, embedding the UI in the Home Assistant interface.

**Rationale**:
- Users access the application at `http://homeassistant.local:8123/api/hassio_ingress/<token>/`
- No need to expose additional ports on the host
- Automatic SSL/TLS if Home Assistant is configured for it
- Follows Home Assistant addon best practices

**Alternatives Considered**:
- Port mapping: Would require exposing frontend port (e.g., 8080), less secure, requires manual port management
- Web link only: No embedded UI, worse user experience

### Decision 3: Configuration Management via Addon Options

**Choice**: Define configuration schema in `config.yaml` and read options from `/data/options.json` at runtime.

**Rationale**:
- Home Assistant UI provides form-based configuration editing
- Changes persist across restarts
- Validation happens at the addon configuration layer
- Environment variables can be populated from options.json in the startup script

**Alternatives Considered**:
- Environment variables in docker-compose: Would require rebuilding addon to change config
- Config files mounted from /config: Less user-friendly, requires manual file editing

### Decision 4: Database Persistence Strategy

**Choice**: Store MySQL data in `/data/mysql` directory using Home Assistant's persistent storage.

**Rationale**:
- `/data` directory is automatically persisted across addon updates and restarts
- No need for named volumes or host path mounts
- Backup/restore handled by Home Assistant's backup system

**Alternatives Considered**:
- Named Docker volume: Not compatible with Home Assistant addon architecture
- Host path mount: Would require user to manually configure paths

### Decision 5: Startup Script Approach

**Choice**: Create `run.sh` script that:
1. Reads `/data/options.json`
2. Generates `.env` files for backend and frontend
3. Starts docker-compose with generated configuration

**Rationale**:
- Allows dynamic configuration without rebuilding images
- Centralizes configuration logic
- Can perform pre-flight checks (database initialization, migrations)

**Alternatives Considered**:
- Entrypoint scripts in each Dockerfile: Would duplicate logic, harder to coordinate
- Direct docker-compose up: No opportunity to inject configuration from addon options

### Decision 6: Network Configuration

**Choice**: Use docker-compose internal networking with service names for inter-container communication. Frontend ingress path configured via VITE_BASE_URL environment variable.

**Rationale**:
- Backend accessible at `http://backend:5000` from frontend container
- MySQL accessible at `mysql:3306` from backend container
- No need to expose backend/database ports to host
- Ingress path `/api/hassio_ingress/<token>/` handled by Vite base configuration

**Alternatives Considered**:
- Host networking: Would expose all ports, less secure, conflicts with existing services
- Bridge networking with published ports: Unnecessary complexity, ingress already provides access

## Risks / Trade-offs

**Risk**: Ingress path changes could break frontend routing  
→ **Mitigation**: Configure Vite with dynamic base path support, test with various ingress tokens

**Risk**: Addon updates might not trigger database migrations automatically  
→ **Mitigation**: Include migration check in run.sh startup script, log migration status

**Risk**: Large MySQL data directory could impact addon backup size  
→ **Mitigation**: Document backup size expectations, recommend periodic cleanup of old scrape data

**Risk**: Docker-compose inside Docker (DinD) complexity  
→ **Mitigation**: Use bind mounts instead of volumes where possible, follow Home Assistant multi-container addon examples

**Trade-off**: Bundled MySQL means no shared database with other addons  
→ **Accepted**: Simpler setup, better isolation, acceptable for this use case

**Trade-off**: Ingress adds slight latency compared to direct port access  
→ **Accepted**: Minimal impact, security and UX benefits outweigh performance cost

## Migration Plan

**For New Installations:**
1. User adds addon repository URL to Home Assistant
2. Navigates to Add-on Store, installs "Occasion Scraper"
3. Configures addon options (admin password, scraping schedule)
4. Starts addon
5. Accesses UI via Sidebar link

**For Existing Standalone Deployments:**
1. Export data using existing backup scripts (if any)
2. Install addon
3. Access addon's MySQL container and import data (documented procedure)
4. Verify data migration successful
5. Stop standalone deployment

**Rollback Strategy:**
- Addon version pinning available in Home Assistant
- `/data` directory preserved across addon uninstall/reinstall
- If addon fails, users can revert to standalone deployment using same data backup

## Open Questions

1. **Admin user initialization**: Should the addon create a default admin user with a configured password, or require manual user creation on first launch?
   - **Proposed answer**: Create default admin user with password from addon options for better UX

2. **Scraping schedule**: Should scraping be triggered via Home Assistant automation or via addon's built-in scheduler?
   - **Proposed answer**: Keep built-in scheduler for standalone compatibility, but also expose Home Assistant service for automation integration

3. **Log access**: How should users access application logs?
   - **Proposed answer**: Use Home Assistant's built-in addon log viewer (stdout/stderr), ensure application logs to console

4. **SSL certificates**: Should addon support custom SSL cert configuration for external API calls?
   - **Proposed answer**: Use system certificates by default, add option for custom cert path if needed in future iteration
