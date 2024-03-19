<template>
    <div class="flex flex-wrap justify-center">
        <div v-for="blueprint in blueprints" :key="blueprint.id" class="w-full md:w-1/2 lg:w-1/3 xl:w-1/4 p-2">
            <div class="bg-white shadow-lg rounded-lg overflow-hidden h-max">
                <div class="p-4 max-h-1/4">
                    <h1 class="font-bold text-lg">{{ blueprint.name }}</h1>
                    <p class="text-gray-700">{{ blueprint.created }}</p>
                    <p class="text-gray-600">{{ blueprint.brand }} {{ blueprint.model }}</p>
                    <p class="text-gray-600">Build year: {{ blueprint.min_first_registration }} - {{
            blueprint.max_first_registration }}</p>
                    <p class="text-gray-600 mb-4">Mileage: {{ blueprint.min_mileage }} - {{ blueprint.max_mileage }} km
                    </p>
                    <div>
                        <button @click="handleSubscriptionChange(blueprint)" v-if="!blueprint.isSubscribed"
                            class="inline-block bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">Subscribe</button>
                        <button @click="handleSubscriptionChange(blueprint)" v-if="blueprint.isSubscribed"
                            class="p-4 inline-block bg-blue-500 text-white py-2 px-4 m-2 rounded hover:bg-blue-600">Unsubscribe</button>
                        <button @click="handleDeleteBlueprint(blueprint)" v-if="blueprint.isOwner"
                            class="inline-block bg-red-500 text-white py-2 px-4 m-2 rounded hover:bg-red-600">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps } from 'vue';
import SubscriptionRepository from '../../services/SubscriptionRepository';
import BlueprintRepository from '../../services/BlueprintRepository';
import { useRouter } from 'vue-router';

const props = defineProps({
    blueprints: {
        type: Array,
        required: true
    }
});

const router = useRouter();

async function handleSubscriptionChange(blueprint) {
    if (blueprint.isSubscribed) {
        await SubscriptionRepository.deleteSubscription(blueprint.id);
    } else {
        var newSubscription = {
            user_id: localStorage.getItem('id'),
            blueprint_id: blueprint.id
        }

        await SubscriptionRepository.addSubscription(newSubscription);
    }

    blueprint.isSubscribed = !blueprint.isSubscribed;
}

async function handleDeleteBlueprint(blueprint) {
    await BlueprintRepository.deleteBlueprint(blueprint.id);

    router.go();
}

function addUserIsSubscribed() {
    var newBlueprints = [];

    props.blueprints.forEach((blueprint) => {
        blueprint.subscriptions.forEach((subscription) => {
            if (subscription.user.id == localStorage.getItem('id')) {
                blueprint.isSubscribed = true;
            }
        });

        newBlueprints.push(blueprint);
    });

    props.blueprints = newBlueprints;
}

function addBlueprintIsOwner() {
    var newBlueprints = [];

    props.blueprints.forEach((blueprint) => {
        if (blueprint.owner_id == localStorage.getItem('id')) {
            blueprint.isOwner = true;
        }

        newBlueprints.push(blueprint);
    });

    props.blueprints = newBlueprints;
}

onMounted(async () => {
    addUserIsSubscribed();
    addBlueprintIsOwner();
});

</script>