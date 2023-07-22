<template>
  <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
    <Datatable :input-data="cars" v-if="cars.length > 0" :input-columns="columns" @order-by="order_by" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Datatable from '../datatables/Datatable.vue';
import CarRepository from '../../services/CarRepository';

const cars = ref([]);
const columns = ref([]);

onMounted(async () => {
  try {
    cars.value = await CarRepository.getAllCars();

    columns.value = Object.keys(cars.value[0]);

  } catch (error) {
    console.error('Failed to fetch cars:', error);
  }
});
</script>

<style scoped></style>