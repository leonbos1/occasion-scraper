<template>
  <div class="p-6">
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-3xl font-bold text-gray-800">Model Management</h1>
      <router-link
        to="/admin/brands"
        class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg transition"
      >
        ← Back to Brands
      </router-link>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="message" class="mb-4 p-4 rounded-lg" :class="messageClass">
      {{ message }}
    </div>

    <!-- 
      Model Management UI
      
      Key Concepts:
      - slug: The URL-safe identifier (e.g., "3-series")
      - display_name: Human-readable name shown in dropdowns (e.g., "3 Series")
      - enabled: Controls dropdown visibility
      - brand_id: Foreign key linking model to brand
      
      Models can be filtered by brand. The "View Models" link from Brand Management
      pre-populates the brand filter via route.query.brand_id.
    -->
    <div class="mb-4 flex gap-4">
      <select
        v-model="selectedBrandId"
        @change="fetchModels"
        class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option :value="null">All Brands</option>
        <option v-for="brand in brands" :key="brand.id" :value="brand.id">
          {{ brand.display_name }}
        </option>
      </select>
      <button
        @click="bulkEnable"
        :disabled="selectedModels.length === 0"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        Enable Selected ({{ selectedModels.length }})
      </button>
      <button
        @click="bulkDisable"
        :disabled="selectedModels.length === 0"
        class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        Disable Selected ({{ selectedModels.length }})
      </button>
    </div>

    <!-- Model Table -->
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
              Brand
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
          <tr v-for="model in models" :key="model.id" class="hover:bg-gray-50">
            <td class="px-4 py-4">
              <input
                type="checkbox"
                :value="model.id"
                v-model="selectedModels"
                class="rounded border-gray-300"
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-700">
              {{ model.brand_name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ model.name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <input
                v-if="editingModel === model.id"
                v-model="editDisplayName"
                @keyup.enter="saveDisplayName(model)"
                @keyup.escape="cancelEdit"
                class="px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <span v-else>{{ model.display_name }}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">
              {{ model.slug }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                :class="model.enabled ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
              >
                {{ model.enabled ? 'Enabled' : 'Disabled' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(model.last_seen) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
              <button
                v-if="editingModel !== model.id"
                @click="startEdit(model)"
                class="text-blue-600 hover:text-blue-900"
              >
                ✏️ Edit
              </button>
              <button
                v-else
                @click="saveDisplayName(model)"
                class="text-green-600 hover:text-green-900"
              >
                ✓ Save
              </button>
              <button
                @click="toggleEnabled(model)"
                class="text-gray-600 hover:text-gray-900"
              >
                {{ model.enabled ? '⊗ Disable' : '✓ Enable' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="models.length === 0" class="text-center py-8 text-gray-500">
        <p v-if="!selectedBrandId">No models in catalog. Select a brand or run the catalog scraper.</p>
        <p v-else>No models found for the selected brand.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import AdminCatalogRepository from '../../services/AdminCatalogRepository';

const route = useRoute();

const brands = ref([]);
const models = ref([]);
const selectedBrandId = ref(null);
const selectedModels = ref([]);
const editingModel = ref(null);
const editDisplayName = ref('');
const message = ref('');
const messageType = ref('');

const allSelected = computed({
  get() {
    return models.value.length > 0 &&
           selectedModels.value.length === models.value.length;
  },
  set(value) {
    if (value) {
      selectedModels.value = models.value.map(m => m.id);
    } else {
      selectedModels.value = [];
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
  
  // Check if brand_id was passed via query parameter
  if (route.query.brand_id) {
    selectedBrandId.value = parseInt(route.query.brand_id);
  }
  
  await fetchModels();
});

async function fetchBrands() {
  try {
    brands.value = await AdminCatalogRepository.getAdminBrands();
  } catch (error) {
    showMessage('Failed to load brands: ' + error.message, 'error');
  }
}

async function fetchModels() {
  try {
    models.value = await AdminCatalogRepository.getAdminModels(selectedBrandId.value);
  } catch (error) {
    showMessage('Failed to load models: ' + error.message, 'error');
  }
}

function startEdit(model) {
  editingModel.value = model.id;
  editDisplayName.value = model.display_name;
}

function cancelEdit() {
  editingModel.value = null;
  editDisplayName.value = '';
}

async function saveDisplayName(model) {
  try {
    await AdminCatalogRepository.updateModel(model.id, {
      display_name: editDisplayName.value
    });
    
    model.display_name = editDisplayName.value;
    cancelEdit();
    showMessage('Display name updated successfully', 'success');
  } catch (error) {
    showMessage('Failed to update display name: ' + error.message, 'error');
  }
}

async function toggleEnabled(model) {
  try {
    const updated = await AdminCatalogRepository.updateModel(model.id, {
      enabled: !model.enabled
    });
    
    model.enabled = updated.enabled;
    showMessage(`Model ${model.enabled ? 'enabled' : 'disabled'} successfully`, 'success');
  } catch (error) {
    showMessage('Failed to update model: ' + error.message, 'error');
  }
}

async function bulkEnable() {
  try {
    await Promise.all(
      selectedModels.value.map(id =>
        AdminCatalogRepository.updateModel(id, { enabled: true })
      )
    );
    
    await fetchModels();
    selectedModels.value = [];
    showMessage('Selected models enabled successfully', 'success');
  } catch (error) {
    showMessage('Failed to enable models: ' + error.message, 'error');
  }
}

async function bulkDisable() {
  try {
    await Promise.all(
      selectedModels.value.map(id =>
        AdminCatalogRepository.updateModel(id, { enabled: false })
      )
    );
    
    await fetchModels();
    selectedModels.value = [];
    showMessage('Selected models disabled successfully', 'success');
  } catch (error) {
    showMessage('Failed to disable models: ' + error.message, 'error');
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
