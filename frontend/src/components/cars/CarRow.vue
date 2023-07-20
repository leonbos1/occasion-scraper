<template>
    <tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700">
      <td class="px-2 py-2">{{ car.id }}</td>
      <td class="px-6 py-2">{{ car.brand }}</td>
      <td class="px-6 py-2">{{ car.model }}</td>
      <td class="px-6 py-2">{{ car.price }}</td>
      <td class="px-6 py-2">{{ car.mileage }}</td>
      <td class="px-6 py-2">{{ car.location }}</td>
      <td class="px-6 py-2">{{ car.first_registration }}</td>
      <td class="px-6 py-2">{{ car.vehicle_type }}</td>
      <td class="px-6 py-2">{{ car.created }}</td>
      <td class="px-6 py-2">{{ car.updated }}</td>
      <td class="px-6 py-2"><a :href="car.url" target="_blank">Link</a></td>
      <td class="px-6 py-2">{{ car.image }}</td>
    </tr>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  
  defineProps({
    car: {
      type: Object,
      required: true
    }
  });
  </script>
  
  <style scoped>
  </style>
  