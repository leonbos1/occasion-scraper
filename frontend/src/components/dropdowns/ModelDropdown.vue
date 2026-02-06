<template>
  <div class="model-dropdown">
    <v-select
      v-model="selected"
      :options="models"
      :reduce="model => model.slug"
      label="display_name"
      :filterable="true"
      :searchable="true"
      :loading="loading"
      :disabled="disabled || !brandSlug"
      :placeholder="placeholder"
      @option:selected="onSelect"
    >
      <template #no-options>
        <span v-if="!loading">{{ emptyMessage }}</span>
        <span v-else>Loading models...</span>
      </template>
    </v-select>
  </div>
</template>

<script>
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';
import CatalogRepository from '../../services/CatalogRepository';

export default {
  name: 'ModelDropdown',
  components: {
    vSelect
  },
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    brandSlug: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'change'],
  data() {
    return {
      models: [],
      loading: false,
      selected: this.modelValue
    };
  },
  computed: {
    placeholder() {
      if (!this.brandSlug) {
        return 'Select a brand first';
      }
      return 'Select a model...';
    },
    emptyMessage() {
      if (!this.brandSlug) {
        return 'Select a brand first';
      }
      const brandName = this.brandSlug.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      return this.models.length === 0
        ? `No models available for ${brandName}`
        : 'No models found';
    }
  },
  watch: {
    modelValue(newValue) {
      this.selected = newValue;
    },
    selected(newValue) {
      this.$emit('update:modelValue', newValue);
    },
    brandSlug(newSlug, oldSlug) {
      // Clear selection when brand changes
      if (newSlug !== oldSlug) {
        this.selected = '';
        this.models = [];
        
        if (newSlug) {
          this.fetchModels();
        }
      }
    }
  },
  mounted() {
    if (this.brandSlug) {
      this.fetchModels();
    }
  },
  methods: {
    async fetchModels() {
      if (!this.brandSlug) {
        this.models = [];
        return;
      }
      
      this.loading = true;
      try {
        this.models = await CatalogRepository.getModels(this.brandSlug);
      } catch (error) {
        console.error('Failed to fetch models:', error);
        this.models = [];
      } finally {
        this.loading = false;
      }
    },
    onSelect(model) {
      this.$emit('change', model);
    }
  }
};
</script>

<style scoped>
.model-dropdown {
  width: 100%;
}
</style>
