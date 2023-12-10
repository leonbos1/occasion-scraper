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
            <button v-if="!successMessage" type="submit"
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Register</button>
            <a v-if="successMessage" href="/login"
                class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Login</a>
            <p class=" text-red-800" v-if="errorMessage">{{ errorMessage }}</p>
            <p class="" v-if="successMessage">{{ successMessage }}</p>
        </div>
    </form>
</template>

<script setup>
import { ref } from 'vue';
import UserRepository from '../../services/UserRepository';

const user = ref({ email: '', password: '' });
const errorMessage = ref('');
const successMessage = ref('');

const submitForm = async () => {
    try {
        const response = await UserRepository.register(user.value);

        if (response.status === 201) {
            successMessage.value = "User registered successfully!";
        }

        if (response.status === 400) {
            errorMessage.value = "Invalid request, please fill in all fields";
        }

        if (response.status === 409) {
            errorMessage.value = "User already exists";
        }

        if (response.status === 500) {
            errorMessage.value = "Oops! Something went wrong, please try again later";
        }

    } catch (error) {
        console.log(error);
    }
};
</script>