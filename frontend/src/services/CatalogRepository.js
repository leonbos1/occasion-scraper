import { getCachedData, setCachedData } from '../utils/catalogCache';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/**
 * Catalog Repository
 * API methods for fetching brand/model catalog data
 */
export default {
  /**
   * Get all enabled brands
   * Uses cache if available
   * @returns {Promise<Array>}
   */
  async getBrands() {
    const cacheKey = 'brands_cache';
    
    // Check cache first
    const cached = getCachedData(cacheKey);
    if (cached) {
      return cached;
    }
    
    // Fetch from API
    const response = await fetch(`${BASE_URL}/api/brands`);
    const data = await response.json();
    const brands = data.data || data;
    
    // Cache the result
    setCachedData(cacheKey, brands);
    
    return brands;
  },

  /**
   * Get all enabled models for a specific brand
   * Uses cache if available
   * @param {string} brandSlug - Brand slug
   * @returns {Promise<Array>}
   */
  async getModels(brandSlug) {
    if (!brandSlug) {
      return [];
    }
    
    const cacheKey = `models_${brandSlug}`;
    
    // Check cache first
    const cached = getCachedData(cacheKey);
    if (cached) {
      return cached;
    }
    
    // Fetch from API
    const response = await fetch(`${BASE_URL}/api/models?brand_slug=${brandSlug}`);
    const data = await response.json();
    const models = data.data || data;
    
    // Cache the result
    setCachedData(cacheKey, models);
    
    return models;
  }
};
