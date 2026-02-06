<template>
    <div class="container mx-auto p-4">
        <div class="row">
            <h1 class="text-2xl font-bold mb-4">Expensive Cars</h1>
        </div>

        <div v-if="!cars || cars.length === 0" class="flex flex-col justify-center items-center h-48 bg-white rounded-lg shadow-lg">
            <svg class="w-16 h-16 text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <h3 class="text-xl font-semibold text-gray-700 mb-1">No Expensive Cars</h3>
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

        cars.value = await CarRepository.getExpensiveCars(5);;
    } catch (error) {
        console.error('Failed to fetch cars:', error);
    }
});

</script>
  
<style scoped></style>