<template>
  <div>
    <DataTable :data="cars" :columns="dataTableColumns">
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import CarRow from './CarRow.vue';
import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net';
 
DataTable.use(DataTablesCore);

const cars = ref([]);

const dataTableColumns = [
  { data: 'brand' },
  { data: 'model' },
  { data: 'price' },
  { data: 'mileage' },
  { data: 'location' },
  { data: 'first_registration' },
  { data: 'url' },
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

<style scoped>
@import 'datatables.net-dt';
@import 'datatables.net-bs5';
@import 'bootstrap';
</style>
