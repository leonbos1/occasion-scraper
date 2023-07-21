<template>
  <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
    <div class="flex flex-col items-center justify-center w-full h-32">
      <perPageComponent class="w-1/4 mr-auto" @option-selected="perPageSelected" />
      <paginationComponent class="w-1/4 ml-auto" :current-page="currentPage"
        :total-pages="Math.ceil(cars.length / perPage)" :has-previous="hasPrevious" :has-next="hasNext"
        @previous="handlePrevious" @next="handleNext" />
    </div>
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
      <table class="w-full text-sm text-left">
        <thead class="text-xs">
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
    <div class="flex flex-col items-center justify-center w-full h-32">
      <perPageComponent class="w-1/4 mr-auto" @option-selected="perPageSelected" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import CarRow from './CarRow.vue';
import perPageComponent from '../datatables/perPageComponent.vue';
import paginationComponent from '../datatables/paginationComponent.vue';

const cars = ref([]);
const selectedCars = ref([]);
const perPage = ref(10);
const currentPage = ref(1);;
const hasNext = ref(true);
const hasPrevious = ref(false);

function perPageData() {
  const start = (currentPage.value - 1) * perPage.value;
  const end = currentPage.value * perPage.value;
  return cars.value.slice(start, end);
}

function perPageSelected(option) {
  perPage.value = option;
};



function checkNextAndPrevious() {
  if (currentPage.value === 1) {
    hasPrevious.value = false;
  }

  else {
    hasPrevious.value = true;
  }

  if (currentPage.value === Math.ceil(cars.value.length / perPage.value)) {
    hasNext.value = false;
  }

  else {
    hasNext.value = true;
  }
}

function handleNext() {
  currentPage.value++;

  checkNextAndPrevious();
}

function handlePrevious() {
  currentPage.value--;

  checkNextAndPrevious();
}

watch(perPage, () => {
  selectedCars.value = perPageData();
  currentPage.value = 1;
  checkNextAndPrevious();
});

watch(currentPage, () => {
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