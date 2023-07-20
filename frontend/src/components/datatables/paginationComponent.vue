<template>
    <div>
        <button
            class="px-4 py-2 text-sm font-medium leading-5 text-gray-700 transition-colors duration-150 bg-white border border-gray-300 rounded-md active:bg-gray-100 hover:bg-gray-100 focus:outline-none focus:shadow-outline-blue"
            @click="handlePrevious">
            Previous
        </button>
        <button
            class="px-4 py-2 text-sm font-medium leading-5 text-gray-700 transition-colors duration-150 bg-white border border-gray-300 rounded-md active:bg-gray-100 hover:bg-gray-100 focus:outline-none focus:shadow-outline-blue"
            @click="handleNext">
            Next
        </button>
    </div>
</template>
  
<script setup>
import { defineEmits, ref, watch, withDefaults } from 'vue';

const emit = defineEmits();

function handlePrevious() {
    emit('previous');
}

function handleNext() {
    emit('next');
}

const hasNext = ref(false);
const hasPrevious = ref(false);

</script>
  