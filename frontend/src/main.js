import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';

import Cars from './components/cars/Cars.vue';
import CarInfo from './components/cars/CarInfo.vue';
import Home from './components/home/Home.vue'; 
import Users from './components/users/Users.vue';
import Blueprints from './components/blueprints/Blueprints.vue';
import Dashboard from './components/dashboard/Dashboard.vue';
import Login from './components/users/Login.vue';
import Register from './components/users/Register.vue';
import Logout from './components/users/Logout.vue';
import store from './store';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home, name: 'Home' },
    { path: '/cars', component: Cars },
    { path: '/users', component: Users},
    { path: '/blueprints', component: Blueprints},
    { path: '/dashboard', component: Dashboard},
    { path: '/cars/:id', component: CarInfo, props: true, name: 'CarInfo'},
    { path: '/login', component: Login},
    { path: '/register', component: Register},
    { path: '/logout', component: Logout},
  ],
});

const app = createApp(App);
app.use(router);
app.use(store);
app.mount('#app');