<template>
    <div @click="dropdownOpen = !dropdownOpen"
        class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
        {{ label }}
        <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4" />
        </svg>
    </div>
    <div v-if="dropdownOpen" class="...">
        <div class="p-3 space-y-3 text-sm text-gray-700 dark:text-gray-200">
            <ul class="p-3 space-y-3 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownCheckboxButton">
                <li v-for="user in users" :key="user.id">
                    <div class="flex items-center">
                        <input type="checkbox" :id="user.id" class="..." :value="user.id" v-model="selectedItems">
                        <label :for="user.id" class="ms-2 text-sm font-small text-gray-900 dark:text-gray-300">
                            {{ user.email }}
                        </label>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { defineEmits, ref, defineProps, watch, onMounted } from 'vue';
import UserRepository from '../../services/UserRepository';

const props = defineProps({
    subscriptions: Array,
    label: String
});

const selectedItems = ref([]);
const dropdownOpen = ref(false);
const users = ref([]);

const emit = defineEmits(['update:selectedItems']);

watch(selectedItems, (newVal) => {
    emit('update:selectedItems', newVal);
});

onMounted(async () => {
    users.value = await UserRepository.getAllUsers();
    preselectSubscribedUsers();
});

function preselectSubscribedUsers() {
    const subscribedUserIds = props.subscriptions.map(sub => sub.user.id);
    selectedItems.value = users.value.filter(user => subscribedUserIds.includes(user.id)).map(user => user.id);
}
</script>