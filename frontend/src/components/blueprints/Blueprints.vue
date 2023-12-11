<template>
  <div class="flex justify-between items-center mb-4">
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
      <BlueprintsCardView v-if="blueprints.length > 0" :blueprints="blueprints" />
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
  blueprints.value = await BlueprintRepository.getBlueprintsByPage(page, size);
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