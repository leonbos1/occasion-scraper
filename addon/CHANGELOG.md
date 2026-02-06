# Changelog

All notable changes to the Occasion Scraper Home Assistant Addon will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-06

### Added
- Initial release of Home Assistant addon
- Multi-container architecture (backend, frontend, MySQL)
- Home Assistant ingress integration for embedded UI
- Configuration via Home Assistant UI
- Admin user auto-creation from addon options
- Database persistence in `/data` directory
- Home Assistant services for automation:
  - `trigger_scrape`: Start a scraping session
  - `get_scrape_status`: Check scraping progress
  - `list_cars`: Query cars with filters
  - `get_car_details`: Get detailed car information
- Comprehensive documentation (DOCS.md, README.md)
- Support for multiple scrapers:
  - AutoScout24
  - Marktplaats
  - ANWB
  - Gaspedaal
- Brand and model catalog management
- User authentication and role-based access control
- Dashboard with scraping statistics

### Features
- One-click installation via Home Assistant Add-on Store
- Automatic database initialization
- Health checks for all containers
- Configurable scraping intervals
- Enable/disable individual scrapers
- Persistent storage across restarts and updates
- Compatible with Home Assistant backup system

### Technical
- Python Flask backend (REST API)
- Vue.js 3 frontend with Vite
- MySQL 8.0 database
- Docker Compose orchestration
- Ingress base path support for routing
- Environment-based configuration

## [Unreleased]

### Planned
- Home Assistant authentication integration
- Sensor entities for scraping statistics
- Binary sensor for new car alerts
- Notification integration
- More granular scraper configuration
- Advanced filtering and search capabilities
