## Why

The occasion-scraper application currently requires manual deployment and management of separate backend (Flask) and frontend (Vue.js) services, along with a MySQL database. Making it available as a Home Assistant addon would enable users to easily install, configure, and manage the application directly from their Home Assistant instance, providing seamless integration with their existing smart home ecosystem.

## What Changes

- Create Home Assistant addon configuration and metadata files
- Package the application as a multi-container addon (backend, frontend, database)
- Add Home Assistant ingress support for the frontend UI
- Configure addon options for database credentials, API keys, and scraping schedules
- Add addon lifecycle management (start, stop, configuration updates)
- Integrate with Home Assistant's authentication and user management
- Add Home Assistant service calls for triggering scrapes and managing blueprints
- Create addon documentation and installation instructions

## Capabilities

### New Capabilities
- `addon-configuration`: Home Assistant addon manifest, configuration schema, and metadata
- `multi-container-setup`: Docker Compose configuration for backend, frontend, and MySQL containers
- `ingress-integration`: Home Assistant ingress proxy configuration for secure frontend access
- `addon-services`: Home Assistant service definitions for programmatic control
- `authentication-integration`: Optional integration with Home Assistant authentication

### Modified Capabilities
<!-- No existing capabilities are being modified at the requirements level -->

## Impact

**New Files:**
- `addon/config.yaml` - Home Assistant addon configuration
- `addon/Dockerfile` - Addon container image (if needed)
- `addon/docker-compose.yml` - Multi-container service definitions
- `addon/run.sh` - Addon startup script
- `addon/DOCS.md` - Addon documentation
- `addon/README.md` - Developer documentation
- `addon/icon.png` - Addon icon
- `addon/logo.png` - Addon logo

**Modified Files:**
- `backend/main.py` - Add support for reading configuration from addon options
- `frontend/vite.config.js` - Configure base path for ingress support
- `docker-compose.yaml` - May need adjustments for addon compatibility

**Dependencies:**
- Home Assistant OS (Supervisor)
- Docker/Container runtime
- Home Assistant version compatibility requirements

**Systems Affected:**
- Deployment process (now via Home Assistant addon store instead of manual)
- Configuration management (now via Home Assistant UI)
- Authentication (optional HA auth integration)
- Network routing (via HA ingress proxy)
