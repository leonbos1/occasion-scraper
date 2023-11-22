<template>
  <Datatable :input-data="cars" v-if="cars.length > 0" :input-columns="columns" :maximumPage="maxPage" :loading="loading"
    :order-by="orderBy" @edit="handleEdit" :key="datatableKey" @updatePerPage="handlePerPageUpdate"
    @updateCurrentPage="handleCurrentPageUpdate" @order_by="handleOrderBy" />
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

    columns.value = ['created', 'brand', 'model', 'first_registration', 'price', 'mileage', 'location', 'url', 'base_image'];

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