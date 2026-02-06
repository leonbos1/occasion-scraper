# Implementation Tasks

## 1. Foundation: Database & Models

- [x] 1.1 Update BaseModel datetime handling to use replace(microsecond=0)
- [x] 1.2 Verify all model timestamps (Car, ScrapeSession, BluePrint, User) inherit microsecond removal
- [x] 1.3 Add unit tests for BaseModel datetime creation without microseconds
- [x] 1.4 Test database inserts to ensure no truncation errors occur

## 2. API Layer: Envelope Pattern & Error Handling

- [x] 2.1 Create API response helper functions for success and error envelopes
- [x] 2.2 Define standardized error codes (VALIDATION_ERROR, NOT_FOUND, AUTH_ERROR, DATABASE_ERROR)
- [x] 2.3 Update all car endpoints (/cars, /cars/<id>) to use envelope pattern
- [x] 2.4 Update all blueprint endpoints to use envelope pattern
- [x] 2.5 Update all user endpoints to use envelope pattern
- [x] 2.6 Update all subscription endpoints to use envelope pattern
- [x] 2.7 Convert datetime objects to strings in all API responses using str() and split('.')[0]
- [x] 2.8 Implement consistent input validation with VALIDATION_ERROR responses
- [x] 2.9 Add user-friendly error messages that hide technical details in production
- [x] 2.10 Test error handling for validation, not found, and database errors

## 3. Scraper Framework: Robust Data Extraction

- [x] 3.1 Update autoscout_fast.py to extract car IDs from article data-guid attributes
- [x] 3.2 Update URL construction to use `/offers/{car_id}` pattern
- [x] 3.3 Implement location extraction with fallback (SellerInfo_address span → last span)
- [x] 3.4 Implement picture element parsing to extract img src from listing page
- [x] 3.5 Add image URL validation (only fetch from prod.pictures.autoscout24.net/listing-images)
- [x] 3.6 Update image fetch to return b"" on failure instead of crashing
- [x] 3.7 Refactor selectors to prioritize element types over class names for flexibility
- [x] 3.8 Add multiple fallback strategies for critical data extraction
- [x] 3.9 Implement comprehensive parsing failure logging with context
- [x] 3.10 Test scraper with no cars found scenario (return empty list)
- [x] 3.11 Test scraper with page fetch failure (log error, return empty list)
- [ ] 3.12 Update other scrapers (anwb.py, gaspedaal.py, marktplaats.py) to follow same patterns

## 4. Frontend: Component Architecture & Responsiveness

- [ ] 4.1 Update BlueprintsCardView.vue to use fixed-width cards (w-80/w-96 instead of w-1/2, w-1/3)
- [ ] 4.2 Update card container to use flex flex-wrap justify-center gap-4
- [ ] 4.3 Implement responsive widths (w-full on mobile <640px, fixed on larger screens)
- [ ] 4.4 Test single blueprint card display (should not stretch across screen)
- [ ] 4.5 Test multiple blueprint cards display (should wrap consistently)
- [ ] 4.6 Add loading spinner component for asynchronous operations
- [ ] 4.7 Implement loading states for data fetching in all repository services
- [ ] 4.8 Implement loading states for form submissions (disable buttons, show spinner)
- [ ] 4.9 Add error message components for API failures
- [ ] 4.10 Implement network error handling with retry option
- [ ] 4.11 Update datetime displays to format consistently (YYYY-MM-DD HH:MM:SS, no microseconds)
- [ ] 4.12 Test component responsiveness on mobile, tablet, and desktop viewports

## 5. Integration & Testing

- [ ] 5.1 Update frontend API services to handle new envelope response format
- [ ] 5.2 Update error handling in Vue components to parse standardized error codes
- [ ] 5.3 End-to-end test: Create blueprint, trigger scraper, verify no datetime errors
- [ ] 5.4 End-to-end test: Test API error scenarios and verify user-friendly messages
- [ ] 5.5 End-to-end test: Test single and multiple card layouts on different screen sizes
- [ ] 5.6 Verify all scraper changes work with actual AutoScout24 listings
- [ ] 5.7 Performance test: Verify scraper speed with direct article parsing
- [ ] 5.8 Update README.md with new API response format documentation
- [ ] 5.9 Update README.md with component usage examples
- [ ] 5.10 Final smoke test of all application features

## 6. Documentation & Code Quality

- [ ] 6.1 Add docstrings to all API helper functions
- [ ] 6.2 Add comments explaining envelope pattern usage
- [ ] 6.3 Add comments explaining scraper fallback strategies
- [ ] 6.4 Document error codes in a central location
- [ ] 6.5 Add component prop documentation in Vue files
- [ ] 6.6 Review code for consistent formatting and style
- [ ] 6.7 Clean up unused imports and dead code
- [ ] 6.8 Add type hints to Python functions where missing
