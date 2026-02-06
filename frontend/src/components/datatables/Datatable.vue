<template>
    <div class=" w-full px-4 py-10 sm:px-6 lg:px-8 lg:py-14 mx-auto">
        <div v-if="props.loading || data.length === 0"
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
        <div class="flex flex-col">
            <div
                class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden dark:bg-slate-900 dark:border-gray-700">
                <div
                    class="px-6 py-4 grid gap-3 md:flex md:justify-between md:items-center border-b border-gray-200 dark:border-gray-700">
                    <div class="flex flex-row w-full h-32">
                        <div class="flex flex-row items-center justify-start w-1/4">
                            <PerPageComponent @option-selected="perPageSelected" />
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
                                data-hs-overlay="#hs-modal-create" @click="editItem = null">
                                Create
                            </a>
                        </div>
                    </div>
                </div>

                <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
                    <table class="min-w-full max-w-full divide-y divide-gray-200 dark:divide-gray-700">
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
                            <tr v-for="row in data" :key="row.id" class="w-1/12">
                                <td v-for="column in columns" :key="column"
                                    class="h-px whitespace-nowrap overflow-hidden w-px">
                                    <div class="pl-6 py-3">
                                        <template v-if="column === 'base_image'">
                                            <img :src="getImageSrc(row[column])" class="w-1/2 h-1/2 " />
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
                                            data-hs-overlay="#hs-modal-signup" @click="editItem = row">
                                            Edit
                                        </a>

                                    </div>
                                </td>
                            </tr>
                        </tbody>
                        <EditComponent :item="editItem" v-if="editItem" @edit="handleEdit" />
                        <CreateComponent :item="createItem" v-if="createItem" @create="handleCreate" />
                    </table>
                </div>
                <div class="flex flex-col items-center justify-center w-full h-32">
                    <PerPageComponent class="w-1/4 mr-auto" @option-selected="perPageSelected" />
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted, watch, defineProps, defineEmits } from 'vue';
import getImageSrc from '../../utils/imagehelper';
import PerPageComponent from '@/components/datatables/PerPageComponent.vue';
import PaginationComponent from '@/components/datatables/PaginationComponent.vue';
import SearchComponent from '@/components/datatables/SearchComponent.vue';
import EditComponent from '@/components/datatables/EditComponent.vue'
import CreateComponent from '@/components/datatables/CreateComponent.vue'

const data = ref([]);
const columns = ref([]);

const props = defineProps(['inputData', 'inputColumns', 'maximumPage', 'loading', 'order_by']);

const perPage = ref(10);
const currentPage = ref(1);;
const hasNext = ref(false);
const hasPrevious = ref(false);
const editItem = ref(null);
const createItem = ref(null);

const emit = defineEmits(['edit', 'create', 'order_by']);

function handleEdit(item) {
    emit('edit', item);
}

function handleCreate(item) {
    emit('create', item);
}

watch(perPage, (newVal) => {
    emit('updatePerPage', newVal);
});

watch(currentPage, (newVal) => {
    emit('updateCurrentPage', newVal);
});

function handleOrderBy(column) {
    currentPage.value = 1;
    emit('order_by', column);
}

function handleNext() {
    if (hasNext.value) {
        currentPage.value++;
        checkNextAndPrevious();
    }
}

function handlePrevious() {
    if (hasPrevious.value) {
        currentPage.value--;
        checkNextAndPrevious();
    }
}

function checkNextAndPrevious() {
    if (currentPage.value === 1) {
        hasPrevious.value = false;
    }

    else {
        hasPrevious.value = true;
    }

    if (currentPage.value === props.maximumPage) {
        hasNext.value = false;
    }

    else {
        hasNext.value = true;
    }
}

function perPageSelected(selectedOption) {
    perPage.value = selectedOption;
    currentPage.value = 1;
}

function handleSearch(search) {
    if (search === '') {
        filteredData.value = data.value;
    }

    else {
        filteredData.value = data.value.filter((row) => {
            return Object.values(row).some((column) => {
                return String(column).toLowerCase().includes(search.toLowerCase());
            });
        });
    }

    currentPage.value = 1;

    checkNextAndPrevious();
}

watch(perPage, () => {
    console.log('per page changed');
});

watch(currentPage, () => {
    console.log('current page changed');
});

watch(() => props.inputData, () => {
    data.value = props.inputData;
});

onMounted(() => {
    data.value = props.inputData;

    columns.value = props.inputColumns;

    checkNextAndPrevious();
});

</script>