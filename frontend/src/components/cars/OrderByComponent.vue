<template>
    <select class="block w-full px-4 py-2 pr-8 leading-tight text-gray-700 bg-white border" @change="handleOptionSelected">
        <option value="" disabled selected hidden>Sort by</option>
        <option v-for="option in options" :key="option.value" :value="option.value">{{ option.label }}</option>
    </select>
</template>

<script setup>
import { defineEmits, onMounted, ref } from 'vue';
import 'preline';

const newInitialOptions = [
    {
        name: "brand",
        label: "Brand"
    },
    {
        name: "model",
        label: "Model"
    },
    {
        name: "price",
        label: "Price"
    },
    {
        name: "mileage",
        label: "Mileage"
    },
    {
        name: "first_registration",
        label: "First registration"
    },
    {
        name: "location",
        label: "Location"
    }
];

const options = ref([]);

function addAllOptions() {
    newInitialOptions.forEach(option => {
        options.value.push({ value: option.name + " asc", label: option.label + " (Ascending)" });
        options.value.push({ value: option.name + " desc", label: option.label + " (Descending)" });
    });
}

const emit = defineEmits();

function handleOptionSelected(event) {
    emit('option-selected', event.target.value);
}

onMounted(() => {
    addAllOptions();
});
</script>