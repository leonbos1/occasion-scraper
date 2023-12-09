<template>
  <div class="flex justify-between items-center mb-4">
    <PaginationComponent :maximumPage="maxPage" :currentPage="currentPage" @next="handleNextPage" @previous="handlePreviousPage" class="max-w-[30%]" />
    <PerPageComponent @option-selected="handlePerPageUpdate" class="max-w-[30%]" />
  </div>
  <div class="container mx-auto max-w-[70vw] px-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
    <div v-for="car in cars" :key="car.id" class="col-span-1 justify-center">
      <div class="card">
        <div class="">
          <h1 class="font-bold">{{ car.brand }} {{ car.model }}</h1>
          <p class="">{{ car.price }} €</p>
          <p class="">{{ car.mileage }} km</p>
          <p class="">{{ car.first_registration }}</p>
          <p class="">{{ car.location }}</p>
          <img :src="car.base_image" class="card-img-top" alt="...">
          <a :href="car.url" class="btn btn-primary">Go to offer</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import CarRepository from '../../services/CarRepository';
import PaginationComponent from '../datatables/PaginationComponent.vue';
import PerPageComponent from '../datatables/PerPageComponent.vue';

const cars = ref([]);
const columns = ref([]);
const datatableKey = ref(0);
const perPage = ref(10);
const currentPage = ref(1);
const maxPage = ref(1000);
const orderBy = ref('created');
const orderDirection = ref('desc');
const loading = ref(true);

function handleOrderBy(column) {
  if (orderBy.value === column) {
    orderDirection.value = orderDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    orderDirection.value = 'asc';
  }

  orderBy.value = column;

  setPageCars(currentPage.value, perPage.value);
}

function handleEdit(car) {
  CarRepository.updateCar(car);
}

function handlePreviousPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
  console.log('handlePreviousPage', currentPage.value, maxPage.value);
  setPageCars(currentPage.value, perPage.value);
}

function handleNextPage() {
  if (currentPage.value < maxPage.value) {
    currentPage.value++;
  }
  console.log('handleNextPage', currentPage.value, maxPage.value);
  setPageCars(currentPage.value, perPage.value);
}

function handlePerPageUpdate(newVal) {
  perPage.value = newVal;
  currentPage.value = 1;
  setPageCars(currentPage.value, perPage.value);
  setMaxPage();
}

function handleCurrentPageUpdate(newVal) {
  currentPage.value = newVal;

  setPageCars(currentPage.value, perPage.value);
}

onMounted(async () => {
  try {
    setPageCars(currentPage.value, perPage.value);

    setMaxPage();
  } catch (error) {
    console.error('Failed to fetch cars:', error);
  }
});

async function setPageCars(page, size) {
  loading.value = true;
  var newCars = await CarRepository.getCarsByPage(page, size, orderBy.value, orderDirection.value);
  loading.value = false;

  cars.value = newCars;
}

async function setMaxPage() {
  maxPage.value = await CarRepository.getMaxPage(perPage.value);
}


</script>

<style scoped></style>