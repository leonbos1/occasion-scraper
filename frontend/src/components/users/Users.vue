<template>
  <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
    <Datatable :input-data="users" v-if="users.length > 0" :input-columns="columns" @order-by="order_by" @edit="handleEdit" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Datatable from '../datatables/Datatable.vue';
import UserRepository from '../../services/UserRepository';

const users = ref([]);
const columns = ref([]);

function handleEdit(user) {
  UserRepository.updateUser(user);
}

onMounted(async () => {
  try {
    users.value = await UserRepository.getAllUsers();

    columns.value = Object.keys(users.value[0]);

  } catch (error) {
    console.error('Failed to fetch users:', error);
  }
});
</script>

<style scoped></style>