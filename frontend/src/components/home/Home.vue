<template>
  <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <div class="flex justify-center">
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="start">Start</button>
    </div>
  </div>
</template>
  
<script setup>

const start = () => {
  fetch('http://leonbos.nl:5000/start')
    .then(response => response.json());
}

</script>
  
<style scoped></style>
  