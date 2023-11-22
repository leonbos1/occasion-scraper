import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';

import Cars from './components/cars/Cars.vue';
import Home from './components/home/Home.vue'; 
import Users from './components/users/Users.vue';
import Blueprints from './components/blueprints/Blueprints.vue';
import Tests from './components/test/Tests.vue';
import Dashboard from './components/dashboard/Dashboard.vue';
import Subscriptions from './components/subscriptions/Subscriptions.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/cars', component: Cars },
    { path: '/users', component: Users},
    { path: '/blueprints', component: Blueprints},
    { path: '/tests', component: Tests},
    { path: '/dashboard', component: Dashboard},
    { path: '/subscriptions', component: Subscriptions},
  ],
});

const app = createApp(App);
app.use(router);
app.mount('#app');