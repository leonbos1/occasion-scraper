<template>
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">Id</th>
                    <th scope="col" class="px-6 py-3">Brand</th>
                    <th scope="col" class="px-6 py-3">Model</th>
                    <th scope="col" class="px-6 py-3">Min Price</th>
                    <th scope="col" class="px-6 py-3">Max Price</th>
                    <th scope="col" class="px-6 py-3">Min Mileage</th>
                    <th scope="col" class="px-6 py-3">Max Mileage</th>
                    <th scope="col" class="px-6 py-3">Min First Registration</th>
                    <th scope="col" class="px-6 py-3">Max First Registration</th>
                    <th scope="col" class="px-6 py-3">Vehicle Type</th>
                    <th scope="col" class="px-6 py-3">Owned Id</th>
                    <th scope="col" class="px-6 py-3">City</th>
                    <th scope="col" class="px-6 py-3">Created</th>
                    <th scope="col" class="px-6 py-3">Updated</th>
                    <th scope="col" class="px-6 py-3">Max Distance From Home</th>
                </tr>
            </thead>
            <tbody>
                <BlueprintRow v-for="blueprint in blueprints" :key="blueprint.id" :blueprint="blueprint" />
            </tbody>
        </table>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import BlueprintRow from './BlueprintRow.vue';
import credentials from '../../../../credentials.json';

const blueprints = ref([]);

onMounted(async () => {

    var api_key = credentials.api_key;

    try {
        const response = await fetch('http://192.168.68.138:8000/blueprints', {
            headers: {
                'X-API-Key': api_key
            }
        });
        const data = await response.json();
        blueprints.value = data;
    } catch (error) {
        console.error('Failed to fetch blueprints:', error);
    }
});
</script>
  
<style scoped></style>
  