<template>
    <div v-if="Object.keys(groupedFilters).length > 0" class="p-4">
        <form @submit.prevent="applyFilters" class="space-y-4">
            <div v-for="(group, baseName) in groupedFilters" :key="baseName"
                class="grid grid-cols-1 gap-2">
                <span class="text-sm font-semibold text-gray-700">
                    {{ baseName.charAt(0).toUpperCase() + baseName.slice(1) }}
                </span>
                <div class="flex flex-wrap items-center gap-2">
                    <template v-for="filter in group" :key="filter">
                        <template v-if="filter === 'brand'">
                            <select v-model="filterValues[filter]"
                                class="border border-gray-300 rounded-lg px-3 py-2 w-full">
                                <option value="">All brands</option>
                                <option v-for="brand in brands" :key="brand" :value="brand">{{ brand }}</option>
                            </select>
                        </template>

                        <template v-else-if="filter === 'model'">
                            <select v-model="filterValues[filter]"
                                class="border border-gray-300 rounded-lg px-3 py-2 w-full">
                                <option value="">All models</option>
                                <option v-for="model in models" :key="model" :value="model">{{ model }}</option>
                            </select>
                        </template>

                        <template v-else>
                            <input :type="getInputType(filter)" :id="filter" v-model="filterValues[filter]"
                                class="border border-gray-300 rounded-lg px-3 py-2 w-full" />
                        </template>

                        <span v-if="group.length > 1 && filter.startsWith('min_')" class="text-xs text-gray-400">to</span>
                    </template>
                </div>
            </div>
            <div class="flex gap-2">
                <button type="button" @click="resetFilters"
                    class="w-1/2 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200">Reset</button>
                <button type="submit" class="w-1/2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Apply
                    Filters</button>
            </div>
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

function resetFilters() {
    initializeFilterValues();
    emit('filter', filterValues);
}

function getInputType(filterName) {
    const numericKeys = ['price', 'mileage', 'first_registration', 'distance'];
    return numericKeys.some((key) => filterName.includes(key)) ? 'number' : 'text';
}
</script>
