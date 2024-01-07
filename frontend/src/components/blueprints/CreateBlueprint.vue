<template>
    <div class="p-4">
        <form @submit.prevent="handleSubmit" class="space-y-4">
            <div class="flex flex-col">
                <label for="name" class="text-gray-700">Name:</label>
                <input type="text" id="name" v-model="blueprint.name" class="border border-gray-300 rounded p-2" />
            </div>

            <div class="flex flex-col">
                <label for="minPrice" class="text-gray-700">Min Price:</label>
                <input type="number" id="minPrice" v-model="blueprint.min_price"
                    class="border border-gray-300 rounded p-2" />
            </div>

            <div class="flex flex-col">
                <label for="maxPrice" class="text-gray-700">Max Price:</label>
                <input type="number" id="maxPrice" v-model="blueprint.max_price"
                    class="border border-gray-300 rounded p-2" />
            </div>

            <div class="flex flex-col">
                <label for="minMileage" class="text-gray-700">Min Mileage:</label>
                <input type="number" id="minMileage" v-model="blueprint.min_mileage"
                    class="border border-gray-300 rounded p-2" />
            </div>

            <div class="flex flex-col">
                <label for="maxMileage" class="text-gray-700">Max Mileage:</label>
                <input type="number" id="maxMileage" v-model="blueprint.max_mileage"
                    class="border border-gray-300 rounded p-2" />
            </div>

            <button type="submit"
                class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200">
                Submit
            </button>
        </form>
    </div>
</template>
  
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // Import useRouter from vue-router
import BlueprintRepository from '../../services/BlueprintRepository';

const router = useRouter();

const blueprint = ref({
    name: '',
    min_price: 0,
    max_price: 0,
    min_mileage: 0,
    max_mileage: 0,
});

const handleSubmit = () => {
    console.log(blueprint.value);
    BlueprintRepository.createBlueprint(blueprint.value);

    router.push({ name: 'Blueprints' });
};

</script>