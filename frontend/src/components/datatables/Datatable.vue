<template>
    <div class="max-w-[85rem] px-4 py-10 sm:px-6 lg:px-8 lg:py-14 mx-auto">
        <div class="flex flex-col">
            <div class="-m-1.5 overflow-x-auto">
                <div class="p-1.5 min-w-full inline-block align-middle">
                    <div
                        class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden dark:bg-slate-900 dark:border-gray-700">
                        <div
                            class="px-6 py-4 grid gap-3 md:flex md:justify-between md:items-center border-b border-gray-200 dark:border-gray-700">
                            <div class="flex flex-row w-full h-32">
                                <div class="flex flex-row items-center justify-start w-1/4">
                                    <PerPageComponent @option-selected="perPageSelected" />
                                </div>
                                <div class="flex flex-row items-center justify-center w-1/2">
                                    <PaginationComponent :current-page="currentPage"
                                        :total-pages="Math.ceil(data.length / perPage)" :has-previous="hasPrevious"
                                        :has-next="hasNext" @previous="handlePrevious" @next="handleNext" />
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
                            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                                <thead class="bg-gray-50 dark:bg-slate-800">
                                    <tr>
                                        <th v-for="column in columns" :key="column" scope="col"
                                            class="pl-6 lg:pl-3 xl:pl-0 pr-6 py-3 text-left" @click="setOrderBy(column)">
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
                                    <tr v-for="row in selectedData" :key="row.id">
                                        <td v-for="column in columns" :key="column" class="h-px w-px whitespace-nowrap">
                                            <div class="pl-6 py-3">
                                                <template v-if="column === 'base_image'">
                                                    <img v-if="row[column] !== ''" :src="row[column]"
                                                        class="w-1/2 h-1/2 " />

                                                    <img v-else :src="setBaseImage(row)" class="w-1/2 h-1/2 " />

                                                </template>
                                                <template v-else-if="column.toLowerCase() === 'url'">
                                                    <a :href="row[column]" target="_blank"
                                                        class="inline-flex items-center gap-x-1.5 text-sm text-blue-600 decoration-2 hover:underline font-medium">
                                                        URL
                                                    </a>
                                                </template>
                                                <template v-else>
                                                    <span>{{ row[column] }}</span>
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
        </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted, watch, defineProps, defineEmits } from 'vue';
import PerPageComponent from '@/components/datatables/PerPageComponent.vue';
import PaginationComponent from '@/components/datatables/PaginationComponent.vue';
import SearchComponent from '@/components/datatables/SearchComponent.vue';
import EditComponent from '@/components/datatables/EditComponent.vue'
import CreateComponent from '@/components/datatables/CreateComponent.vue'

const data = ref([]);
const columns = ref([]);

const props = defineProps(['inputData', 'inputColumns']);

const selectedData = ref([]);
const filteredData = ref([]);
const perPage = ref(10);
const currentPage = ref(1);;
const hasNext = ref(true);
const hasPrevious = ref(false);
const order_by = ref('id');
const editItem = ref(null);
const createItem = ref(null);

const emit = defineEmits(['edit', 'create']);

function handleEdit(item) {
    emit('edit', item);
}

function handleCreate(item) {
    emit('create', item);
}

function setBaseImage(row) {
    if (row.base_image === '') {
        var url = row.image_url;

        fetch(url)
            .then(response => response.text())
            .then(data => {
                row.base_image = data;
            });
    }
}

function orderBy(column) {
    data.value.sort((a, b) => {
        if (!isNaN(a[column]) && !isNaN(b[column])) {
            return a[column] - b[column];
        }

        else {
            return a[column].localeCompare(b[column]);
        }
    });
}

function setOrderBy(column) {
    if (order_by.value === column) {
        data.value.reverse();
    }

    else {
        order_by.value = column;
        orderBy(column);
    }

    selectedData.value = perPageData();
}

function perPageData() {
    const start = (currentPage.value - 1) * perPage.value;
    const end = currentPage.value * perPage.value;

    return filteredData.value.slice(start, end);
}

function perPageSelected(option) {
    perPage.value = option;
};

function checkNextAndPrevious() {
    if (currentPage.value === 1) {
        hasPrevious.value = false;
    }

    else {
        hasPrevious.value = true;
    }

    if (currentPage.value === Math.ceil(data.value.length / perPage.value)) {
        hasNext.value = false;
    }

    else {
        hasNext.value = true;
    }
}

function handleNext() {
    currentPage.value++;

    checkNextAndPrevious();
}

function handlePrevious() {
    currentPage.value--;

    checkNextAndPrevious();
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

    selectedData.value = perPageData();

    checkNextAndPrevious();
}

watch(perPage, () => {
    selectedData.value = perPageData();
    currentPage.value = 1;

    checkNextAndPrevious();
});

watch(currentPage, () => {
    selectedData.value = perPageData();

    checkNextAndPrevious();
});

watch(props.inputData, () => {
    data.value = props.inputData;
    selectedData.value = perPageData();
    currentPage.value = 1;

    checkNextAndPrevious();
});

onMounted(() => {
    data.value = props.inputData;
    columns.value = props.inputColumns;
    filteredData.value = data.value;
    selectedData.value = perPageData();
    currentPage.value = 1;

    checkNextAndPrevious();

    createItem.value = columns.value.reduce((acc, column) => {
        acc[column] = '';

        return acc;
    }, {});
});

</script>