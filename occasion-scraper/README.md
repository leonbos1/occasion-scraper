# Occasion Scraper - Home Assistant Addon (Developer Documentation)

This document provides technical details for developers working on the Occasion Scraper Home Assistant addon.

## Architecture

The addon uses a **multi-container architecture** with three services:

```
┌─────────────────────────────────────────┐
│     Home Assistant (Ingress Proxy)      │
└──────────────┬──────────────────────────┘
               │ HTTP
┌──────────────▼──────────────────────────┐
│          Frontend (Vue.js)               │
│     - Nginx serving static files         │
│     - Port 80 (ingress only)            │
└──────────────┬──────────────────────────┘
               │ HTTP (internal)
┌──────────────▼──────────────────────────┐
│          Backend (Flask)                 │
│     - Python REST API                    │
│     - SQLAlchemy ORM                     │
│     - Port 5000 (internal only)         │
└──────────────┬──────────────────────────┘
               │ MySQL protocol
┌──────────────▼──────────────────────────┐
│          MySQL 8.x                       │
│     - Persistent storage in /data       │
│     - Port 3306 (internal only)         │
└─────────────────────────────────────────┘
```

## Directory Structure

```
addon/
├── config.yaml           # Addon manifest and configuration schema
├── docker-compose.yml    # Multi-container service definitions
├── run.sh               # Startup script (reads options, starts services)
├── services.py          # Home Assistant service handlers
├── init_db.sh           # Database initialization script
├── DOCS.md              # User-facing documentation
├── README.md            # This file (developer documentation)
├── icon.png             # Addon icon (256x256)
├── logo.png             # Addon logo (1024x1024)
└── CHANGELOG.md         # Version history
```

## Configuration Flow

1. **User configures addon** via Home Assistant UI
2. **Home Assistant writes** `/data/options.json` with configuration
3. **run.sh reads** `/data/options.json` at startup
4. **Environment variables set** for backend and frontend containers
5. **docker-compose starts** all three containers with config
6. **Backend reads** env vars and configures database connection
7. **Frontend builds** with ingress base path from env vars

## Environment Variables

### Backend Container

- `MYSQL_HOST`: Hostname of MySQL container (default: `mysql`)
- `MYSQL_DATABASE`: Application database name
- `MYSQL_USER`: Application database user
- `MYSQL_PASSWORD`: Application database password
- `ADMIN_EMAIL`: Admin user email for auto-creation
- `ADMIN_PASSWORD`: Admin user password for auto-creation
- `SCRAPE_INTERVAL`: Scraping interval in minutes
- `ENABLE_AUTOSCOUT`: Boolean for AutoScout24 scraper
- `ENABLE_MARKTPLAATS`: Boolean for Marktplaats scraper
- `ENABLE_ANWB`: Boolean for ANWB scraper
- `ENABLE_GASPEDAAL`: Boolean for Gaspedaal scraper

### Frontend Container

- `VITE_BASE_URL`: Base path for ingress (e.g., `/api/hassio_ingress/<token>/`)
- `VITE_API_URL`: Backend API URL (default: `http://backend:5000`)

### MySQL Container

- `MYSQL_ROOT_PASSWORD`: Root password from addon options
- `MYSQL_DATABASE`: Application database name
- `MYSQL_USER`: Application database user
- `MYSQL_PASSWORD`: Application database password

## Service Handlers

The addon exposes Home Assistant services via stdin. The `services.py` script:

1. Reads JSON from stdin
2. Parses service name and parameters
3. Makes HTTP requests to backend API
4. Returns results as JSON to stdout

### Service Format

```json
{
  "service": "trigger_scrape",
  "scrapers": ["autoscout", "marktplaats"]
}
```

### Backend API Endpoints Used

- `POST /api/scrape` - Trigger scraping
- `GET /api/scrape-sessions/:id` - Get scrape status
- `GET /api/cars` - List cars with filters
- `GET /api/cars/:id` - Get car details

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Home Assistant OS test environment (or Home Assistant in Docker)
- Git

### Local Testing (Without Home Assistant)

