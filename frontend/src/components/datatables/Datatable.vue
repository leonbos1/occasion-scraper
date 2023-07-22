<template>
    <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <div class="flex flex-col items-center justify-center w-full h-32">
            <perPageComponent class="w-1/4 mr-auto" @option-selected="perPageSelected" />
            <paginationComponent class="w-1/4 ml-auto" :current-page="currentPage"
                :total-pages="Math.ceil(data.length / perPage)" :has-previous="hasPrevious" :has-next="hasNext"
                @previous="handlePrevious" @next="handleNext" />
        </div>
        <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
            <table class="w-full text-sm text-left">
                <thead class="text-xs">
                    <tr>
                        <th v-for="column in columns" :key="column"
                            class="px-4 py-3 text-gray-500 uppercase tracking-wider">
                            {{ column }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="row in selectedData" :key="row.id" class="border-b border-gray-200">
                        <td v-for="column in columns" :key="column" class="px-4 py-3">
                            <template v-if="column === 'base_image'">
                                <img :src="row[column]" class="w-10 h-10" />
                            </template>
                            <template v-else>
                                <span>{{ row[column] }}</span>
                            </template>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="flex flex-col items-center justify-center w-full h-32">
            <perPageComponent class="w-1/4 mr-auto" @option-selected="perPageSelected" />
        </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted, watch, defineProps } from 'vue';
import perPageComponent from './PerPageComponent.vue';
import paginationComponent from './PaginationComponent.vue';

const data = ref([]);
const columns = ref([]);

const props = defineProps(['inputData', 'inputColumns']);

const selectedData = ref([]);
const perPage = ref(10);
const currentPage = ref(1);;
const hasNext = ref(true);
const hasPrevious = ref(false);

function perPageData() {
    const start = (currentPage.value - 1) * perPage.value;
    const end = currentPage.value * perPage.value;
    return data.value.slice(start, end);
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

watch(perPage, () => {
    selectedData.value = perPageData();
    currentPage.value = 1;

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
    selectedData.value = perPageData();
    currentPage.value = 1;

    checkNextAndPrevious();
});

</script>
  
<style scoped></style>