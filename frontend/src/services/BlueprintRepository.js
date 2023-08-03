import credentials from '../../../credentials.json';

class BlueprintRepository {
    constructor() {
        this.api_url = credentials.api_url;
        this.api_key = credentials.api_key;
    }

    async getAllBlueprints() {
        var url = '/blueprints';
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