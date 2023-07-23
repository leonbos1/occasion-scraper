<template>
  <select class="block w-full px-4 py-2 pr-8 leading-tight text-gray-700 bg-white border" @change="handleOptionSelected">
    <option v-for="option in options" :key="option" :value="option">{{ option }}</option>
  </select>
</template>
  
<script setup>
import { defineEmits } from 'vue';
import 'preline';

const options = [10, 25, 50, 100];

const emit = defineEmits();

function handleOptionSelected(event) {
  const selectedOption = parseInt(event.target.value, 10);
  emit('option-selected', selectedOption);
}
</script>
  