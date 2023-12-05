class BlueprintRepository {
    constructor() {
        this.api_url = import.meta.env.VITE_API_URL;
        this.api_key = import.meta.env.VITE_API_KEY;
    }

    async getAllBlueprints() {
        var url = '/blueprints';
        const response = await this.get(url);

        return await response.json();
    }

    async getBlueprintsByPage(page, size) {
        var url = '/blueprints/' + page + '/' + size;
        try {
            const response = await this.get(url);

            return await response.json();
        }
        catch (error) {
            return []
        }
    }

    async getMaxPage(size) {
        var url = '/blueprints/max_page/' + size;
        const response = await this.get(url);

        return await response.json();
    }

    async getBlueprintById(id) {
        const response = await this.get(`/blueprints/${id}`);

        return await response.json();
    }

    async updateBlueprint(blueprint) {
        const response = await fetch(this.api_url + `/blueprints/${blueprint.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(blueprint),
        });

        return response;
    }

    async createBlueprint(blueprint) {
        const response = await fetch(this.api_url + '/blueprints', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(blueprint),
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

export default new BlueprintRepository();