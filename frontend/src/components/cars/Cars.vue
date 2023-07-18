<template>
    <DataTable id="carTable" :data="cars" :columns="dataTableColumns" class="display nowrap" />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net-bs5';

DataTable.use(DataTablesCore);

const cars = ref([]);

const dataTableColumns = [
  { data: 'brand', title: 'Brand' },
  { data: 'model', title: 'Model' },
  { data: 'price', title: 'Price' },
  { data: 'mileage', title: 'Mileage' },
  { data: 'location', title: 'Location' },
  { data: 'first_registration', title: 'First Registration' },
  { data: 'url', title:'Url' },
];

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