<template>
  <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
    <Datatable :input-data="blueprints" :maximum-page="maxPage" v-if="blueprints.length > 0" :input-columns="columns"
      @order-by="order_by" @edit="handleEdit" @create="handleCreate" @updatePerPage="handlePerPageUpdate" @updateCurrentPage="handleCurrentPageUpdate" />
      </div>
</template>
  
<script setup>
import { ref, onMounted, watch } from 'vue';
import Datatable from '../datatables/Datatable.vue';
import BlueprintRepository from '../../services/BlueprintRepository';

const blueprints = ref([]);
const columns = ref([]);
const perPage = ref(10);
const currentPage = ref(1);
const maxPage = ref(1000);

function handleEdit(blueprint) {
  BlueprintRepository.updateBlueprint(blueprint);
}

function handleCreate(blueprint) {
  BlueprintRepository.createBlueprint(blueprint);
}

async function setMaxPage() {
  maxPage.value = await BlueprintRepository.getMaxPage(perPage.value);
}

function handlePerPageUpdate(newVal) {
  perPage.value = newVal;
  currentPage.value = 1;
  setPageBlueprints(currentPage.value, perPage.value);
  setMaxPage();
}

function handleCurrentPageUpdate(newVal) {
  currentPage.value = newVal;

  setPageBlueprints(currentPage.value, perPage.value);
}

async function setPageBlueprints(page, size) {
  var newBlueprints = await BlueprintRepository.getBlueprintsByPage(page, size);

  blueprints.value = newBlueprints;
}


onMounted(async () => {
  try {
    setPageBlueprints(currentPage.value, perPage.value);

    columns.value = ['name', 'brand', 'model', 'min_price', 'max_price', 'min_first_registration', 'max_first_registration', 'city', 'max_distance_from_home'];

    await setMaxPage();
  } catch (error) {
    console.error('Failed to fetch blueprints:', error);
  }
});
</script>
  
<style scoped></style>