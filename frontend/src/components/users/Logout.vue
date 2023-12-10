<template></template>

<script setup>
import { onMounted, ref } from 'vue';
import UserRepository from '../../services/UserRepository';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const router = useRouter();
const store = useStore();

onMounted(async () => {
    await UserRepository.logout();
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    store.commit('setToken', '');
    store.commit('setRole', '0');
    router.push({ name: 'Home' });
});

</script>