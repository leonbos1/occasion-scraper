<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <div class="flex justify-center mb-4">
      <RecentCars />
    </div>
    <div class="flex justify-center">
      <MostExpensiveCars />
    </div>
  </div>
</template>
  
<script setup>
import RecentCars from '../cars/RecentCars.vue';
import MostExpensiveCars from '../cars/MostExpensiveCars.vue';

</script>