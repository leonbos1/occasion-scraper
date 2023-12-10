<template>
    <form @submit.prevent="submitForm" class="w-full max-w-xs mx-auto">
        <div class="mb-4">
            <label for="email" class="block text-gray-700 text-sm font-bold mb-2">Email:</label>
            <input type="email" id="email" v-model="user.email" required
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
        </div>

        <div class="mb-6">
            <label for="password" class="block text-gray-700 text-sm font-bold mb-2">Password:</label>
            <input type="password" id="password" v-model="user.password" required
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline">
        </div>

        <div class="flex items-center justify-between">
            <button type="submit"
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Login</button>
        </div>
    </form>
</template>

<script setup>
import { ref } from 'vue';
import UserRepository from '../../services/UserRepository';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const store = useStore();

const router = useRouter();

const user = ref({ email: '', password: '' });

const submitForm = async () => {
    try {
        const response = await UserRepository.login(user.value);

        var json = await response.json();

        localStorage.setItem('token', json.token);
        localStorage.setItem('role', json.role);

        if (response.status === 200) {
            store.commit('setToken', json.token);
            var role = json.role;
            store.commit('setRole', role);
            router.push({ name: 'Home' });
        }
    } catch (error) {
        console.log(error);
    }
};
</script>