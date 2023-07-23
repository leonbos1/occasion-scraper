<template>
    <div id="hs-modal-signup"
        class="hs-overlay hidden w-full h-full fixed top-0 left-0 z-[60] overflow-x-hidden overflow-y-auto">
        <div
            class="hs-overlay-open:mt-7 hs-overlay-open:opacity-100 hs-overlay-open:duration-500 mt-0 opacity-0 ease-out transition-all sm:max-w-lg sm:w-full m-3 sm:mx-auto">
            <div class="bg-white border border-gray-200 rounded-xl shadow-sm dark:bg-gray-800 dark:border-gray-700">
                <div class="p-4 sm:p-7">
                    <div class="text-center">
                    </div>

                    <div class="grid gap-y-4">
                        <!--for all properties in car object, create a form input

                             -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6" v-for="property in properties"
                            :key="property.id">
                            <label class="block text-sm mb-2 dark:text-white"> {{ property }} </label>
                            <div class="relative">
                                <input type="text" :name="property" :value="car[property]"
                                    @input="updateProperty(property, $event.target.value)"
                                    class="py-3 px-4 block w-full border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400" />
                                <div class="hidden absolute inset-y-0 right-0 flex items-center pointer-events-none pr-3">
                                    <svg class="h-5 w-5 text-red-500" width="16" height="16" fill="currentColor"
                                        viewBox="0 0 16 16" aria-hidden="true">
                                        <path
                                            d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button @click="edit(car)"
                        class="mt-4 block w-full py-3 px-4 rounded-md bg-blue-500 text-white font-medium hover:bg-blue-600 focus:outline-none focus:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:bg-blue-700">
                        Edit
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { defineEmits, onMounted, ref, watch, withDefaults, defineProps } from 'vue';

const emit = defineEmits();

const props = defineProps({
    car: Object,
});

const updateProperty = (property, value) => {
    props.car[property] = value;
}

const properties = ref([]);

function edit(car) {
    emit('edit', car);
}

onMounted(() => {
    properties.value = Object.keys(props.car);
})
</script>
  