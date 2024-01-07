import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';

import Cars from './components/cars/Cars.vue';
import CarInfo from './components/cars/CarInfo.vue';
import Home from './components/home/Home.vue'; 
import Users from './components/users/Users.vue';
import Blueprints from './components/blueprints/Blueprints.vue';
import CreateBlueprint from './components/blueprints/CreateBlueprint.vue';
import Dashboard from './components/dashboard/Dashboard.vue';
import Login from './components/users/Login.vue';
import Register from './components/users/Register.vue';
import Logout from './components/users/Logout.vue';
import store from './store';
import profile from './components/users/Profile.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home, name: 'Home' },
    { path: '/cars', component: Cars, name: 'Cars' },
    { path: '/cars/:id', component: CarInfo, props: true, name: 'CarInfo'},
    { path: '/users', component: Users, name: 'Users'},
    { path: '/blueprints', component: Blueprints, name: 'Blueprints'},
    { path: '/blueprints/create', component: CreateBlueprint, name: 'CreateBlueprint'},
    { path: '/dashboard', component: Dashboard, name: 'Dashboard'},
    { path: '/login', component: Login, name: 'Login'},
    { path: '/register', component: Register, name: 'Register'},
    { path: '/logout', component: Logout, name: 'Logout'},
    { path: '/profile', component: profile, name: 'Profile'},
  ],
});

const app = createApp(App);
app.use(router);
app.use(store);
app.mount('#app');