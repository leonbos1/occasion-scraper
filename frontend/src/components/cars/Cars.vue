<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="flex flex-col gap-4 mb-6">
      <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-3">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Cars</h1>
          <p class="text-sm text-gray-500">Browse scraped listings and filter by your preferences.</p>
        </div>
        <div class="flex items-center gap-2 text-sm text-gray-500">
          <span class="font-medium text-gray-700">Page</span>
          <span class="px-2 py-1 rounded bg-gray-100 text-gray-700">{{ currentPage }} / {{ maxPage }}</span>
        </div>
      </div>

      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3">
        <div class="flex flex-wrap items-center gap-3">
          <div class="bg-white border border-gray-200 rounded-lg px-3 py-2 shadow-sm">
            <OrderByComponent @option-selected="handleOrderBy" class="max-w-xs" />
          </div>
          <div class="bg-white border border-gray-200 rounded-lg px-3 py-2 shadow-sm">
            <PerPageComponent @option-selected="handlePerPageUpdate" class="max-w-xs" />
          </div>
          <button @click="showFilters = !showFilters" class="md:hidden inline-flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
            <span>{{ showFilters ? 'Hide Filters' : 'Show Filters' }}</span>
          </button>
        </div>
        <div class="bg-white border border-gray-200 rounded-lg px-3 py-2 shadow-sm">
          <PaginationComponent :maximumPage="maxPage" :currentPage="currentPage" @next="handleNextPage"
            @previous="handlePreviousPage" class="max-w-xs" />
        </div>
      </div>
    </div>

    <div class="flex flex-col md:flex-row gap-4">
      <div v-if="showFilters || !isMobile" class="w-full md:w-72 md:flex-shrink-0">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-3">
          <FilterComponent @filter="handleFilter" />
        </div>
      </div>
      <div class="flex-grow">
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="text-xl text-gray-600">Loading cars...</div>
        </div>
        <div v-else-if="!cars || cars.length === 0" class="flex flex-col justify-center items-center h-64 bg-white rounded-xl shadow-sm border border-gray-200">
          <svg class="w-24 h-24 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <h3 class="text-2xl font-semibold text-gray-700 mb-2">No Cars Found</h3>
          <p class="text-gray-500 text-center max-w-md">
            There are currently no cars in the database. Try running a scraper to populate the database with car listings.
          </p>
        </div>
        <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <div v-for="car in cars" :key="car.id" class="group">
            <div class="bg-white shadow-sm border border-gray-200 rounded-xl overflow-hidden h-full transition hover:shadow-lg hover:-translate-y-0.5">
              <div class="relative">
                <img :src="getImageSrc(car.base_image) || placeholderImage" class="w-full h-44 object-cover object-center" alt="Car Image">
                <span class="absolute top-3 left-3 bg-white/90 text-gray-700 text-xs font-semibold px-2 py-1 rounded-full">{{ car.first_registration }}</span>
              </div>
              <div class="p-4 flex flex-col">
                <div class="flex items-start justify-between gap-2">
                  <h1 class="font-semibold text-gray-900 leading-tight">{{ car.brand }} {{ car.model }}</h1>
                  <span class="text-sm font-semibold text-green-600 whitespace-nowrap">€ {{ formatPrice(car.price) }}</span>
                </div>
                <div class="text-sm text-gray-600 flex flex-wrap gap-2 mt-2">
                  <span class="bg-gray-100 rounded-full px-2 py-1">{{ formatMileage(car.mileage) }} km</span>
                  <span class="bg-gray-100 rounded-full px-2 py-1">{{ car.location }}</span>
                </div>
              </div>
              <div class="px-4 pb-4">
                <div class="flex items-center gap-2">
                  <a :href="getOfferUrl(car.url)" target="_blank" rel="noopener"
                    class="inline-flex items-center justify-center flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700">Go to offer</a>
                  <button @click="viewInfo(car)" class="inline-flex items-center justify-center flex-1 bg-gray-100 py-2 rounded-lg hover:bg-gray-200">View info</button>
                </div>
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
import getImageSrc from '../../utils/imagehelper';

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
const placeholderImage = `data:image/svg+xml;utf8,${encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400"><rect width="600" height="400" fill="#f3f4f6"/><path d="M140 280h320l-50-80h-220l-50 80z" fill="#d1d5db"/><circle cx="220" cy="300" r="24" fill="#9ca3af"/><circle cx="380" cy="300" r="24" fill="#9ca3af"/><text x="300" y="170" text-anchor="middle" font-family="Arial" font-size="20" fill="#9ca3af">No image</text></svg>')}`;

function formatPrice(value) {
  if (value === null || value === undefined) {
    return '-';
  }
  return new Intl.NumberFormat('nl-NL').format(value);
}

function formatMileage(value) {
  if (value === null || value === undefined) {
    return '-';
  }
  return new Intl.NumberFormat('nl-NL').format(value);
}

function getOfferUrl(url) {
  if (!url) {
    return '#';
  }
  return url.startsWith('http') ? url : `https://www.autoscout24.nl${url}`;
}

function handleFilter(filterValues) {
  filters.value = filterValues;
  setPageCars(currentPage.value, perPage.value);
  setMaxPage();
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
    setPageCars(currentPage.value, perPage.value);
  }
}

function handleNextPage() {
  if (currentPage.value < maxPage.value) {
    currentPage.value++;
    setPageCars(currentPage.value, perPage.value);
  }
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
  try {
    const newCars = await CarRepository.getCarsByPage(page, size, orderBy.value, orderDirection.value, filters.value);
    cars.value = newCars;
  } finally {
    loading.value = false;
  }
}

async function setMaxPage() {
  maxPage.value = await CarRepository.getMaxPage(perPage.value);
  if (currentPage.value > maxPage.value && maxPage.value > 0) {
    currentPage.value = maxPage.value;
    setPageCars(currentPage.value, perPage.value);
  }
}


</script>

<style scoped></style>