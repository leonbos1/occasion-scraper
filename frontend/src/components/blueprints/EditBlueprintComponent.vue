<template>
    <div id="hs-modal-signup"
        class="hs-overlay hidden w-full h-5/6 fixed top-28 left-0 z-[60] overflow-x-hidden overflow-y-auto">
        <div
            class="hs-overlay-open:mt-7 hs-overlay-open:opacity-100 hs-overlay-open:duration-500 mt-0 opacity-0 ease-out transition-all sm:max-w-lg sm:w-full m-3 sm:mx-auto">
            <div
                class="bg-white border border-gray-200 rounded-xl shadow-sm dark:bg-gray-800 dark:border-gray-700 h-[70vh] flex flex-col">
                <div class="p-4 sm:p-7 h-full">
                    <div class="text-center">
                    </div>
                    <div class="grid gap-y-4 h-[90%]">
                        <div class="overflow-auto">
                            <div class="grid grid-cols-1 mb-1 sm:grid-cols-2 gap-4 sm:gap-6">
                                <label class="block text-sm mb-2 dark:text-white"> Created </label>
                                <div class="relative">
                                    <span
                                        class="py-3 px-4 block w-full border-gray-200 rounded-md text-sm dark:bg-gray-700 dark:border-gray-700 dark:text-gray-400">
                                        {{ blueprint.created }}
                                    </span>
                                </div>
                            </div>
                            <div class="grid grid-cols-1 mb-1 sm:grid-cols-2 gap-4 sm:gap-6">
                                <label class="block text-sm mb-2 dark:text-white"> Updated </label>
                                <div class="relative">
                                    <span
                                        class="py-3 px-4 block w-full border-gray-200 rounded-md text-sm dark:bg-gray-700 dark:border-gray-700 dark:text-gray-400">
                                        {{ blueprint.updated }}
                                    </span>
                                </div>
                            </div>
                            <div class="grid grid-cols-1 mb-1 sm:grid-cols-2 gap-4 sm:gap-6">
                                <label class="block text-sm mb-2 dark:text-white"> Name </label>
                                <div class="relative">
                                    <input v-model="blueprint.name" type="text" name="name" id="name"
                                        class="py-3 px-4 block w-full border-gray-200 rounded-md text-sm dark:bg-gray-700 dark:border-gray-700 dark:text-gray-400" />
                                </div>
                            </div>
                            <div class="grid grid-cols-1 mb-1 sm:grid-cols-2 gap-4 sm:gap-6">
                                <label class="block text-sm mb-2 dark:text-white"> Users </label>
                                <div class="relative">
                                    <UserDropdown :subscriptions="blueprint.subscriptions" label="Select users"
                                        v-model="selectedUsers" @update:selectedItems="handleUpdateUsers" />
                                </div>
                            </div>
                        </div>
                        <button @click="edit(blueprint)"
                            class="mt-auto block w-full py-3 px-4 rounded-md bg-blue-500 text-white font-medium hover:bg-blue-600 focus:outline-none focus:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:bg-blue-700">
                            Edit
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { defineEmits, onMounted, ref, defineProps } from 'vue';
import UserRepository from '../../services/UserRepository';
import UserDropdown from '../dropdowns/UserDropdown.vue';

const emit = defineEmits();

const props = defineProps({
    blueprint: {
        type: Object,
        required: true
    }
});

const selectedUsers = ref([]);

const updateProperty = (property, value) => {
    props.blueprint[property] = value;
}

const properties = ref([]);

function edit(blueprint) {
    emit('edit', blueprint, selectedUsers.value);
}

function handleUpdateUsers(newVal) {
    selectedUsers.value = newVal;
}
</script>
  