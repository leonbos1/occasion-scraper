<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="px-6 py-3">Id</th>
          <th scope="col" class="px-6 py-3">Email</th>
          <th scope="col" class="px-6 py-3">Password</th>
        </tr>
      </thead>
      <tbody>
        <UserRow v-for="user in users" :key="user.id" :user="user" />
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import UserRow from './UserRow.vue';
import credentials from '../../../../credentials.json';

const users = ref([]);

onMounted(async () => {
  
  var api_key = credentials.api_key;

  try {
    const response = await fetch('http://192.168.68.138:8000/users', {
      headers: {
        'X-API-Key' : api_key
      }
    });
    const data = await response.json();
    users.value = data;
  } catch (error) {
    console.error('Failed to fetch users:', error);
  }
});
</script>

<style scoped>
/* Add your custom styles here */
</style>
