<template>
    <div class="w-full text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <Datatable :input-data="subscriptions" :maximum-page="maxPage" v-if="subscriptions.length > 0"
            :input-columns="columns" @order-by="order_by" @edit="handleEdit" @create="handleCreate"
            @updatePerPage="handlePerPageUpdate" @updateCurrentPage="handleCurrentPageUpdate" />
    </div>
</template>
    
<script setup>
import { ref, onMounted, watch } from 'vue';
import Datatable from '../datatables/Datatable.vue';
import SubscriptionRepository from '../../services/SubscriptionRepository';

const subscriptions = ref([]);
const columns = ref([]);
const perPage = ref(10);
const currentPage = ref(1);
const maxPage = ref(1000);

async function setMaxPage() {
    maxPage.value = await SubscriptionRepository.getMaxPage(perPage.value);
}

function handlePerPageUpdate(newVal) {
    perPage.value = newVal;
    currentPage.value = 1;
    setPageSubscriptions(currentPage.value, perPage.value);
    setMaxPage();
}

function handleCurrentPageUpdate(newVal) {
    currentPage.value = newVal;

    setPageSubscriptions(currentPage.value, perPage.value);
}

async function setPageSubscriptions(page, size) {
    var newSubscriptions = await SubscriptionRepository.getSubscriptionsByPage(page, size);

    newSubscriptions = newSubscriptions.map(subscription => {
        return {
            created: subscription.created,
            updated: subscription.updated,
            email: subscription.email,
            blueprint_name: subscription.blueprint.name,
        }
    })

    console.log(newSubscriptions);

    subscriptions.value = newSubscriptions;
}

onMounted(async () => {
    try {
        setPageSubscriptions(currentPage.value, perPage.value);

        columns.value = ['created', 'updated', 'email', 'blueprint_name'];

        await setMaxPage();
    } catch (error) {
        console.error('Failed to fetch subscriptions:', error);
    }
});
</script>
    
<style scoped></style>