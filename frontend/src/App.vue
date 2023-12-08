<template>
  <div class="container m-auto">
    <div class="max-w-screen-xl mx-auto p-0 pb-4 flex flex-col items-center">
      <Nav class="bg-white border-gray-200 dark:bg-gray-900 w-full" />
      <router-view />
    </div>
  </div>
</template>

<script>
import Nav from './components/Nav.vue';
import Cars from './components/cars/Cars.vue';
import Home from './components/home/Home.vue';
import Users from './components/users/Users.vue';
import Blueprints from './components/blueprints/Blueprints.vue';

export default {
  components: {
    Nav,
    Cars,
    Home,
    Users,
    Blueprints
  }
};
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

body {
  margin: 0;
  background-color: rgba(198, 198, 255, 0.26);
}
h1 {
  margin-top: 0;
}
</style>
