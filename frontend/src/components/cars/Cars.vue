<template>
  <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
    <Datatable :input-data="cars" v-if="cars.length > 0" :input-columns="columns" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Datatable from '../datatables/Datatable.vue';
import fixBase64Image from '../../utils/imagehelper.js';

const cars = ref([]);
const columns = ref([]);


onMounted(async () => {
  try {
    const response = await fetch('http://192.168.68.138:8000/cars');
    const data = await response.json();
    cars.value = data;
    columns.value = Object.keys(cars.value[0]);
    fixBase64Image(cars);

  } catch (error) {
    console.error('Failed to fetch cars:', error);
  }
});
</script>

<style scoped></style>