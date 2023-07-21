<template>
    <div>
        <button
            class="px-4 py-2 text-sm font-medium leading-5 text-gray-700 transition-colors duration-150 bg-white border border-gray-300 rounded-md active:bg-gray-100 hover:bg-gray-100 focus:outline-none focus:shadow-outline-blue"
            @click="handlePrevious">
            Previous
        </button>
        <span class="px-4 py-2 text-sm font-medium leading-5 text-white">
            Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button
            class="px-4 py-2 text-sm font-medium leading-5 text-gray-700 transition-colors duration-150 bg-white border border-gray-300 rounded-md active:bg-gray-100 hover:bg-gray-100 focus:outline-none focus:shadow-outline-blue"
            @click="handleNext">
            Next
        </button>
    </div>
</template>
  
<script setup>
import { defineEmits, ref, watch, withDefaults, defineProps } from 'vue';

const emit = defineEmits();

const props = defineProps({
    currentPage: {
        type: Number,
        required: true,
    },
    totalPages: {
        type: Number,
        required: true,
    },
    hasPrevious: {
        type: Boolean,
        required: true,
    },
    hasNext: {
        type: Boolean,
        required: true,
    },
});

function handlePrevious() {
    if (props.hasPrevious) {
        emit('previous');
    }
}

function handleNext() {
    if (props.hasNext) {
        emit('next');
    }
}

</script>
  