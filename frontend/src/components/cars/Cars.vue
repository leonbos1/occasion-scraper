<template>
  <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
    <Datatable :input-data="cars" v-if="cars.length > 0" :input-columns="columns" @order-by="order_by" @edit="handleEdit"
      :key="datatableKey" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Datatable from '../datatables/Datatable.vue';
import CarRepository from '../../services/CarRepository';

const cars = ref([]);
const columns = ref([]);
const datatableKey = ref(0); // Add this line

function handleEdit(car) {
  CarRepository.updateCar(car);
}

onMounted(async () => {
  try {
    setTop100Cars();

    columns.value = ['brand', 'model', 'first_registration', 'price', 'mileage', 'location', 'url', 'base_image'];

    setAllCars();

  } catch (error) {
    console.error('Failed to fetch cars:', error);
  }
});

async function setTop100Cars() {
  cars.value = await CarRepository.getTop100Cars();
}

async function setAllCars() {
  var newCars = await CarRepository.getAllCars();
  addNewCars(newCars);
  datatableKey.value += 1;
}

async function addNewCars(newCars) {
  var newCarsIds = newCars.map(car => car.id);
  var carsIds = cars.value.map(car => car.id);

  newCars.forEach(car => {
    car.url = CarRepository.api_url + '/cars/image/' + car.id;
  });

  var newCarsIdsNotInCarsIds = newCarsIds.filter(id => !carsIds.includes(id));

  var newCarsNotInCars = newCars.filter(car => newCarsIdsNotInCarsIds.includes(car.id));

  cars.value = cars.value.concat(newCarsNotInCars);
}

</script>

<style scoped></style>