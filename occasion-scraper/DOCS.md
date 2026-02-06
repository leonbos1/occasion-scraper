# Occasion Scraper Home Assistant Addon

Automated car marketplace scraper with brand/model catalog management. Scrapes listings from multiple Dutch car marketplaces including AutoScout24, Marktplaats, ANWB, and Gaspedaal.

## Installation

1. Add this repository to your Home Assistant Add-on Store:
   - Navigate to **Settings** → **Add-ons** → **Add-on Store** → **⋮** (menu) → **Repositories**
   - Add the repository URL: `https://github.com/leonbos1/occasion-scraper`
   
2. Find "Occasion Scraper" in the Add-on Store and click **Install**

3. Configure the addon (see Configuration section below)

4. Start the addon

5. Access the UI via the addon's sidebar entry or the **Open Web UI** button

## Configuration

### Database Settings

- **mysql_root_password**: Root password for the MySQL database (change this!)
- **db_name**: Application database name (default: `occasion_scraper`)
- **db_user**: Application database user (default: `scraper`)
- **db_password**: Application database password (change this!)

### Admin User

- **admin_email**: Email address for the admin user
- **admin_password**: Password for the admin user (used to log into the UI)

The admin user will be automatically created/updated on addon startup.

### Scraping Configuration

- **scrape_interval_minutes**: How often to run automatic scraping (in minutes, default: 60)
- **enable_autoscout**: Enable AutoScout24 scraper (default: true)
- **enable_marktplaats**: Enable Marktplaats scraper (default: true)
- **enable_anwb**: Enable ANWB scraper (default: true)
- **enable_gaspedaal**: Enable Gaspedaal scraper (default: true)

### Example Configuration

```yaml
mysql_root_password: "MySecureRootPass123!"
db_name: "occasion_scraper"
db_user: "scraper"
db_password: "MySecureDbPass456!"
admin_email: "admin@mydomain.com"
admin_password: "MySecureAdminPass789!"
scrape_interval_minutes: 60
enable_autoscout: true
enable_marktplaats: true
enable_anwb: false
enable_gaspedaal: false
```

## Using the Addon

### Web Interface

After starting the addon, click the sidebar entry or **Open Web UI** button to access the application. Log in with your configured admin credentials.

**Features:**
- **Dashboard**: View scraping statistics and trends
- **Cars**: Browse scraped car listings with filtering
- **Blueprints**: Create search templates for specific car criteria
- **Brand Catalog**: Manage the list of car brands (Admin only)
- **Model Catalog**: Manage car models by brand (Admin only)
- **Users**: Manage additional users (Admin only)

### Home Assistant Services

The addon exposes services for use in automations:

#### `hassio.addon_stdin` with `addon: occasion-scraper` and `input:`

**trigger_scrape**
```yaml
service: hassio.addon_stdin
data:
  addon: occasion-scraper
  input:
    service: trigger_scrape
    scrapers: ["autoscout", "marktplaats"]  # Optional, defaults to all enabled
```

**get_scrape_status**
```yaml
service: hassio.addon_stdin
data:
  addon: occasion-scraper
  input:
    service: get_scrape_status
    session_id: "abc-123"  # Session ID from trigger_scrape
```

**list_cars**
```yaml
service: hassio.addon_stdin
data:
  addon: occasion-scraper
  input:
    service: list_cars
    brand: "volkswagen"
    model: "golf"
    max_price: 15000
    limit: 50
```

**get_car_details**
```yaml
service: hassio.addon_stdin
data:
  addon: occasion-scraper
  input:
    service: get_car_details
    car_id: "uuid-here"
```

## Initial Setup

### First Time Setup

1. Start the addon and wait for initialization to complete (check logs)
2. Access the web UI and log in with your admin credentials
3. Navigate to **Admin** → **Brand Catalog** and click **Build Catalog** to extract brands/models from any existing data
4. Set up blueprints for the types of cars you want to track
5. Wait for automatic scraping or trigger manually via the UI or Home Assistant service

### Building the Brand/Model Catalog

The addon includes a catalog builder that extracts distinct brands and models from your scraped cars:

1. Log in as admin
2. Go to **Admin** → **Brand Catalog**
3. Click **Build Catalog** button
4. Wait for extraction to complete (watch for success message)
5. Review and enable/disable brands as needed
6. Navigate to **Admin** → **Model Catalog** to manage models

## Troubleshooting

### Addon won't start

- Check the addon logs for error messages
- Verify all passwords are set (not using defaults)
- Ensure Home Assistant has enough resources (disk space, memory)

### Cannot access web UI

- Verify ingress is enabled in addon configuration
- Try clicking the sidebar entry instead of **Open Web UI**
- Check that the addon is running (green status)
- Review addon logs for backend errors

### Scraping not working

- Check that at least one scraper is enabled in configuration
- Verify network connectivity from the addon
- Review logs for HTTP errors or rate limiting
- Some scrapers may require VPN or Dutch IP address

### Database errors

- Ensure MySQL has enough disk space (check `/data` directory size)
- Try restarting the addon
- If corruption suspected, consider backing up data and reinstalling

### Authentication issues

- Verify admin credentials in addon configuration match what you're entering
- Admin user is automatically updated on startup - restart addon after changing password
- Check that role is '1' for admin access (visible in user management)

### Missing brands or models

- Use the **Build Catalog** button in Brand Management to extract from existing cars
- Catalog builder runs automatically on first install but may need manual trigger later
- You can manually add brands/models via the admin UI

## Data Backup

The addon stores all data in the `/data` directory, which is included in Home Assistant backups.

To back up:
1. Go to **Settings** → **System** → **Backups**
2. Create a **Full Backup** or **Partial Backup** (include occasion-scraper addon)

To restore:
1. Install the addon (don't start it yet)
2. Restore your Home Assistant backup
3. Start the addon

## Support

For issues, feature requests, or contributions:
- GitHub: https://github.com/leonbos1/occasion-scraper
- Report issues: https://github.com/leonbos1/occasion-scraper/issues

## Privacy & Data

This addon:
- Scrapes public car listings from marketplaces
- Stores data locally in your Home Assistant instance
- Does not send data to external services
- Does not track users or usage

Scraped data includes: car details, prices, images, listing URLs. No personal information is collected.
