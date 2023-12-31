<template>
    <div class="">
        <h1 class="text-3xl font-bold text-gray-700 mb-2">Cars in database</h1>
        <h2 class="text-2xl font-bold text-gray-700 mb-2">{{ carsInDatabase }}</h2>

    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import DashboardRepository from '../../services/DashboardRepository';

const carsInDatabase = ref(0);

onMounted(async () => {
    const data = await DashboardRepository.getCarsInDatabase();

    carsInDatabase.value = data;
});

</script>