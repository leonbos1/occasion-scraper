<template>
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
      <!--make a button to do a get request to leonbos.nl:5000/start
      and center it-->
      <div class="flex justify-center">
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="start">Start</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';

  const start = () => {
    fetch('http://leonbos.nl:5000/start')
    .then(response => response.json())
    .then(data => console.log(data));
  }
  
  </script>
  
  <style scoped>
  </style>
  