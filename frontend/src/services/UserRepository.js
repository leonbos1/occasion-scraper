import credentials from '../../../credentials.json';

class UserRepository {
    constructor() {
        this.api_url = credentials.api_url;
        this.api_key = credentials.api_key;
    }

    async getAllUsers() {
        var url = '/users';
        const response = await this.get(url);

        return await response.json();
    }

    async getUserById(id) {
        const response = await this.get(`/users/${id}`);

        return await response.json();
    }

    async updateUser(id, user) {
        const response = await fetch(this.api_url + `/users/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(user),
        });

        return await response.json();
    }

    async addUser(user) {
        const response = await fetch(this.api_url + '/users', {
            method: 'POST'
        });

        return await response.json();
    }

    async deleteUser(id) {
        const response = await fetch(this.api_url + `/users/${id}`, {
            method: 'DELETE'
        });

        return await response.json();
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

export default new UserRepository();