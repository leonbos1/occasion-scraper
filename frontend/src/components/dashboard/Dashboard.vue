<template>
    <div class="container mx-auto p-4">
        <div class="bg-yellow-600 mb-8">
            <button v-if="role == '1' && !isScraping"
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-full" @click="start">Start
                Scraper!</button>
            <button v-else class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded w-full">Scraper
                disabled!</button>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-10 h-max mb-8">

            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center h-32">
                <CarsInDatabase />
            </div>
            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center h-32">
                <UsersInDatabase />
            </div>
            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center h-32">
                <BlueprintsInDatabase />
            </div>
        </div>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-10 h-max mb-8">
            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center h-64">
                <CarsScrapedGraph />
            </div>
            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center h-64">
                <CarsScrapedPerWeekGraph />
            </div>
            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center h-64">
                <CarsScrapedPerMonthGraph />
            </div>
        </div>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-10 h-max">
            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center">
                <CarBrandsTable />
            </div>
            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center">
                <CarModelsTable />
            </div>
            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center">

                <BestDaysTable />

            </div>
        </div>
    </div>
</template>

<script setup>
import CarsScrapedGraph from './CarsScrapedGraph.vue';
import CarsScrapedPerWeekGraph from './CarsScrapedPerWeekGraph.vue';
import CarsScrapedPerMonthGraph from './CarsScrapedPerMonthGraph.vue';
import CarBrandsTable from './CarBrandsTable.vue';
import CarModelsTable from './CarModelsTable.vue';
import DashboardRepository from '../../services/DashboardRepository';
import BestDaysTable from './BestDaysTable.vue';
import CarsInDatabase from './CarsInDatabase.vue';
import BlueprintsInDatabase from './BlueprintsInDatabase.vue';
import UsersInDatabase from './UsersInDatabase.vue';
import { useStore } from 'vuex';
import { ref } from 'vue';

const store = useStore();

const role = store.state.role;

const isScraping = ref(false);

const start = () => {
    isScraping.value = true;

    DashboardRepository.startScraper().then(() => {
        isScraping.value = false;
    });
}

</script>