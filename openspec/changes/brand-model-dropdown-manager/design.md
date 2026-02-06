# Design: Brand and Model Dropdown Manager

## Context

The application currently requires users to manually type brand and model names when creating blueprints. This creates friction and errors. The existing scraper infrastructure (`backend/scrapers/autoscout_json.py`) already uses brand/model slugs in URL paths (e.g., `/lst/alfa-romeo.json`), so we have working knowledge of how AutoScout24 structures its data.

**Current Architecture:**
- Backend: Python Flask with SQLAlchemy ORM, MySQL database
- Frontend: Vue 3 with Tailwind CSS, using Vue Router
- Existing models: `Car`, `CarImage`, `BluePrint`, `ScrapeSession`, `User`, `Subscription`
- Blueprint model stores brand/model as plain text strings
- Admin functionality exists but needs extension for new catalog management

**Constraints:**
- Must maintain backward compatibility with existing blueprints that have text-based brand/model values
- Cannot disrupt existing scraper functionality
- Rate limiting required to avoid AutoScout24 blocking
- Initial catalog population required before dropdowns can be useful

**Stakeholders:**
- End users: Want easier blueprint creation with less typing
- Administrators: Need control over which brands/models appear
- System: Must maintain scraper compatibility and performance

## Goals / Non-Goals

**Goals:**
- Enumerate all available brands and models from AutoScout24 via discovery scraper
- Store brand/model catalog in database with enable/disable capability
- Provide admin UI to manage (enable/disable, customize display names) brands and models
- Replace text inputs with searchable dropdowns in blueprint forms
- Maintain backward compatibility with existing text-based blueprints
- Cache dropdown data on frontend to minimize API calls

**Non-Goals:**
- Automated periodic re-scraping (manual trigger only for MVP)
- Multi-language support for brand/model names
- Brand/model hierarchy beyond single brand → multiple models
- Analytics on which brands/models are most popular
- Validation that brand/model combinations actually exist on AutoScout24 during blueprint creation

## Decisions

### Decision 1: Discovery Strategy - Parse AutoScout24 HTML Brand/Model Pages

**Rationale:** AutoScout24 has brand and model landing pages (e.g., `https://www.autoscout24.nl/lst/alfa-romeo`) that list all available models. We can parse these HTML pages to discover the catalog.

**Alternatives Considered:**
- **Reverse-engineer AutoScout24 API**: Could use their internal APIs, but these are undocumented and may change without notice
- **Hardcode known brands**: Simpler but incomplete and requires manual maintenance
- **Scrape search autocomplete**: Could capture autocomplete suggestions, but may not be comprehensive

**Decision:** Parse HTML brand/model pages because:
- Publicly accessible and stable
- Comprehensive (shows all available options)
- Already used by AutoScout24 for SEO, so unlikely to change drastically
- Can extract both display names and URL slugs from page structure

### Decision 2: Database Schema - Separate Tables for Brands and Models

**Schema:**
```sql
CREATE TABLE brands (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,           -- Original name from AutoScout24
    slug VARCHAR(100) NOT NULL UNIQUE,    -- URL-safe slug for API calls
    display_name VARCHAR(100),             -- Customizable display text (defaults to name)
    enabled BOOLEAN DEFAULT true,
    last_seen DATETIME,                    -- Last time seen during catalog scrape
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_slug (slug),
    INDEX idx_enabled (enabled)
);

CREATE TABLE models (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,            -- Original name from AutoScout24
    slug VARCHAR(100) NOT NULL,            -- URL-safe slug for API calls
    display_name VARCHAR(100),              -- Customizable display text (defaults to name)
    enabled BOOLEAN DEFAULT true,
    last_seen DATETIME,                     -- Last time seen during catalog scrape
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE,
    UNIQUE KEY unique_brand_model (brand_id, slug),
    INDEX idx_brand_id (brand_id),
    INDEX idx_enabled (enabled)
);
```

**Rationale:**
- `name`: Preserve original AutoScout24 naming for reference
- `slug`: Store URL-safe version used in scraper API calls
- `display_name`: Allow customization without breaking API compatibility (defaults to `name` if not set)
- `enabled`: Admin control over dropdown visibility
- `last_seen`: Track when catalog scraper last found this entry (helps identify deprecated brands/models)
- Foreign key cascade ensures models are deleted when brand is deleted

**Alternatives Considered:**
- **Single table with brand/model pairs**: Simpler but causes duplication of brand data and makes brand-level operations harder
- **Store only slugs**: Would require re-slugifying on every display, and loses original AutoScout24 naming

**Decision:** Separate normalized tables for flexibility, data integrity, and efficient queries.

### Decision 3: Frontend Component - Use Vue Select Library for Searchable Dropdowns

