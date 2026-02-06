## Context

The occasion-scraper is a Flask/Vue.js application that scrapes car listings from AutoScout24 and other sites. Users create blueprints (search criteria) and receive notifications about new matching cars. Current pain points include:
- Blueprint cards have fixed fractional widths causing poor single-card display
- Scraper fails when AutoScout24 changes HTML structure
- Manual datetime handling causes database compatibility issues
- No standardized error responses across API endpoints
- Component structure lacks reusability

## Goals / Non-Goals

**Goals:**
- Create a reusable component library with consistent styling and responsive behavior
- Build a robust scraping framework that handles HTML structure changes gracefully
- Standardize datetime handling to prevent database truncation errors
- Implement consistent API response format with proper error handling
- Improve code maintainability through better structure and documentation

**Non-Goals:**
- Rewriting the entire application from scratch
- Changing the database schema or migrating to a different database
- Adding new scraping sources beyond improving existing ones
- Implementing authentication/authorization changes
- Performance optimization (beyond incidental improvements)

## Decisions

### 1. Component Architecture: Fixed-Width Cards with Flexbox
**Decision:** Use fixed-width cards (320-384px) in a flex container with gap spacing instead of fractional widths (w-1/2, w-1/3, etc.)

**Rationale:** Fractional widths cause single cards to appear very narrow on large screens. Fixed widths with flexbox provide consistent card sizes regardless of quantity while maintaining responsiveness.

**Alternatives Considered:**
- CSS Grid with minmax(): More complex, harder to reason about
- Keep fractional widths: Doesn't solve the single-card problem

### 2. Scraper Pattern: Direct Article Parsing
**Decision:** Extract data directly from listing page article elements instead of navigating to detail pages

**Rationale:** AutoScout24's detail page URLs return 404. Images and most car data are available in the listing page itself, reducing HTTP requests and improving speed.

**Alternatives Considered:**
- Selenium-based scraping: Slower, requires browser, higher resource usage
- API reverse engineering: Fragile, likely blocked

### 3. Datetime Strategy: Microsecond Removal in BaseModel
**Decision:** Use `datetime.now().replace(microsecond=0)` in BaseModel initialization

**Rationale:** MySQL DATETIME columns don't support microseconds by default. Removing microseconds at creation prevents truncation errors throughout the application.

**Alternatives Considered:**
- Convert on read from database: Doesn't prevent insert errors
- Use DATETIME(6) columns: Requires schema migration, not worth complexity

### 4. API Response Format: Envelope Pattern
**Decision:** Standardize on `{success: bool, data: any, error: {code, message}}` envelope

**Rationale:** Provides consistent client-side error handling and allows metadata without polluting data structure.

**Alternatives Considered:**
- Raw responses: Inconsistent, harder to handle errors
- Problem Details (RFC 7807): Overkill for this application size

### 5. Image Fetching: Picture Element Extraction
**Decision:** Find `<picture>` element in article, extract `<img>` src, fetch from AutoScout24 CDN

**Rationale:** Images are already in the listing HTML. The picture element contains the car image (2nd or 3rd img tag in article).

**Alternatives Considered:**
- Construct URL from patterns: Brittle when CDN structure changes
- Skip images: Reduces user experience value

## Risks / Trade-offs

**Risk:** AutoScout24 changes HTML structure again  
→ **Mitigation:** Use more flexible selectors (find by element type rather than class names), add fallback strategies, log parsing failures for quick detection

**Risk:** Fixed-width cards may not work on very small screens  
→ **Mitigation:** Use responsive width classes (w-full on mobile, fixed on larger screens), test on multiple viewport sizes

**Risk:** Removing microseconds might cause timestamp collision in high-frequency operations  
→ **Mitigation:** Acceptable trade-off since car scraping is not high-frequency (max a few per second), and UUIDs provide uniqueness

**Trade-off:** Envelope pattern adds response payload size  
→ **Acceptable:** Minimal overhead (~20 bytes) for consistency benefits, not a concern for this application's scale
