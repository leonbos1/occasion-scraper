# occasion-scraper

This is a Python application designed to scrape second-hand car listings from popular car selling websites and send email notifications when new cars matching specified criteria are found. The application is currently running on a server and is scheduled to execute twice a day, at 7 AM and 7 PM.
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
Configuration

Before running the application, make sure to configure the following settings:

    Search Criteria: Edit the config.py file to specify your desired search criteria, such as make, model, price range, etc.

    Email Configuration: In config.py, provide your email configuration settings, including your email address, SMTP server details, and app password (if necessary) for sending email notifications.

    Scheduled Execution: The application is set to run at 7 AM and 7 PM by default. You can adjust the schedule in car_scraping.py using the schedule library.

Happy car hunting! If you have any questions or encounter any issues, please don't hesitate to open an issue.
