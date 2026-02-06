/**
 * Catalog Cache Utility
 * Manages sessionStorage caching for brand/model catalog data
 */

const CACHE_TTL = 3600000; // 1 hour in milliseconds

/**
 * Get cached data from sessionStorage
 * @param {string} key - Cache key
 * @returns {any|null} - Cached data or null if expired/missing
 */
export function getCachedData(key) {
  try {
    const cached = sessionStorage.getItem(key);
    
    if (!cached) {
      return null;
    }
    
    const { data, timestamp } = JSON.parse(cached);
    const now = Date.now();
    
    // Check if cache has expired (1 hour TTL)
    if (now - timestamp > CACHE_TTL) {
      sessionStorage.removeItem(key);
      return null;
    }
    
    return data;
  } catch (error) {
    console.error('Error reading from cache:', error);
    return null;
  }
}

/**
 * Set data in sessionStorage cache
 * @param {string} key - Cache key
 * @param {any} data - Data to cache
 */
export function setCachedData(key, data) {
  try {
    const cacheEntry = {
      data,
      timestamp: Date.now()
    };
    
    sessionStorage.setItem(key, JSON.stringify(cacheEntry));
  } catch (error) {
    console.error('Error writing to cache:', error);
  }
}

/**
 * Clear specific cache entry
 * @param {string} key - Cache key
 */
export function clearCache(key) {
  try {
    sessionStorage.removeItem(key);
  } catch (error) {
    console.error('Error clearing cache:', error);
  }
}

/**
 * Clear all catalog cache entries
 */
export function clearAllCatalogCache() {
  try {
    // Clear brands cache
    sessionStorage.removeItem('brands_cache');
    
    // Clear all model caches (they start with 'models_')
    const keys = Object.keys(sessionStorage);
    keys.forEach(key => {
      if (key.startsWith('models_')) {
        sessionStorage.removeItem(key);
      }
    });
  } catch (error) {
    console.error('Error clearing catalog cache:', error);
  }
}
