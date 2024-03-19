class CarRepository {
    constructor() {
        this.api_url = import.meta.env.VITE_API_URL;
        this.api_key = import.meta.env.VITE_API_KEY;
    }

    async getAllCars() {
        var url = '/cars';
        const response = await this.get(url);

        return await response.json();
    }

    async getBrandsAndModels() {
        var url = '/cars/brands_and_models';

        try {
            const response = await this.get(url);

            return await response.json();

        } catch (error) {
            return []
        }
    }

    async getCarsByPage(page, size, orderBy = "created", orderDirection = "desc", filters = {}) {
        var url = '/cars/' + page + '/' + size;

        try {
            var properties = {
                order_by: orderBy,
                order_direction: orderDirection,
                filters: filters
            }

            const response = await fetch(this.api_url + url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': this.api_key
                },
                body: JSON.stringify(properties),
            });

            return await response.json();
        }
        catch (error) {
            console.log(error);
            return []
        }
    }

    async getMaxPage(size) {
        var url = '/cars/max_page/' + size;
        const response = await this.get(url);

        return await response.json();
    }

    async getRecentCars(amount) {
        var url = '/cars/recent/' + amount;

        try {
            const response = await this.get(url);

            return await response.json();
        }

        catch (error) {
            return []
        }
    }

    async getExpensiveCars(amount) {
        var url = '/cars/expensive/' + amount;

        try {
            const response = await this.get(url);

            return await response.json();
        }

        catch (error) {
            return []
        }
    }

    async getCarById(id) {
        const response = await this.get(`/cars/${id}`);

        return await response.json();
    }

    async updateCar(car) {
        const response = await fetch(this.api_url + `/cars/${car.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(car),
        });

        return response;
    }

    async getFilters() {
        var url = '/cars/filters';

        try {
            const response = await this.get(url);

            return await response.json();
        }

        catch (error) {
            return []
        }
    }

    async get(url) {
        const response = await fetch(this.api_url + url, {
            headers: {
                'X-API-Key': this.api_key
            }
        });

        return response;
    }

    async post(url, body) {
        const response = await fetch(this.api_url + url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': this.api_key
            },
            body: JSON.stringify(body),
        });

        return response;
    }
}

export default new CarRepository();