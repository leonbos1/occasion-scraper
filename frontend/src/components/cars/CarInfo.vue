<template>
    <div class="container mx-auto px-4">
        <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold mb-6 text-center md:text-left">{{ car.brand }} {{ car.model }}</h1>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div class="flex justify-center">
                <img :src="car.base_image" alt="Car image" class="max-w-full h-auto border border-gray-300 rounded-lg shadow-md">
            </div>
            <div class="space-y-4">
                <p class="text-lg"><strong>Price:</strong> <span class="text-gray-600">{{ car.price }} €</span></p>
                <p class="text-lg"><strong>Mileage:</strong> <span class="text-gray-600">{{ car.mileage }} km</span></p>
                <p class="text-lg"><strong>First registration:</strong> <span class="text-gray-600">{{ car.first_registration }}</span></p>
                <p class="text-lg"><strong>Location:</strong> <span class="text-gray-600">{{ car.location }}</span></p>
                <a :href="car.url" class="inline-block mr-2 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded transition duration-300">Go to offer</a>
                <a href="/cars" class="ml-2 bg-gray-200 py-2 px-4 rounded hover:bg-gray-300">Back</a>
            </div>
        </div>
    </div>
</template>


<script setup>

import { defineEmits, defineProps, onMounted, ref } from 'vue';
import CarRepository from '../../services/CarRepository';

const props = defineProps({
    id: {
        type: String,
        required: true
    }
});

const car = ref({});

onMounted(async () => {
    car.value = await CarRepository.getCarById(props.id);
});

</script>