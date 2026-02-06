<template>
  <div class="brand-dropdown">
    <v-select
      v-model="selected"
      :options="brands"
      :reduce="brand => brand.slug"
      label="display_name"
      :filterable="true"
      :searchable="true"
      :loading="loading"
      :disabled="disabled"
      placeholder="Select a brand..."
      @option:selected="onSelect"
    >
      <template #no-options>
        <span v-if="!loading">{{ emptyMessage }}</span>
        <span v-else>Loading brands...</span>
      </template>
    </v-select>
  </div>
</template>

<script>
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';
import CatalogRepository from '../../services/CatalogRepository';

export default {
  name: 'BrandDropdown',
  components: {
    vSelect
  },
  props: {
    modelValue: {
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
      brands: [],
      loading: false,
      selected: this.modelValue
    };
  },
  computed: {
    emptyMessage() {
      return this.brands.length === 0 
        ? 'No brands available. Ask admin to run catalog scraper.'
        : 'No brands found';
    }
  },
  watch: {
    modelValue(newValue) {
      this.selected = newValue;
    },
    selected(newValue) {
      this.$emit('update:modelValue', newValue);
    }
  },
  mounted() {
    this.fetchBrands();
  },
  methods: {
    async fetchBrands() {
      this.loading = true;
      try {
        this.brands = await CatalogRepository.getBrands();
      } catch (error) {
        console.error('Failed to fetch brands:', error);
        this.brands = [];
      } finally {
        this.loading = false;
      }
    },
    onSelect(brand) {
      this.$emit('change', brand);
    }
  }
};
</script>

<style scoped>
.brand-dropdown {
  width: 100%;
}
</style>
