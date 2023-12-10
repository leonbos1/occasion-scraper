<template>
    <div class="container mx-auto p-4">
        <div class="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-10 h-max mb-8">
            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center h-64">
                <CarsScrapedGraph />
            </div>
            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center h-64">
                <CarsScrapedGraph />
            </div>
            <div
                class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex justify-center items-center h-64">
                <CarsScrapedGraph />
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

                <button v-if="role == '1'" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    @click="start">Start</button>

            </div>
        </div>
    </div>
</template>

<script setup>
import CarsScrapedGraph from './CarsScrapedGraph.vue';
import CarBrandsTable from './CarBrandsTable.vue';
import CarModelsTable from './CarModelsTable.vue';
import { useStore } from 'vuex';

const store = useStore();

const role = store.state.role;

const start = () => {
    fetch('http://leonbos.nl:5000/start')
        .then(response => response.json());
}

</script>