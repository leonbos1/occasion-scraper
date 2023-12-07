<template>
    <div @click="dropdownOpen = !dropdownOpen"
        class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
        {{ label }}
        <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4" />
        </svg>
    </div>
    <div v-if="dropdownOpen"
        class="z-10 w-48 bg-white divide-y divide-gray-100 rounded-lg shadow dark:bg-gray-700 dark:divide-gray-600 overflow-hidden">
        <div class="p-3 space-y-3 text-sm text-gray-700 dark:text-gray-200">
            <ul class="p-3 space-y-3 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownCheckboxButton">
                <li v-for="item in items" :key="item[keyProperty]">
                    <div class="flex items-center">
                        <input type="checkbox" :id="item[keyProperty]"
                            class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"
                            :value="item[keyProperty]" v-model="selectedItems">
                        <label :for="item[keyProperty]" class="ms-2 text-sm font-small text-gray-900 dark:text-gray-300">
                            {{ item[displayProperty] }}
                        </label>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { defineEmits, onMounted, ref, defineProps, watch } from 'vue';

const props = defineProps({
    items: Array,
    keyProperty: String,
    displayProperty: String,
    label: String
});

const selectedItems = ref([]);
const dropdownOpen = ref(false);

const emit = defineEmits(['update:selectedItems']);

watch(selectedItems, (newVal) => {
    emit('update:selectedItems', newVal);
});
</script>