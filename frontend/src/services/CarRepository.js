import credentials from '../../../credentials.json';

class CarRepository {
    constructor() {
        this.api_url = credentials.api_url;
        this.api_key = credentials.api_key;
    }

    async getAllCars() {
        var url = '/cars';
        const response = await this.get(url);

        return await response.json();
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

    async get(url) {
        const response = await fetch(this.api_url + url, {
            headers: {
                'X-API-Key': this.api_key
            }
        });

        return response;
    }
}

export default new CarRepository();