class DashboardRepository {
    constructor() {
        this.api_url = import.meta.env.VITE_API_URL;
        this.api_key = import.meta.env.VITE_API_KEY;
    }

    async getCarsScrapedPerDay(days) {
        var url = '/scrape_sessions/cars_per_day/' + days;
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            }
        });

        return await response.json();
    }

    async getWeeklyScrapedCars(weeks) {
        var url = '/scrape_sessions/cars_per_week/' + weeks;
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            }
        });

        return await response.json();
    }

    async getMonthlyScrapedCars(months) {
        var url = '/scrape_sessions/cars_per_month/' + months;
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            }
        });

        return await response.json();
    }

    async startScraper() {
        var url = '/start';
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            }
        });

        return await response.json();
    }

    async getCarBrands() {
        var url = '/cars/brands';
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            }
        });

        return await response.json();
    }

    async getCarModels() {
        var url = '/cars/models';
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            }
        });

        return await response.json();
    }

    async getCarsInDatabase() {
        var url = '/cars/count';
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            }
        });

        return await response.json();
    }

    async getUsersInDatabase() {
        var url = '/users/count';
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key,
            },
        });

        return await response.json();
    }

    async getBlueprintsInDatabase() {
        var url = '/blueprints/count';
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key,
            },
        });

        return await response.json();
    }

    async getBestDays() {
        var url = '/scrape_sessions/best_days';
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            }
        });

        return await response.json();
    }
}

export default new DashboardRepository();
