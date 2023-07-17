<template>
    <tr class="bg-white border-b dark:bg-gray-900 dark:border-gray-700">
      <td class="px-6 py-4">{{ user.id }}</td>
      <td class="px-6 py-4">{{ user.email }}</td>
      <td class="px-6 py-4">{{ user.password }}</td>
    </tr>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  
  defineProps({
    user: {
      type: Object,
      required: true
    }
  });
  </script>
  
  <style scoped>
  </style>
  