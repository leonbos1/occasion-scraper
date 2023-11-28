<template>
    <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400 border rounded-xl">
        <div class="w-full px-4 py-10 sm:px-6 lg:px-8 lg:py-14 mx-auto">
            <div v-if="loading || subscriptions.length === 0"
                class="absolute top-0 left-0 w-full h-full flex justify-center items-center bg-gray-500 bg-opacity-50 z-10">
                <svg aria-hidden="true" class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                    viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                        fill="currentColor" />
                    <path
                        d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                        fill="currentFill" />
                </svg>
                <span class="sr-only">Loading...</span>
            </div>
            <div class="flex flex-col h-auto">
                <div
                    class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden dark:bg-slate-900 dark:border-gray-700 h-[75vh]">
                    <div
                        class="px-6 py-4 grid gap-3 md:flex md:justify-between md:items-center border-b border-gray-200 dark:border-gray-700">
                        <div class="flex flex-row w-full h-32">
                            <div class="flex flex-row items-center justify-start w-1/4">
                                <PerPageComponent @option-selected="handlePerPageUpdate" />
                            </div>
                            <div class="flex flex-row items-center justify-center w-1/2">
                                <PaginationComponent :current-page="currentPage" :maximum-page="maximumPage"
                                    :has-previous="hasPrevious" :has-next="hasNext" @previous="handlePrevious"
                                    @next="handleNext" />
                            </div>
                            <div class="flex flex-row items-center justify-center w-1/2">
                                <SearchComponent @search="handleSearch" />
                            </div>
                            <div class="flex flex-row items-center justify-center w-1/2">
                                <a class="inline-flex items-center gap-x-1.5 text-sm text-blue-600 decoration-2 hover:underline font-medium"
                                    data-hs-overlay="#hs-modal-create" @click="editSubscription = null">
                                    Create
                                </a>
                            </div>
                        </div>
                    </div>

                    <EditSubscriptionComponent :subscription="editSubscription" v-if="editSubscription" />
                    <CreateSubscriptionComponent :subscription="createItem" v-if="createItem" @create="handleCreate" />

                    <div class="relative h-96 overflow-x-auto shadow-md sm:rounded-lg">

                        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                            <thead class="bg-gray-50 dark:bg-slate-800">
                                <tr>
                                    <th v-for="column in columns" :key="column" scope="col"
                                        class="pl-6 lg:pl-3 xl:pl-0 pr-6 py-3 text-left" @click="handleOrderBy(column)">
                                        <div class="flex items-center gap-x-2">
                                            <span
                                                class="text-xs font-semibold uppercase tracking-wide text-gray-800 dark:text-gray-200">
                                                {{ column }}
                                            </span>
                                        </div>
                                    </th>
                                    <th scope="col" class="px-6 py-3 text-right"></th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                                <tr v-for="row in subscriptions" :key="row.id" class="w-1/12">
                                    <td v-for="column in columns" :key="column"
                                        class="h-px whitespace-nowrap overflow-hidden w-px">
                                        <div class="pl-6 py-3">
                                            <template v-if="column === 'base_image'">
                                                <img v-if="row[column] !== ''" :src="row[column]" class="w-1/2 h-1/2 " />

                                                <img v-else :src="setBaseImage(row)" class="w-1/2 h-1/2 " />

                                            </template>
                                            <template v-else-if="column.toLowerCase() === 'url'">
                                                <a :href="row[column]" target="_blank"
                                                    class="inline-flex items-center gap-x-1.5 text-sm text-blue-600 decoration-2 hover:underline font-medium">
                                                    URL
                                                </a>
                                            </template>
                                            <template v-else>
                                                <span
                                                    class="text-xs font-semibold uppercase tracking-wide text-gray-800 dark:text-gray-500">{{
                                                        row[column] }}</span>
                                            </template>
                                        </div>
                                    </td>
                                    <td class="h-px w-px whitespace-nowrap">
                                        <div class="px-6 py-1.5">
                                            <a class="inline-flex items-center gap-x-1.5 text-sm text-blue-600 decoration-2 hover:underline font-medium"
                                                data-hs-overlay="#hs-modal-signup" @click="editSubscription = row">
                                                Edit
                                            </a>

                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="flex flex-col items-center justify-center w-full h-32">
                        <PerPageComponent class="w-1/4 mr-auto" @option-selected="handlePerPageUpdate" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
    
<script setup>
import { ref, onMounted, watch } from 'vue';
import SubscriptionRepository from '../../services/SubscriptionRepository';
import PaginationComponent from '../datatables/PaginationComponent.vue';
import PerPageComponent from '../datatables/PerPageComponent.vue';
import SearchComponent from '../datatables/SearchComponent.vue';
import EditSubscriptionComponent from './EditSubscriptionComponent.vue';
import CreateSubscriptionComponent from './CreateSubscriptionComponent.vue';

const subscriptions = ref([]);
const columns = ref([]);
const perPage = ref(10);
const currentPage = ref(1);
const maximumPage = ref(1);
const loading = ref(true);
const data = ref([]);
const editSubscription = ref(null);

async function setMaxPage() {
    maximumPage.value = await SubscriptionRepository.getMaxPage(perPage.value);
}

async function handlePerPageUpdate(newVal) {
    perPage.value = newVal;
    currentPage.value = 1;
    await setPageSubscriptions(currentPage.value, perPage.value);
    setMaxPage();
}

async function handleCurrentPageUpdate(newVal) {
    currentPage.value = newVal;

    await setPageSubscriptions(currentPage.value, perPage.value);
}

async function setPageSubscriptions(page, size) {
    subscriptions.value = await SubscriptionRepository.getSubscriptionsByPage(page, size);

    console.log(subscriptions.value);

    loading.value = false;
}

onMounted(async () => {
    try {
        await setPageSubscriptions(currentPage.value, perPage.value);

        console.log(subscriptions.value);

        columns.value = ['created', 'updated', 'email', 'blueprint_name'];

        await setMaxPage();
    } catch (error) {
        console.error('Failed to fetch subscriptions:', error);
    }
});
</script>
    
<style scoped></style>