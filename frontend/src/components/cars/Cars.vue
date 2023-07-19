<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="px-6 py-3">Id</th>
          <th scope="col" class="px-6 py-3">Brand</th>
          <th scope="col" class="px-6 py-3">Model</th>
          <th scope="col" class="px-6 py-3">Price</th>
          <th scope="col" class="px-6 py-3">Mileage</th>
          <th scope="col" class="px-6 py-3">City</th>
          <th scope="col" class="px-6 py-3">First Registration</th>
          <th scope="col" class="px-6 py-3">Vehicle Type</th>
          <th scope="col" class="px-6 py-3">Created</th>
          <th scope="col" class="px-6 py-3">Updated</th>
          <th scope="col" class="px-6 py-3">Url</th>
          <th scope="col" class="px-6 py-3">Image</th>
        </tr>
      </thead>
      <tbody>
        <CarRow v-for="car in cars" :key="car.id" :car="car" />
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import CarRow from './CarRow.vue';

const cars = ref([]);

onMounted(async () => {
  try {
    const response = await fetch('http://192.168.68.138:8000/cars');
    const data = await response.json();
    cars.value = data;
  } catch (error) {
    console.error('Failed to fetch cars:', error);
  }
});
</script>

<style scoped></style>