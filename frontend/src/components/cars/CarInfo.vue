<template>
    <div class="container mx-auto px-4">
        <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold mb-6 text-center md:text-left">{{ car.brand }} {{ car.model }}</h1>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div class="flex flex-col items-center gap-4">
                <img :src="currentImageSrc" alt="Car image" class="max-w-full h-auto border border-gray-300 rounded-lg shadow-md">
                <div v-if="imageSources.length > 1" class="grid grid-cols-5 gap-2 w-full">
                    <button v-for="(src, index) in imageSources" :key="index" type="button"
                        class="border rounded-md overflow-hidden focus:outline-none focus:ring-2 focus:ring-blue-500"
                        :class="index === selectedImageIndex ? 'ring-2 ring-blue-500' : ''"
                        @click="selectedImageIndex = index">
                        <img :src="src" alt="Car thumbnail" class="w-full h-16 object-cover" />
                    </button>
                </div>
            </div>
            <div class="space-y-4">
                <p class="text-lg"><strong>Price:</strong> <span class="text-gray-600">{{ car.price }} €</span></p>
                <p class="text-lg"><strong>Mileage:</strong> <span class="text-gray-600">{{ car.mileage }} km</span></p>
                <p class="text-lg"><strong>First registration:</strong> <span class="text-gray-600">{{ car.first_registration }}</span></p>
                <p class="text-lg"><strong>Location:</strong> <span class="text-gray-600">{{ car.location }}</span></p>
                <a :href="offerUrl" class="inline-block mr-2 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded transition duration-300">Go to offer</a>
                <a href="/cars" class="ml-2 bg-gray-200 py-2 px-4 rounded hover:bg-gray-300">Back</a>
            </div>
        </div>
    </div>
</template>


<script setup>

import { defineEmits, defineProps, onMounted, ref, computed } from 'vue';
import CarRepository from '../../services/CarRepository';
import getImageSrc from '../../utils/imagehelper';

const props = defineProps({
    id: {
        type: String,
        required: true
    }
});

const car = ref({});
const images = ref([]);
const selectedImageIndex = ref(0);

const imageSources = computed(() =>
    images.value.map((img) => getImageSrc(img.image_data)).filter(Boolean)
);

const currentImageSrc = computed(() => {
    if (imageSources.value.length > 0) {
        return imageSources.value[selectedImageIndex.value] || imageSources.value[0];
    }
    return getImageSrc(car.value?.base_image);
});

const offerUrl = computed(() => {
    const url = car.value?.url || '';
    if (!url) {
        return '';
    }
    return url.startsWith('http') ? url : `https://www.autoscout24.nl${url}`;
});

onMounted(async () => {
    car.value = await CarRepository.getCarById(props.id);
    images.value = await CarRepository.getCarImages(props.id);
});

</script>