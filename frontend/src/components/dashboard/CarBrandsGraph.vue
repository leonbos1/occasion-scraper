<template>
    <Pie itemid="brandschart" :data="chartData" :options="options" v-if="loaded" />
</template>

<script setup>

import DashboardRepository from '../../services/DashboardRepository';
import { ref, onMounted } from 'vue';
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, ArcElement);

const data = ref({});
const loaded = ref(false);
const brands = ref([]);
const amounts = ref([]);
const options = ref({
    plugins: {
        title: {
            display: true,
            text: 'Car brands',
        },
        legend: {
            display: false,
        },
    },
});

const chartData = ref({});

onMounted(async () => {
    data.value = await DashboardRepository.getCarBrands();

    for (var key in data.value) {
        brands.value.push(key);
        amounts.value.push(data.value[key]);
    }

    chartData.value = {
        labels: brands.value,
        datasets: [
            {
                label: 'Car brands',
                data: amounts.value,
                backgroundColor: ['#F0F8FF',
                    '#FAEBD7',
                    '#00FFFF',
                    '#7FFFD4',
                    '#F0FFFF',
                    '#F5F5DC',
                    '#FFE4C4',
                    '#000000',
                    '#FFEBCD',
                    '#0000FF',
                    '#8A2BE2',
                    '#A52A2A',
                    '#DEB887',
                    '#5F9EA0',
                    '#7FFF00',
                    '#D2691E',
                    '#FF7F50',
                    '#6495ED',
                    '#FFF8DC',
                    '#DC143C',
                    '#00FFFF',
                    '#00008B',
                    '#008B8B',
                    '#B8860B',
                    '#A9A9A9',
                    '#006400',
                    '#A9A9A9',
                    '#BDB76B',
                    '#8B008B',
                    '#556B2F']
            },
        ],
    };

    loaded.value = true;
});

</script>