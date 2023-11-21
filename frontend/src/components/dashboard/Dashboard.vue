<template>
    <div class="container mx-auto p-4">
        <div class="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-10 h-max">
            <div class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 h-max">
                <CarsScrapedGraph />
            </div>
            <div class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 h-max">
                <CarsScrapedGraph />
            </div>
            <div class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 h-max">
                <CarsScrapedGraph />
            </div>
        </div>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-10 h-max">
            <div class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 h-max">

            </div>
            <div class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 h-max">
            </div>
            <div class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 h-max">
            </div>
        </div>
        <p>sample</p>
    </div>
</template>

<script setup>

import CarsScrapedGraph from './CarsScrapedGraph.vue';

</script>