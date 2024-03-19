<template>
    <div v-if="Object.keys(groupedFilters).length > 0" class="p-4">
        <form @submit.prevent="applyFilters" class="space-y-4">
            <div v-for="(group, baseName) in groupedFilters" :key="baseName"
                class="flex flex-col md:flex-row items-center md:space-x-2 space-y-2 md:space-y-0">
                <span class="font-semibold w-full md:w-[7vw] text-center md:text-left">{{
        baseName.charAt(0).toUpperCase() +
        baseName.slice(1) }}:</span>
                <div v-for="filter in group" :key="filter" class="flex items-center space-x-1">

                    <template v-if="filter === 'brand'">
                        <select v-model="filterValues[filter]"
                            class="border-2 border-gray-300 rounded px-2 py-1 w-full md:max-w-[5vw]">
                            <option v-for="brand in brands" :key="brand" :value="brand">{{ brand }}</option>
                        </select>
                    </template>

                    <template v-else-if="filter === 'model'">
                        <select v-model="filterValues[filter]"
                            class="border-2 border-gray-300 rounded px-2 py-1 w-full md:max-w-[5vw]">
                            <option v-for="model in models" :key="model" :value="model">{{ model }}</option>
                        </select>
                    </template>

                    <template v-else>
                        <input type="text" :id="filter" v-model="filterValues[filter]"
                            class="border-2 border-gray-300 rounded px-2 py-1 w-full md:max-w-[5vw]" />
                    </template>

                    <span v-if="group.length > 1 && filter.startsWith('min_')">to</span>
                </div>
            </div>
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 w-full">Apply
                Filters</button>
        </form>
    </div>
</template>


<script setup>
import { ref, onMounted, reactive, watch } from 'vue';
import CarRepository from '../../services/CarRepository';

const filters = ref([]);
const filterValues = reactive({});
const groupedFilters = ref({});
const brands = ref([]);
const models = ref([]);
const brandAndModels = ref({});

const emit = defineEmits(['filter']);

watch(filterValues, (newValue, oldValue) => {
    if (newValue.brand !== '' && newValue.brand !== oldValue.brand) {
        filterValues.model = '';
    }
    setBrandAndModels();
});

onMounted(async () => {
    try {
        const response = await CarRepository.getFilters();
        if (Array.isArray(response)) {
            filters.value = response;
            groupFilters(response);
            initializeFilterValues();
            await setBrandAndModels();
        } else {
            console.error("Unexpected response format:", response);
        }
    } catch (error) {
        console.error("Error fetching filters:", error);
    }
});

async function setBrandAndModels() {
    if (!brandAndModels.value || Object.keys(brandAndModels.value).length === 0) {
        brandAndModels.value = await CarRepository.getBrandsAndModels();
    }

    brands.value = Object.keys(brandAndModels.value);

    if (filterValues.brand && brandAndModels.value[filterValues.brand]) {
        models.value = brandAndModels.value[filterValues.brand];
    } else {
        models.value = [];
    }
}

function groupFilters(filterList) {
    const groupMap = {};

    filterList.forEach(filter => {
        const baseName = filter.replace(/^(min_|max_)/, '');
        if (!groupMap[baseName]) {
            groupMap[baseName] = [];
        }
        groupMap[baseName].push(filter);
    });

    groupedFilters.value = groupMap;
}

function initializeFilterValues() {
    filters.value.forEach(filter => {
        filterValues[filter] = '';
    });
}

function applyFilters() {
    emit('filter', filterValues);
}
</script>
