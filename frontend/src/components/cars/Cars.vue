<template>
  <div class="flex justify-between items-center mb-4">
    <OrderByComponent @option-selected="handleOrderBy" class="max-w-xs" />
    <PaginationComponent :maximumPage="maxPage" :currentPage="currentPage" @next="handleNextPage"
      @previous="handlePreviousPage" class="max-w-xs" />
    <PerPageComponent @option-selected="handlePerPageUpdate" class="max-w-xs" />
  </div>

  <div class="flex flex-col md:flex-row justify-center">
    <button @click="showFilters = !showFilters" class="md:hidden bg-blue-500 text-white px-4 py-2 rounded m-4">
      {{ showFilters ? 'Hide Filters' : 'Show Filters' }}
    </button>

    <div v-if="showFilters || !isMobile" class="w-full md:w-auto md:flex-shrink-0 md:mr-4">
      <FilterComponent @filter="handleFilter" />
    </div>
    <div class="flex-grow">
      <div class="flex flex-wrap justify-center">
        <div v-for="car in cars" :key="car.id" class="w-full md:w-1/2 lg:w-1/3 xl:w-1/4 p-2">
          <div class="bg-white shadow-lg rounded-lg overflow-hidden h-full">
            <img :src="car.base_image" class="w-full h-44 object-cover object-center" alt="Car Image">
            <div class="p-4">
              <h1 class="font-bold text-lg">{{ car.brand }} {{ car.model }}</h1>
              <p class="text-gray-700">{{ car.price }} €</p>
              <p class="text-gray-600">{{ car.mileage }} km</p>
              <p class="text-gray-600">{{ car.first_registration }}</p>
              <p class="text-gray-600 mb-4">{{ car.location }}</p>
              <div>
                <a :href="car.url" class="inline-block bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">Go to
                  offer</a>
                <button @click="viewInfo(car)" class="ml-2 bg-gray-200 py-2 px-4 rounded hover:bg-gray-300">View
                  Info</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import CarRepository from '../../services/CarRepository';
import PaginationComponent from '../datatables/PaginationComponent.vue';
import PerPageComponent from '../datatables/PerPageComponent.vue';
import OrderByComponent from './OrderByComponent.vue';
import FilterComponent from './FilterComponent.vue';
import { useRouter } from 'vue-router';

const cars = ref([]);
const columns = ref([]);
const datatableKey = ref(0);
const perPage = ref(10);
const currentPage = ref(1);
const maxPage = ref(1000);
const orderBy = ref('created');
const orderDirection = ref('desc');
const loading = ref(true);
const router = useRouter();
const filters = ref({});
const showFilters = ref(false);

const isMobile = computed(() => window.innerWidth < 768);

function handleFilter(filterValues) {
  filters.value = filterValues;
  setPageCars(currentPage.value, perPage.value);
}

function handleOrderBy(column) {
  orderBy.value = column.split(' ')[0];
  orderDirection.value = column.split(' ')[1];

  setPageCars(currentPage.value, perPage.value);
}

function handleEdit(car) {
  CarRepository.updateCar(car);
}

function viewInfo(car) {
  router.push({ name: 'CarInfo', params: { id: car.id } });
}

function handlePreviousPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
  setPageCars(currentPage.value, perPage.value);
}

function handleNextPage() {
  if (currentPage.value < maxPage.value) {
    currentPage.value++;
  }
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

  var newCars = await CarRepository.getCarsByPage(page, size, orderBy.value, orderDirection.value, filters.value);

  loading.value = false;

  cars.value = newCars;
}

async function setMaxPage() {
  maxPage.value = await CarRepository.getMaxPage(perPage.value);
}


</script>

<style scoped></style>