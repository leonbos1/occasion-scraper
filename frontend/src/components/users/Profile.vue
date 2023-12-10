<template>
    <div class="bg-gray-100 p-4">
        <div class="bg-white rounded-lg shadow-lg p-6">
            <div class="mb-4">
                <p class="text-lg font-semibold">{{ profile.email }}</p>
                <p class="text-gray-500 text-sm">Created: <span>{{ profile.created }}</span></p>
                <p class="text-gray-500 text-sm">Updated: <span>{{ profile.updated }}</span></p>
                <p class="text-gray-500 text-sm">Role: <span>{{ profile.role }}</span></p>
                <p class="text-gray-500 text-sm">Blueprints Created: <span>{{ profile.amount_of_blueprints_created }}</span>
                </p>
                <p class="text-gray-500 text-sm">Blueprints Subscribed: <span>{{ profile.amount_of_blueprints_subscribed
                }}</span></p>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { onMounted, ref } from 'vue';
import UserRepository from '../../services/UserRepository';

const profile = ref({});

onMounted(async () => {
    profile.value = await UserRepository.profile();
});
</script>
  