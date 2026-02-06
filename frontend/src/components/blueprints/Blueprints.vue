<template>
  <div class="flex justify-between items-center mb-4 w-full">
    <a href="/blueprints/create" class=" left-0 bg-blue-500 text-white px-4 py-2 rounded m-4">
      Create Blueprint</a>
    <OrderByComponent @option-selected="handleOrderBy" class="max-w-xs" />
    <PaginationComponent :maximumPage="maxPage" :currentPage="currentPage" @next="handleNextPage"
      @previous="handlePreviousPage" class="max-w-xs" />
    <PerPageComponent @option-selected="handlePerPageUpdate" class="max-w-xs" />
  </div>

  <div class="flex flex-col md:flex-row justify-center">
    <button @click="showFilters = !showFilters" class="md:hidden bg-blue-500 text-white px-4 py-2 rounded m-4">
      {{ showFilters ? 'Hide Filters' : 'Show Filters' }}
    </button>

    <div v-if="showFilters || !isMobile" class="w-full md:w-auto md:flex-shrink-0 md:mr-4">
      <FilterComponent @filter="handleFilter" />
    </div>
    <div class="flex-grow">
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="text-xl text-gray-600">Loading blueprints...</div>
      </div>
      <div v-else-if="!blueprints || blueprints.length === 0" class="flex flex-col justify-center items-center h-64 bg-white rounded-lg shadow-lg m-4">
        <svg class="w-24 h-24 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <h3 class="text-2xl font-semibold text-gray-700 mb-2">No Blueprints Found</h3>
        <p class="text-gray-500 text-center max-w-md mb-4">
          Create a blueprint to define search criteria for car listings. Blueprints help you automate car searches with specific filters.
        </p>
        <a href="/blueprints/create" class="bg-blue-500 text-white px-6 py-3 rounded hover:bg-blue-600 font-semibold">
          Create Your First Blueprint
        </a>
      </div>
      <BlueprintsCardView v-else :blueprints="blueprints" />
    </div>
  </div>
</template>
  
<script setup>
import { ref, onMounted, watch } from 'vue';
import BlueprintRepository from '../../services/BlueprintRepository';
import SubscriptionRepository from '../../services/SubscriptionRepository';
import PerPageComponent from '../datatables/PerPageComponent.vue';
import PaginationComponent from '../datatables/PaginationComponent.vue';
import BlueprintsCardView from './BlueprintsCardView.vue';

const blueprints = ref([]);
const perPage = ref(10);
const currentPage = ref(1);
const maxPage = ref(1000);
const editBlueprint = ref(null);
const loading = ref(true);

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
  loading.value = true;
  try {
    blueprints.value = await BlueprintRepository.getBlueprintsByPage(page, size);
  } catch (error) {
    console.error('Failed to fetch blueprints:', error);
    blueprints.value = [];
  } finally {
    loading.value = false;
  }
}

async function handleEditBlueprint(blueprint, selectedUsers) {
  await addNewUsersToBlueprint(blueprint, selectedUsers);

  await removeOldUsersFromBlueprint(blueprint, selectedUsers);

  await BlueprintRepository.updateBlueprint(blueprint);
}

async function addNewUsersToBlueprint(blueprint, selectedUsers) {
  selectedUsers.forEach(async (user) => {
    const subscription = blueprint.subscriptions.find(sub => sub.user.id === user);

    if (!subscription) {
      var newSubscription = {
        user_id: user,
        blueprint_id: blueprint.id
      }

      await SubscriptionRepository.addSubscription(newSubscription);
    }
  });
}

async function removeOldUsersFromBlueprint(blueprint, selectedUsers) {
  blueprint.subscriptions.forEach(async (subscription) => {
    if (!selectedUsers.includes(subscription.user.id)) {
      await SubscriptionRepository.deleteSubscription(subscription);
    }
  });
}

onMounted(async () => {
  try {
    setPageBlueprints(currentPage.value, perPage.value);

    await setMaxPage();
  } catch (error) {
    console.error('Failed to fetch blueprints:', error);
  }
});
</script>
  
<style scoped></style>