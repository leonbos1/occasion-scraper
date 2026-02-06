<template>
  <div class="p-6">
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-800">Brand Management</h1>
      <button
        @click="triggerScraper"
        :disabled="scraping"
        class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        <span v-if="!scraping">🔄 Run Catalog Scraper</span>
        <span v-else>⏳ Scraping...</span>
      </button>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="message" class="mb-4 p-4 rounded-lg" :class="messageClass">
      {{ message }}
    </div>

    <!-- 
      Brand Management UI
      
      Key Concepts:
      - slug: The URL-safe identifier used in the database and API (e.g., "alfa-romeo")
      - display_name: Human-readable name shown in the UI (e.g., "Alfa Romeo")
      - enabled: Controls whether the brand appears in public dropdown menus
      
      Admins can customize display_name while keeping the slug constant for data consistency.
    -->
    <div class="mb-4 flex gap-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search brands..."
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        @click="bulkEnable"
        :disabled="selectedBrands.length === 0"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        Enable Selected ({{ selectedBrands.length }})
      </button>
      <button
        @click="bulkDisable"
        :disabled="selectedBrands.length === 0"
        class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        Disable Selected ({{ selectedBrands.length }})
      </button>
    </div>

    <!-- Brand Table -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3">
              <input
                type="checkbox"
                @change="toggleSelectAll"
                :checked="allSelected"
                class="rounded border-gray-300"
              />
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Name
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Display Name
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Slug
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Last Seen
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="brand in filteredBrands" :key="brand.id" class="hover:bg-gray-50">
            <td class="px-4 py-4">
              <input
                type="checkbox"
                :value="brand.id"
                v-model="selectedBrands"
                class="rounded border-gray-300"
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ brand.name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <input
                v-if="editingBrand === brand.id"
                v-model="editDisplayName"
                @keyup.enter="saveDisplayName(brand)"
                @keyup.escape="cancelEdit"
                class="px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <span v-else>{{ brand.display_name }}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">
              {{ brand.slug }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                :class="brand.enabled ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
              >
                {{ brand.enabled ? 'Enabled' : 'Disabled' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(brand.last_seen) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
              <button
                v-if="editingBrand !== brand.id"
                @click="startEdit(brand)"
                class="text-blue-600 hover:text-blue-900"
              >
                ✏️ Edit
              </button>
              <button
                v-else
                @click="saveDisplayName(brand)"
                class="text-green-600 hover:text-green-900"
              >
                ✓ Save
              </button>
              <button
                @click="toggleEnabled(brand)"
                class="text-gray-600 hover:text-gray-900"
              >
                {{ brand.enabled ? '⊗ Disable' : '✓ Enable' }}
              </button>
              <router-link
                :to="{ name: 'ModelManagement', query: { brand_id: brand.id } }"
                class="text-purple-600 hover:text-purple-900"
              >
                🔍 View Models
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="filteredBrands.length === 0" class="text-center py-8 text-gray-500">
        <p v-if="brands.length === 0">No brands in catalog. Run the catalog scraper to populate.</p>
        <p v-else>No brands match your search.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AdminCatalogRepository from '../../services/AdminCatalogRepository';

const router = useRouter();

const brands = ref([]);
const searchQuery = ref('');
const selectedBrands = ref([]);
const editingBrand = ref(null);
const editDisplayName = ref('');
const scraping = ref(false);
const message = ref('');
const messageType = ref('');

const filteredBrands = computed(() => {
  if (!searchQuery.value) return brands.value;
  
  const query = searchQuery.value.toLowerCase();
  return brands.value.filter(brand =>
    brand.name.toLowerCase().includes(query) ||
    brand.display_name.toLowerCase().includes(query) ||
    brand.slug.toLowerCase().includes(query)
  );
});

const allSelected = computed({
  get() {
    return filteredBrands.value.length > 0 &&
           selectedBrands.value.length === filteredBrands.value.length;
  },
  set(value) {
    if (value) {
      selectedBrands.value = filteredBrands.value.map(b => b.id);
    } else {
      selectedBrands.value = [];
    }
  }
});

const messageClass = computed(() => {
  return messageType.value === 'success'
    ? 'bg-green-100 text-green-800 border border-green-300'
    : 'bg-red-100 text-red-800 border border-red-300';
});

onMounted(async () => {
  await fetchBrands();
});

async function fetchBrands() {
  try {
    brands.value = await AdminCatalogRepository.getAdminBrands();
  } catch (error) {
    showMessage('Failed to load brands: ' + error.message, 'error');
  }
}

function startEdit(brand) {
  editingBrand.value = brand.id;
  editDisplayName.value = brand.display_name;
}

function cancelEdit() {
  editingBrand.value = null;
  editDisplayName.value = '';
}

async function saveDisplayName(brand) {
  try {
    await AdminCatalogRepository.updateBrand(brand.id, {
      display_name: editDisplayName.value
    });
    
    brand.display_name = editDisplayName.value;
    cancelEdit();
    showMessage('Display name updated successfully', 'success');
  } catch (error) {
    showMessage('Failed to update display name: ' + error.message, 'error');
  }
}

async function toggleEnabled(brand) {
  try {
    const updated = await AdminCatalogRepository.updateBrand(brand.id, {
      enabled: !brand.enabled
    });
    
    brand.enabled = updated.enabled;
    showMessage(`Brand ${brand.enabled ? 'enabled' : 'disabled'} successfully`, 'success');
  } catch (error) {
    showMessage('Failed to update brand: ' + error.message, 'error');
  }
}

async function bulkEnable() {
  try {
    await Promise.all(
      selectedBrands.value.map(id =>
        AdminCatalogRepository.updateBrand(id, { enabled: true })
      )
    );
    
    await fetchBrands();
    selectedBrands.value = [];
    showMessage('Selected brands enabled successfully', 'success');
  } catch (error) {
    showMessage('Failed to enable brands: ' + error.message, 'error');
  }
}

async function bulkDisable() {
  try {
    await Promise.all(
      selectedBrands.value.map(id =>
        AdminCatalogRepository.updateBrand(id, { enabled: false })
      )
    );
    
    await fetchBrands();
    selectedBrands.value = [];
    showMessage('Selected brands disabled successfully', 'success');
  } catch (error) {
    showMessage('Failed to disable brands: ' + error.message, 'error');
  }
}

async function triggerScraper() {
  scraping.value = true;
  try {
    const summary = await AdminCatalogRepository.triggerCatalogScrape();
    showMessage(
      `Scraper complete: ${summary.brands_success}/${summary.brands_total} brands, ${summary.models_success}/${summary.models_total} models`,
      'success'
    );
    await fetchBrands();
  } catch (error) {
    showMessage('Failed to run scraper: ' + error.message, 'error');
  } finally {
    scraping.value = false;
  }
}

function toggleSelectAll() {
  allSelected.value = !allSelected.value;
}

function formatDate(dateString) {
  if (!dateString) return 'Never';
  const date = new Date(dateString);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function showMessage(msg, type) {
  message.value = msg;
  messageType.value = type;
  setTimeout(() => {
    message.value = '';
  }, 5000);
}
</script>
