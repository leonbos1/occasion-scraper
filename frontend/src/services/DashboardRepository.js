class DashboardRepository {
    constructor() {
        this.api_url = import.meta.env.VITE_API_URL;
        this.api_key = import.meta.env.VITE_API_KEY;
    }

    async getCarsScrapedPerDay(days) {
        var url = '/scrape_sessions/cars_per_day/' + days;
        try {
            const response = await fetch(this.api_url + url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.api_key
                }
            });
            const data = await response.json();
            return data.data || [];
        } catch (error) {
            console.error('Error fetching cars per day:', error);
            return [];
        }
    }

    async getWeeklyScrapedCars(weeks) {
        var url = '/scrape_sessions/cars_per_week/' + weeks;
        try {
            const response = await fetch(this.api_url + url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.api_key
                }
            });
            const data = await response.json();
            return data.data || [];
        } catch (error) {
            console.error('Error fetching weekly cars:', error);
            return [];
        }
    }

    async getMonthlyScrapedCars(months) {
        var url = '/scrape_sessions/cars_per_month/' + months;
        try {
            const response = await fetch(this.api_url + url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.api_key
                }
            });
            const data = await response.json();
            return data.data || [];
        } catch (error) {
            console.error('Error fetching monthly cars:', error);
            return [];
        }
    }

    async startScraper() {
        var url = '/start';
        try {
            const response = await fetch(this.api_url + url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.api_key
                }
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error starting scraper:', error);
            return { success: false, error: error.message };
        }
    }

    async getCarBrands() {
        var url = '/cars/brands';
        try {
            const response = await fetch(this.api_url + url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.api_key
                }
            });
            const data = await response.json();
            return data.data || [];
        } catch (error) {
            console.error('Error fetching car brands:', error);
            return [];
        }
    }

    async getCarModels() {
        var url = '/cars/models';
        try {
            const response = await fetch(this.api_url + url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.api_key
                }
            });
            const data = await response.json();
            return data.data || [];
        } catch (error) {
            console.error('Error fetching car models:', error);
            return [];
        }
    }

    async getCarsInDatabase() {
        var url = '/cars/count';
        try {
            const response = await fetch(this.api_url + url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.api_key
                }
            });
            const data = await response.json();
            return data.data?.count ?? 0;
        } catch (error) {
            console.error('Error fetching cars count:', error);
            return 0;
        }
    }

    async getUsersInDatabase() {
        var url = '/users/count';
        try {
            const response = await fetch(this.api_url + url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.api_key,
                },
            });
            const data = await response.json();
            return data.data?.count ?? 0;
        } catch (error) {
            console.error('Error fetching users count:', error);
            return 0;
        }
    }

    async getBlueprintsInDatabase() {
        var url = '/blueprints/count';
        try {
            const response = await fetch(this.api_url + url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.api_key,
                },
            });
            const data = await response.json();
            return data.data?.count ?? 0;
        } catch (error) {
            console.error('Error fetching blueprints count:', error);
            return 0;
        }
    }

    async getBestDays() {
        var url = '/scrape_sessions/best_days';
        try {
            const response = await fetch(this.api_url + url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': this.api_key
                }
            });
            const data = await response.json();
            return data.data || [];
        } catch (error) {
            console.error('Error fetching best days:', error);
            return [];
        }
    }
}

export default new DashboardRepository();
