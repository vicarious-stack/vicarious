# Plan: E2E Test Suite Development

## Mission
Design, implement, and verify a comprehensive, requirement-driven, opaque-box E2E test suite for the "Vicarious" book content and reader application.

## Feature Inventory (N = 11)
- **F1: Content Presence & Layout**: Verifies that all 24 individual markdown files exist and contain content.
- **F2: Book Assembly & Word Counts**: Verifies compilation of `the_vicarious_complete.md` by `assemble.py`, and word count verification by `word_count.py` and `validate.py` (total >= 80k words, chapters >= 3k, interludes >= 3.5k).
- **F3: Content Quality & Conventions**: Verifies that chapters start with physical/sensory verbs, contain >=3 sensory details, Digital Ledger entries, character names are present, interludes have ASCII diagrams, callouts, and academic citations, and style profile forbidden phrases are not in narrative chapters.
- **F4: Web Reader Theme Switcher**: Verifies that three color themes (Midnight Void, Warm Alabaster, Amber Night) are switchable and apply the correct CSS styling.
- **F5: Web Reader Typography & Header**: Verifies UI typography (Lora, Inter, Fira Code) and title/credits.
- **F6: Web Reader Pagination**: Verifies H1-boundary splitting, page-by-page display, Next/Prev navigation buttons.
- **F7: Web Reader Table of Contents**: Verifies collapsible sidebar with table of contents and highlighting of the active section.
- **F8: Web Reader Text Controls**: Verifies font size controls (increase, decrease, reset).
- **F9: Web Reader State Persistence**: Verifies that active theme, current section, and font size are stored and restored from LocalStorage.
- **F10: Web Reader Custom Callout Parsing**: Verifies parsing and styling of "Vicarious Insight" and "Reality Check" boxes.
- **F11: Web Reader Progress & Layout**: Verifies reading progress bar updates on scroll, responsive hamburger menu, and smooth transition animations.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| M1.1 | Environment Exploration | Investigate available system dependencies (Python packages, Node.js, browsers) | None | DONE |
| M1.2 | Test Infrastructure Design | Create test runner skeleton, layout `e2e_tests/` directory, and define HTML validation strategy | M1.1 | IN_PROGRESS |
| M1.3 | Tier 1 Tests Implementation | Write >= 55 test cases covering F1-F11 happy paths | M1.2 | PLANNED |
| M1.4 | Tier 2 Tests Implementation | Write >= 55 boundary/corner test cases | M1.3 | PLANNED |
| M1.5 | Tier 3 & 4 Tests Implementation | Write >= 11 cross-feature tests and >= 6 real-world workloads | M1.4 | PLANNED |
| M1.6 | Execution Verification & Docs | Verify test suite execution, produce `TEST_INFRA.md` and `TEST_READY.md` | M1.5 | PLANNED |

## Code Layout
All tests will be created within:
- `C:\Users\Dell\.gemini\antigravity\scratch\vicarious\e2e_tests/`

Coordination files at project root:
- `C:\Users\Dell\.gemini\antigravity\scratch\vicarious\TEST_INFRA.md`
- `C:\Users\Dell\.gemini\antigravity\scratch\vicarious\TEST_READY.md`
