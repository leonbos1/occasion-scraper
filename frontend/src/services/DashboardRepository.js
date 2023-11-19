import credentials from '../../../credentials.json';

class DashboardRepository {
    constructor() {
        this.api_url = credentials.api_url;
        this.api_key = credentials.api_key;
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
}

export default new DashboardRepository();