```bash
# Clone repository
git clone https://github.com/leonbos1/occasion-scraper.git
cd occasion-scraper

# Create test options.json
mkdir -p /data
cat > /data/options.json << EOF
{
  "mysql_root_password": "test_root",
  "db_name": "occasion_scraper",
  "db_user": "scraper",
  "db_password": "test_db",
  "admin_email": "admin@test.com",
  "admin_password": "test_admin",
  "scrape_interval_minutes": 60,
  "enable_autoscout": true,
  "enable_marktplaats": true,
  "enable_anwb": false,
  "enable_gaspedaal": false
}
EOF

# Run startup script
cd addon
chmod +x run.sh
./run.sh
```

### Testing in Home Assistant

1. Set up Home Assistant OS in a VM or dedicated device
2. Enable SSH addon for file access
3. Copy addon directory to `/addons/occasion-scraper/`
4. Reload addon list in Home Assistant
5. Install and configure the addon

### Building Images

The frontend and backend containers are built from existing Dockerfiles:

```bash
# Backend
cd backend
docker build -t occasion-scraper-backend .

# Frontend
cd frontend
docker build -t occasion-scraper-frontend \
  --build-arg VITE_BASE_URL=/ \
  --build-arg VITE_API_URL=http://localhost:5000 .
```

## Database Migrations

Database migrations are handled by the backend on startup. The backend checks for pending migrations and applies them automatically.

Migration files are located in `backend/migrations/` (if using Flask-Migrate) or applied via SQLAlchemy's `create_all()` method.

## Debugging

### View Logs

```bash
# From Home Assistant UI
Settings → Add-ons → Occasion Scraper → Logs

# From SSH
docker logs addon_occasion-scraper
```

### Access Container Shells

```bash
# Backend
docker exec -it addon_occasion-scraper_backend_1 /bin/bash

# Frontend
docker exec -it addon_occasion-scraper_frontend_1 /bin/sh

# MySQL
docker exec -it addon_occasion-scraper_mysql_1 /bin/bash
mysql -u root -p
```

### Check Database

```bash
docker exec -it addon_occasion-scraper_mysql_1 mysql -u scraper -p
# Enter db_password when prompted
USE occasion_scraper;
SHOW TABLES;
SELECT COUNT(*) FROM cars;
```

## Release Process

1. Update version in `addon/config.yaml`
2. Update `addon/CHANGELOG.md`
3. Commit changes: `git commit -m "Release v1.x.x"`
4. Tag release: `git tag -a v1.x.x -m "Version 1.x.x"`
5. Push: `git push && git push --tags`
6. Users will see update notification in Home Assistant

## Testing Checklist

Before releasing a new version:

- [ ] Fresh installation works
- [ ] Addon starts without errors
- [ ] Web UI accessible via ingress
- [ ] Admin login works with configured credentials
- [ ] Database persists across restarts
- [ ] Scraping functionality works
- [ ] Brand/model catalog building works
- [ ] Home Assistant services respond correctly
- [ ] Addon configuration changes apply correctly
- [ ] Addon survives Home Assistant restart
- [ ] Backup and restore preserves data

## Common Issues

### Port Conflicts

If port 80 is already in use, the frontend container won't start. Check `docker ps` for conflicts.

### Database Connection Errors

Ensure MySQL container is healthy before backend starts. Check `docker-compose.yml` for proper `depends_on` and `healthcheck` configuration.

### Ingress Path Issues

Frontend must be built with correct `VITE_BASE_URL`. If assets fail to load, check that the base path matches Home Assistant's ingress path.

### Service Not Found

Home Assistant services are registered via `config.yaml`. Ensure `services:` section is present and addon has restarted after changes.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and test locally
4. Commit: `git commit -m "Add feature X"`
5. Push: `git push origin feature/my-feature`
6. Open a Pull Request

## Resources

- [Home Assistant Addon Documentation](https://developers.home-assistant.io/docs/add-ons)
- [Multi-Container Addons](https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile)
- [Ingress Documentation](https://developers.home-assistant.io/docs/add-ons/communication#ingress)
- [Addon Configuration Schema](https://developers.home-assistant.io/docs/add-ons/configuration#add-on-config)

## License

Same as main project (check root LICENSE file).
