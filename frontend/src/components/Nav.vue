<template>
  <nav class="bg-white border-gray-200 dark:bg-gray-900 w-screen">
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
      <div class="w-full md:block md:w-auto" id="navbar-default">
        <ul
          class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
          <li v-for="item in menuItems" :key="item.id" class="navbar-item">
            <router-link :to="item.url"
              class="block py-2 pl-3 pr-4 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">
              {{ item.label }}
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
  
<script>
export default {
  data() {
    return {
      menuItems: [
        { id: 1, label: 'Home', url: '/' },
        { id: 2, label: 'Cars', url: '/cars' },
        { id: 3, label: 'Blueprints', url: '/blueprints' },
        { id: 4, label: 'Users', url: '/users' },
        { id: 5, label: 'Dashboard', url: '/dashboard' }
      ],
    };
  },
};
</script>  
  
<style scoped></style>
  