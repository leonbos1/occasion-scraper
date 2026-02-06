# occasion-scraper

This is a Python application designed to scrape second-hand car listings from popular car selling websites and send email notifications when new cars matching specified criteria are found.

## Deployment Options

### Option 1: Home Assistant Addon (Recommended)

The easiest way to run occasion-scraper is as a Home Assistant addon. This provides:
- ✨ One-click installation via Home Assistant UI
- 🔧 Easy configuration through Home Assistant
- 🔒 Secure ingress access (no extra ports needed)
- 💾 Automatic backup integration
- 🤖 Home Assistant service calls for automations

**Installation:**
1. Add this repository to your Home Assistant Add-on Store
2. Install the "Occasion Scraper" addon
3. Configure database and admin credentials
4. Start the addon
5. Access via the sidebar or addon page

See [addon/DOCS.md](addon/DOCS.md) for detailed instructions.

### Option 2: Standalone Deployment

Run the application as separate services using Docker Compose or manual setup.

Table of Contents

    Features
    Prerequisites
    Installation
    Usage
    Configuration
    Contributing
    License

Features

    Automated web scraping of second-hand car listings.
    Customizable search criteria for car listings.
    Email notifications for newly found cars.
    Scheduled execution at 7 AM and 7 PM.

Prerequisites

Before you begin, ensure you have met the following requirements:

    Python 3.x installed on your server.
    Required Python packages installed. You can install them using pip:

bash

pip install requests beautifulsoup4 smtplib yagmail schedule

Installation

    Clone this repository to your server:

bash

git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/leonbos1/occasion-scraper.git)

    Change into the project directory:

bash

Usage

To run the application, execute the following command:

bash

flask --app occasion-scraper run --reload

The application will start scraping car listings based on the configured criteria and will send email notifications when new cars are found.

## Brand and Model Catalog Management

The application maintains a database catalog of car brands and models from AutoScout24. This provides:

- Searchable dropdown menus for brand/model selection in blueprints
- Admin tools to manage the catalog (enable/disable brands/models, customize display names)
- Automatic discovery of new brands/models via web scraping

### Initial Catalog Setup

When starting a fresh instance, populate the brand/model catalog:

1. Start the backend server (see Usage above)
2. Log in as an admin user
3. Navigate to "Brand Catalog" in the admin menu
4. Click "Trigger Catalog Scraper" to fetch all brands and models from AutoScout24
5. The scraper respects robots.txt and rate limits (1-3 second delays)
6. Once complete, brands and models are available in the dropdown menus

### Managing the Catalog

**Brand Management** (`/admin/brands`):
- View all discovered brands
- Enable/disable brands (disabled brands won't appear in dropdowns)
- Edit display names (e.g., "BMW" instead of "bmw")
- Bulk enable/disable multiple brands
- View models for a specific brand

**Model Management** (`/admin/models`):
- View all models, optionally filtered by brand
- Enable/disable models
- Edit display names
- Bulk enable/disable multiple models

The frontend caches catalog data for 1 hour to reduce API calls.

Configuration

Before running the application, make sure to configure the following settings:

    Search Criteria: Edit the config.py file to specify your desired search criteria, such as make, model, price range, etc.

    Email Configuration: In config.py, provide your email configuration settings, including your email address, SMTP server details, and app password (if necessary) for sending email notifications.

    Scheduled Execution: The application is set to run at 7 AM and 7 PM by default. You can adjust the schedule in car_scraping.py using the schedule library.

Happy car hunting! If you have any questions or encounter any issues, please don't hesitate to open an issue.
