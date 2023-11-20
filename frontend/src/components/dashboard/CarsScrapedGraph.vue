<template>
    <Bar itemid="chart" v-if="loaded" id="my-chart-id-3" :options="chartOptions" :data="chartData" />
</template>

<script setup>

import { ref, onMounted } from 'vue';
import DashboardRepository from '../../services/DashboardRepository';
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend);

const data = ref([]);
const loaded = ref(false);
const dates = ref([]);
const carsScraped = ref([]);

const chartData = ref({});

onMounted(async () => {
    data.value = await DashboardRepository.getCarsScrapedPerDay(7);

    for (var i = 0; i < data.value.length; i++) {
        dates.value.push(data.value[i].date);
        carsScraped.value.push(data.value[i].cars);
    }

    chartData.value = {
        labels: dates.value,
        datasets: [
            {
                label: 'Cars scraped',
                backgroundColor: '#f87979',
                data: carsScraped.value
            }
        ]
    };

    loaded.value = true;
});

</script>