import credentials from '../../../credentials.json';

class SubscriptionRepository {
    constructor() {
        this.api_url = credentials.api_url;
        this.api_key = credentials.api_key;
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

}

export default new SubscriptionRepository();