**Chosen Library:** `vue-select` (https://vue-select.org/)

**Rationale:**
- Mature, well-maintained Vue 3 component
- Built-in search/filter functionality
- Supports custom display/value separation (show `display_name`, submit `slug`)
- Keyboard navigation and accessibility
- Lightweight (~30kb gzipped)

**Alternatives Considered:**
- **Native `<select>` with `<datalist>`**: No search functionality, poor UX for large lists
- **Build custom component**: Time-consuming, likely less accessible
- **PrimeVue Dropdown**: Heavier dependency, overkill for this use case

**Decision:** Use `vue-select` for rapid implementation with good UX.

### Decision 4: Caching Strategy - Frontend SessionStorage with 1-Hour TTL

**Implementation:**
- Cache brand list in `sessionStorage` with key `brands_cache` and timestamp
- Cache model lists per brand in `sessionStorage` with key `models_{brand_slug}` and timestamp
- TTL: 1 hour (3600 seconds)
- On cache miss or expiration, fetch from API and update cache

**Rationale:**
- Brand/model catalog changes infrequently (only when admin re-runs scraper)
- Reduces API load significantly
- SessionStorage scoped to browser tab (users in multiple tabs don't share stale cache)
- 1-hour TTL balances freshness with performance

**Alternatives Considered:**
- **No caching**: Excessive API calls, slower UX
- **LocalStorage**: Persists across sessions, harder to invalidate
- **Vuex/Pinia state**: Lost on page refresh, doesn't help initial load
- **Server-side caching**: Helpful but frontend caching still needed for multiple form loads

**Decision:** Frontend sessionStorage caching with 1-hour TTL strikes the right balance.

### Decision 5: Catalog Scraper Implementation - Separate Module with Manual Trigger

**Location:** `backend/scrapers/catalog_scraper.py`

**Approach:**
1. Fetch AutoScout24's brand listing page (likely `/lst` or homepage links)
2. Extract brand names and slugs from links
3. For each brand, fetch its landing page (e.g., `/lst/alfa-romeo`)
4. Extract model names and slugs from that page
5. Store in database with upsert logic (update existing, insert new)

**Rate Limiting:**
- Random delay between 1-3 seconds between requests
- Respect `robots.txt` (check with `urllib.robotparser`)
- Use User-Agent header to identify ourselves

**Error Handling:**
- Log errors but continue processing remaining brands
- Return summary with success/failure counts
- Don't modify existing data on failure

**Trigger:** Manual via `POST /api/admin/scrape-catalog` endpoint (admin-only)

**Rationale:**
- Separating catalog scraper from car scraper keeps concerns distinct
- Manual trigger gives admins control over when catalog updates happen
- Rate limiting prevents AutoScout24 blocks

**Alternatives Considered:**
- **Run catalog scraper on schedule**: Could auto-update, but manual trigger gives more control for MVP
- **Integrate into existing car scraper**: Would slow down car scraping and mix concerns
- **Real-time discovery**: Could discover brands/models as users search, but requires more complex logic

**Decision:** Separate manual-triggered catalog scraper for simplicity and control.

### Decision 6: Backward Compatibility - Support Legacy Text-Based Blueprints

**Strategy:**
- Blueprint model continues to store brand/model as text strings (no schema change)
- When editing existing blueprint, attempt to match text to catalog entry by slug
- If match found, pre-select dropdown option
- If no match, show text value as "(custom - not in catalog)" option
- Allow saving custom values if unchanged (don't force catalog selection)
- New blueprints always use catalog slugs

**Rationale:**
- No database migration required for blueprints
- Existing blueprints continue to work
- Gradual migration path as users edit old blueprints
- Edge cases (deleted brands, typos) handled gracefully

**Alternatives Considered:**
- **Migrate all blueprints to catalog IDs**: Requires complex migration logic and may break blueprints for brands not in catalog
- **Two separate fields (text and catalog ID)**: Schema change, added complexity
- **Block editing non-catalog blueprints**: Poor UX, forces immediate migration

**Decision:** In-place compatibility with graceful fallback for non-catalog values.

## Risks / Trade-offs

### Risk: AutoScout24 May Block Catalog Scraper
**Mitigation:** 
- Implement rate limiting (1-3 second delays)
- Respect robots.txt
- Use realistic User-Agent
- Manual trigger only (no automated hammering)
- If blocked, admins can retry after delay or manually populate critical brands

### Risk: AutoScout24 May Change Page Structure
**Mitigation:**
- Scraper includes error handling and logging
- Returns clear failure messages
- Catalog remains functional even if scraper breaks (users can still use existing catalog)
- Can fall back to manual entry if scraper completely fails

### Risk: Large Catalogs May Slow Dropdown Performance
**Trade-off:** AutoScout24 likely has 100-300 brands, each with 10-100 models. Total ~5,000-10,000 entries.

**Mitigation:**
- Frontend caching reduces API calls
- Searchable dropdowns make navigation easy
- Index database queries on brand_id and enabled
- Consider pagination if catalog exceeds 10,000 models (unlikely)

### Risk: Display Name Customization May Confuse Users
**Scenario:** Admin changes "Alfa Romeo" display to "ALFA ROMEO" but slug remains "alfa-romeo". User creates blueprint, slug is stored, but if admin later changes display back, user sees different text.

**Trade-off:** Accept minor confusion in favor of flexibility. Display names are cosmetic only.

**Mitigation:** Document in admin UI that display names are for presentation only.

### Risk: Catalog May Become Stale Over Time
**Trade-off:** Manual trigger means catalog only updates when admin remembers to run it.

**Mitigation:**
- Show `last_seen` timestamp in admin UI as reminder
- Consider future enhancement for scheduled re-scraping
- New brands/models on AutoScout24 won't break existing scraper (text fallback still works)

### Risk: Initial Catalog Population Required Before Dropdowns Useful
**Trade-off:** Chicken-and-egg problem - need to run scraper before dropdowns have data.

**Mitigation:**
- Document setup steps clearly (run catalog scraper first)
- Show helpful message in dropdown if catalog is empty: "No brands available. Ask admin to run catalog scraper."
- Consider including seed data for top 20 brands as fallback

## Migration Plan

### Phase 1: Database Setup
1. Create `brands` and `models` tables via Alembic migration
2. Add indexes for performance

### Phase 2: Backend Implementation
1. Create `backend/models/brand.py` and `backend/models/model.py` SQLAlchemy models
2. Implement `backend/scrapers/catalog_scraper.py` with rate limiting
3. Add API routes:
   - `POST /api/admin/scrape-catalog` (trigger scraper)
   - `GET /api/brands` (public, enabled brands only)
   - `GET /api/models?brand_slug={slug}` (public, enabled models only)
   - `GET /api/admin/brands` (admin, all brands)
   - `POST /api/admin/brands/{id}` (admin, update brand)
   - `GET /api/admin/models` (admin, all models)
   - `POST /api/admin/models/{id}` (admin, update model)
4. Add admin authentication checks to admin endpoints
5. Test catalog scraper in isolation

### Phase 3: Frontend Implementation
1. Install `vue-select` dependency: `npm install vue-select@4`
2. Create reusable dropdown components:
   - `BrandDropdown.vue` (fetches and caches brands)
   - `ModelDropdown.vue` (fetches models for selected brand)
3. Update `CreateBlueprint.vue` to use new dropdowns
4. Update `EditBlueprintComponent.vue` to use new dropdowns with legacy value handling
5. Create admin management pages:
   - `BrandManagement.vue` (table with search, edit, enable/disable)
   - `ModelManagement.vue` (table with brand filter, edit, enable/disable)
6. Add navigation links to admin UI

### Phase 4: Testing & Deployment
1. Run catalog scraper to populate initial data
2. Test blueprint creation with dropdowns
3. Test editing existing blueprints (both catalog and non-catalog values)
4. Test admin management (enable/disable, display name customization)
5. Verify scraper still works with slug values
6. Deploy to production

### Rollback Strategy
If critical issues arise:
1. Disable new admin routes via feature flag or config
2. Revert frontend to text inputs (CreateBlueprint.vue, EditBlueprintComponent.vue)
3. Keep database tables (no data loss) but stop using them
4. Existing blueprints continue to work (no schema changes)

### Post-Deployment
- Monitor API performance for dropdown endpoints
- Gather user feedback on dropdown UX
- Consider future enhancements:
  - Automated periodic catalog refresh
  - Analytics on popular brands/models
  - Bulk import/export for brand/model data

## Open Questions

1. **Should we display brand/model counts in admin UI?** (e.g., "Alfa Romeo (47 models)")
   - Useful for admins to understand catalog size
   - Adds query complexity (COUNT aggregate)
   - **Decision needed:** Wait for user feedback, add if requested

2. **Should we soft-delete or hard-delete brands/models that disappear from AutoScout24?**
   - Soft delete (set `enabled=false`) preserves history
   - Hard delete keeps database clean
   - **Decision needed:** Use `last_seen` timestamp as indicator, let admin decide whether to disable or delete

3. **Should we validate brand/model combinations before allowing blueprint creation?**
   - Pro: Ensures blueprints are valid
   - Con: Adds complexity, slows form submission
   - **Decision needed:** Trust catalog is accurate, skip validation for MVP

4. **Should we allow users (non-admin) to request new brands/models?**
   - Pro: Crowdsourced catalog improvements
   - Con: Requires approval workflow
   - **Decision needed:** Out of scope for MVP, consider for future enhancement
