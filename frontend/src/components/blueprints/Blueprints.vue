<template>
    <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
      <Datatable :input-data="blueprints" v-if="blueprints.length > 0" :input-columns="columns" @order-by="order_by" @edit="handleEdit" />
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue';
  import Datatable from '../datatables/Datatable.vue';
  import BlueprintRepository from '../../services/BlueprintRepository';
  
  const blueprints = ref([]);
  const columns = ref([]);
  
  function handleEdit(blueprint) {
    BlueprintRepository.updateBlueprint(blueprint);
  }
  
  onMounted(async () => {
    try {
      blueprints.value = await BlueprintRepository.getAllBlueprints();
  
      columns.value = ['brand', 'model', 'max_price', 'min_price'];
  
    } catch (error) {
      console.error('Failed to fetch blueprints:', error);
    }
  });
  </script>
  
  <style scoped></style>