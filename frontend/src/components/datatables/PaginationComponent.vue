<template>
    <div class="mr-2 ml-2">
        <div class="inline-flex gap-x-2">
            <button type="button" @click="handlePrevious"
                class="py-2 px-3 inline-flex justify-center items-center gap-2 rounded-md border font-medium bg-white">
                <svg class="w-3 h-3" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                    viewBox="0 0 16 16">
                    <path fill-rule="evenodd"
                        d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z" />
                </svg>
                Prev
            </button>
            <div class="flex items-center gap-x-1 text-black">
                <span>{{ currentPage }}</span>
                <span>/</span>
                <span>{{ maximumPage }}</span>
            </div>
            <button type="button" @click="handleNext"
                class="py-2 px-3 inline-flex justify-center items-center gap-2 rounded-md border font-medium bg-white">
                Next
                <svg class="w-3 h-3" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                    viewBox="0 0 16 16">
                    <path fill-rule="evenodd"
                        d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z" />
                </svg>
            </button>
        </div>
    </div>
</template>
  
<script setup>
import { defineEmits, defineProps } from 'vue';

const emit = defineEmits();

const props = defineProps({
    currentPage: {
        type: Number,
        required: true,
    },
    maximumPage: {
        type: Number,
        required: true,
    },
});

function handlePrevious() {
    emit('previous');
}

function handleNext() {
    emit('next');
}

</script>
  