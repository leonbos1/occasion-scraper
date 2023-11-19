<template>
  <div class="container" id="app">
    <Nav class="nav" />
    <div class="content">
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

.container {
  max-width: 90%;
  margin: 0 auto;
  padding: 20px;
}

.content {
  margin-top: 60px;
}

.nav {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #f2f2f2;
  padding: 10px;
  z-index: 9999;
}
</style>
