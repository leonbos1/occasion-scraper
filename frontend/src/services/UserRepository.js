class UserRepository {
    constructor() {
        this.api_url = import.meta.env.VITE_API_URL;
        this.api_key = import.meta.env.VITE_API_KEY;
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

    async login(user) {
        const response = await fetch(this.api_url + '/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': this.api_key
            },
            body: JSON.stringify(user),
        });

        return await response;
    }

    async logout() {
        var token = localStorage.getItem('token');
        if (token == null) {
            return;
        }

        const response = await fetch(this.api_url + '/users/logout', {
            method: 'POST',
            headers: {
                'X-API-Key': this.api_key,
                'Authorization': token
            }
        });

        return await response.json();
    }

    async register(user) {
        const response = await fetch(this.api_url + '/users/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': this.api_key
            },
            body: JSON.stringify(user),
        });

        return await response;
    }

    async getProfile() {
        const response = await this.get('/users/profile');

        return await response.json();
    }

    async get(url) {
        const response = await fetch(this.api_url + url, {
            headers: {
                'X-API-Key': this.api_key,
                'Authorization': localStorage.getItem('token')
            }
        });

        return response;
    }
}

export default new UserRepository();