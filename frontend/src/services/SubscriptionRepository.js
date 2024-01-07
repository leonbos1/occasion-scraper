class SubscriptionRepository {
    constructor() {
        this.api_url = import.meta.env.VITE_API_URL;
        this.api_key = import.meta.env.VITE_API_KEY;
    }

    async getAllSubscriptions() {
        var url = '/subscriptions';
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            }
        });

        return await response.json();
    }

    async getSubscriptionsByPage(page, size, orderBy = 'created', orderDirection = 'desc') {
        var url = '/subscriptions/' + page + '/' + size;

        const response = await fetch(this.api_url + url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            },
            body: JSON.stringify({
                orderBy: orderBy,
                orderDirection: orderDirection
            })
        });

        return await response.json();
    }

    async getSubscriptionById(id) {
        var url = '/subscriptions/' + id;
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            }
        });

        return await response.json();
    }

    async addSubscription(subscription) {
        var url = '/subscriptions';
        const response = await fetch(this.api_url + url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            },
            body: JSON.stringify(subscription)
        });

        return await response.json();
    }

    async getMaxPage(pageSize) {
        var url = '/subscriptions/maxpage/' + pageSize;
        const response = await fetch(this.api_url + url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            }
        });

        return await response.json();
    }

    async updateSubscription(subscription) {
        var url = '/subscriptions/' + subscription.id;
        const response = await fetch(this.api_url + url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key
            },
            body: JSON.stringify(subscription)
        });

        return await response.json();
    }

    async deleteSubscription(blueprintId) {
        var url = '/subscriptions/blueprint/' + blueprintId;
        const response = await fetch(this.api_url + url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.api_key,
                'Authorization': localStorage.getItem('token')
            }
        });

        return response;
    }
}

export default new SubscriptionRepository();
