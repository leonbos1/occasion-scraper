<template>
  <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
    <Datatable :input-data="cars" v-if="cars.length > 0" :input-columns="columns" @order-by="order_by" @edit="handleEdit" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Datatable from '../datatables/Datatable.vue';
import CarRepository from '../../services/CarRepository';

const cars = ref([]);
const columns = ref([]);

function handleEdit(car) {
  CarRepository.updateCar(car);
}

onMounted(async () => {
  try {
    cars.value = await CarRepository.getAllCars();

    columns.value = ['brand', 'model', 'year', 'price', 'base_image'];

  } catch (error) {
    console.error('Failed to fetch cars:', error);
  }
});
</script>

<style scoped></style>