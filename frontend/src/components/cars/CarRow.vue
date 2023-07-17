<template>
    <tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700">
      <td class="px-6 py-4">{{ car.brand }}</td>
      <td class="px-6 py-4">{{ car.model }}</td>
      <td class="px-6 py-4">{{ car.price }}</td>
      <td class="px-6 py-4">{{ car.mileage }}</td>
      <td class="px-6 py-4">{{ car.location }}</td>
      <td class="px-6 py-4">{{ car.first_registration }}</td>
      <td class="px-6 py-4"><a :href="car.url" target="_blank">Link</a></td>
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
  