<template>
  <div>
    <perPageComponent @option-selected="perPageSelected" />
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
          <CarRow v-for="car in selectedCars" :key="car.id" :car="car" />
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import CarRow from './CarRow.vue';
import perPageComponent from '../datatables/perPageComponent.vue';

const cars = ref([]);
const selectedCars = ref([]);
const perPage = ref(10);

function perPageData() {
  return cars.value.slice(0, perPage.value);
}

function perPageSelected(option) {
  perPage.value = option;
};

watch(perPage, () => {
  selectedCars.value = perPageData();
});

onMounted(async () => {
  try {
    const response = await fetch('http://192.168.68.138:8000/cars');
    const data = await response.json();
    cars.value = data;
    selectedCars.value = perPageData();
  } catch (error) {
    console.error('Failed to fetch cars:', error);
  }
});
</script>

<style scoped></style>