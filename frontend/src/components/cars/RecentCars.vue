<template>
    <div class="container mx-auto p-4">
        <div class="row">
            <h1 class="text-2xl font-bold mb-4">Recent Cars</h1>
        </div>

        <div v-if="!cars || cars.length === 0" class="flex flex-col justify-center items-center h-48 bg-white rounded-lg shadow-lg">
            <svg class="w-16 h-16 text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <h3 class="text-xl font-semibold text-gray-700 mb-1">No Recent Cars</h3>
            <p class="text-gray-500 text-sm">No cars have been scraped yet.</p>
        </div>
        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
            <div v-for="(car, index) in cars.slice(0, 5)" :key="index"
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 h-max">
                <img :src="getImageSrc(car.base_image)" class="w-full h-48 object-cover" />

                <div class="p-4">
                    <h2 class="text-lg font-semibold">{{ car.brand }} {{ car.model }}</h2>
                    <p class="text-sm text-gray-600">Bouwjaar: <span class="text-gray-800">{{ car.first_registration
                    }}</span></p>
                    <p class="text-sm text-gray-600">Kilometerstand: <span class="text-gray-800">{{ car.mileage }}</span>
                    </p>
                    <p class="text-sm text-gray-600">Prijs: <span class="font-semibold text-green-600">${{ car.price
                    }}</span></p>
                    <p class="text-sm text-gray-600">Locatie: <span class="text-gray-800">{{ car.location }}</span></p>
                    <a :href="'https://www.autoscout24.nl' + car.url" target="_blank"
                        class="inline-block mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors duration-200 text-center bottom-0">
                        Bekijk
                        Details</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import CarRepository from '../../services/CarRepository';
import getImageSrc from '../../utils/imagehelper';

const cars = ref([]);
const columns = ref([]);

onMounted(async () => {
    try {
        columns.value = ['brand', 'model', 'first_registration', 'price', 'mileage', 'location', 'url', 'base_image'];

        cars.value = await CarRepository.getRecentCars(5);;
    } catch (error) {
        console.error('Failed to fetch cars:', error);
    }
});

</script>
  
<style scoped></style>