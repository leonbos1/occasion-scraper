<template>
    <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
      <Datatable :input-data="blueprints" v-if="blueprints.length > 0" :input-columns="columns" @order-by="order_by" @edit="handleEdit" @create="handleCreate" />
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

  function handleCreate(blueprint) {
    console.log('handleCreate', blueprint);
    BlueprintRepository.createBlueprint(blueprint);
  }
  
  onMounted(async () => {
    try {
      blueprints.value = await BlueprintRepository.getAllBlueprints();
  
      columns.value = ['brand', 'model', 'min_price', 'max_price', 'min_first_registration', 'max_first_registration', 'city', 'max_distance_from_home'];
  
    } catch (error) {
      console.error('Failed to fetch blueprints:', error);
    }
  });
  </script>
  
  <style scoped></style>