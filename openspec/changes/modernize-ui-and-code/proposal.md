## Why

The current UI has usability issues (narrow blueprint cards, inconsistent styling) and the codebase contains technical debt including deprecated approaches, outdated scraping logic, and manual datetime handling that causes bugs. Modernizing both will improve user experience and maintainability.

## What Changes

- **UI Modernization**: Redesign blueprint cards, improve responsive layouts, enhance visual consistency across all pages, add better feedback for user actions
- **Code Quality**: Refactor scrapers to use modern HTML parsing, standardize datetime handling across models, improve error handling, add input validation
- **Frontend Architecture**: Upgrade component structure, improve state management, add proper loading states and error boundaries
- **Backend Improvements**: Consolidate duplicate logic, add proper logging, improve database query efficiency, standardize API response formats

## Capabilities

### New Capabilities
- `ui-components`: Modern, reusable Vue components with consistent styling and responsive design
- `scraper-framework`: Unified scraping framework with proper error handling and image fetching
- `api-standards`: Standardized API response formats with proper error codes and validation

### Modified Capabilities
<!-- No existing capabilities are being modified, only new ones introduced -->

## Impact

**Affected Code:**
- Frontend: All Vue components in `frontend/src/components/`
- Backend: Scraper modules in `backend/scrapers/`, route handlers in `backend/routes/`, models in `backend/models/`
- Styling: Tailwind CSS configuration and component styles

**APIs:**
- Car listing endpoints may return additional metadata
- Error responses will follow new standardized format

**Dependencies:**
- May update Vue.js and related frontend dependencies to latest stable versions
- Python dependencies remain stable, only code improvements
