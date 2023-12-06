<template>
    <div class="w-full overflow-auto min-h-[75vh]">
        <div class="" v-if="modelObjects.length > 0">
            <div class="text-2xl font-semibold text-gray-900 mb-4 p-4">
                Car Models and Amounts
            </div>
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Model
                        </th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Amount
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="obj in modelObjects">
                        <td class="px-6 py-4 whitespace-nowrap">
                            {{ obj.model }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            {{ obj.amount }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else class="flex justify-center items-center h-full min-h-[75vh]">
            <span class="animate-spin rounded-full h-16 w-16 border-b-2 border-gray-900"></span>
        </div>
    </div>
</template>

<script setup>

import DashboardRepository from '../../services/DashboardRepository';
import { ref, onMounted } from 'vue';

const data = ref({});
const loaded = ref(false);
const modelObjects = ref([]);

function orderByAmount() {
    modelObjects.value.sort((a, b) => {
        return b.amount - a.amount;
    });
}

onMounted(async () => {
    data.value = await DashboardRepository.getCarModels();

    loaded.value = true;

    modelObjects.value = Object.keys(data.value).map((key) => {
        return {
            model: key,
            amount: data.value[key]
        }
    });

    orderByAmount();

    modelObjects.value = modelObjects.value.slice(0, 10);
});

</script>