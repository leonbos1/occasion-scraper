<template>
  <Datatable :input-data="cars" v-if="cars.length > 0" :input-columns="columns" :maximumPage="maxPage" @order-by="order_by" @edit="handleEdit"
    :key="datatableKey" @updatePerPage="handlePerPageUpdate" @updateCurrentPage="handleCurrentPageUpdate" />
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Datatable from '../datatables/Datatable.vue';
import CarRepository from '../../services/CarRepository';

const cars = ref([]);
const columns = ref([]);
const datatableKey = ref(0);
const perPage = ref(10);
const currentPage = ref(1);
const maxPage = ref(1000);

function handleEdit(car) {
  CarRepository.updateCar(car);
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

    columns.value = ['brand', 'model', 'first_registration', 'price', 'mileage', 'location', 'url', 'base_image'];

    setMaxPage();
  } catch (error) {
    console.error('Failed to fetch cars:', error);
  }
});

async function setPageCars(page, size) {
  var newCars = await CarRepository.getCarsByPage(page, size);

  cars.value = newCars;
}

async function setMaxPage() {
  maxPage.value = await CarRepository.getMaxPage(perPage.value);

  console.log('maxPage.value:', maxPage.value);
}


</script>

<style scoped></style>