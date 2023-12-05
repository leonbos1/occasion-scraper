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
}

export default new DashboardRepository();
