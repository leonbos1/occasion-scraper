<template>
    <div class="">
        <h1 class="text-3xl font-bold text-gray-700 mb-2">Users in database</h1>
        <h2 class="text-2xl font-bold text-gray-700 mb-2">{{ usersInDatabase }}</h2>

    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import DashboardRepository from '../../services/DashboardRepository';

const usersInDatabase = ref(0);

onMounted(async () => {
    const data = await DashboardRepository.getUsersInDatabase();

    usersInDatabase.value = data;
});

</script>