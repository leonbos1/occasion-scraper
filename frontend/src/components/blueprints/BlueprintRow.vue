<template>
    <tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700">
      <td class="px-6 py-4">{{ blueprint.id }}</td>
      <td class="px-6 py-4">{{ blueprint.brand }}</td>
      <td class="px-6 py-4">{{ blueprint.model }}</td>
      <td class="px-6 py-4">{{ blueprint.min_price }}</td>
      <td class="px-6 py-4">{{ blueprint.max_price }}</td>
      <td class="px-6 py-4">{{ blueprint.min_mileage }}</td>
      <td class="px-6 py-4">{{ blueprint.max_mileage }}</td>
      <td class="px-6 py-4">{{ blueprint.min_first_registration }}</td>
      <td class="px-6 py-4">{{ blueprint.max_first_registration }}</td>
      <td class="px-6 py-4">{{ blueprint.vehicle_type }}</td>
      <td class="px-6 py-4">{{ blueprint.owner_id }}</td>
      <td class="px-6 py-4">{{ blueprint.city }}</td>
      <td class="px-6 py-4">{{ blueprint.created }}</td>
      <td class="px-6 py-4">{{ blueprint.updated }}</td>
      <td class="px-6 py-4">{{ blueprint.max_distance_from_home }}</td>
    </tr>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  
  defineProps({
    blueprint: {
      type: Object,
      required: true
    }
  });
  </script>
  
  <style scoped>
  </style>
  