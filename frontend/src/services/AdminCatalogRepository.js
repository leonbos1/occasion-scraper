const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/**
 * Admin Catalog Repository
 * API methods for managing brands and models (admin only)
 */
export default {
  /**
   * Get all brands (enabled and disabled)
   * @returns {Promise<Array>}
   */
  async getAdminBrands() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${BASE_URL}/api/admin/brands`, {
      headers: { Authorization: token }
    });
    const data = await response.json();
    return data.data || data;
  },

  /**
   * Update a brand
   * @param {number} id - Brand ID
   * @param {object} data - Update data (display_name, enabled)
   * @returns {Promise<object>}
   */
  async updateBrand(id, data) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${BASE_URL}/api/admin/brands/${id}`, {
      method: 'POST',
      headers: { 
        'Authorization': token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    const result = await response.json();
    return result.data || result;
  },

  /**
   * Get all models (enabled and disabled)
   * @param {number|null} brandId - Optional brand ID to filter by
   * @returns {Promise<Array>}
   */
  async getAdminModels(brandId = null) {
    const token = localStorage.getItem('token');
    const url = brandId 
      ? `${BASE_URL}/api/admin/models?brand_id=${brandId}`
      : `${BASE_URL}/api/admin/models`;
    
    const response = await fetch(url, {
      headers: { Authorization: token }
    });
    const data = await response.json();
    return data.data || data;
  },

  /**
   * Update a model
   * @param {number} id - Model ID
   * @param {object} data - Update data (display_name, enabled)
   * @returns {Promise<object>}
   */
  async updateModel(id, data) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${BASE_URL}/api/admin/models/${id}`, {
      method: 'POST',
      headers: { 
        'Authorization': token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    const result = await response.json();
    return result.data || result;
  },

  /**
   * Trigger the catalog scraper
   * @returns {Promise<object>} - Scraper summary
   */
  async triggerCatalogScrape() {
    const token = localStorage.getItem('token');
    const response = await fetch(`${BASE_URL}/api/admin/scrape-catalog`, {
      method: 'POST',
      headers: { Authorization: token }
    });
    const data = await response.json();
    return data.data || data;
  }
};
