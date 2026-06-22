# Project: Vicarious Book and Reader App

## Architecture
This project consists of two parallel tracks:
1. **Implementation Track**: Responsible for writing the book content (Prologue, 12 Chapters, 6 Interludes, Epilogue, Appendices, Style Profile, Master Outline) and implementing the premium vanilla web reader app (`index.html`) along with build and validation python scripts.
2. **E2E Testing Track**: Responsible for building a comprehensive, requirement-driven, opaque-box E2E test suite. It will publish `TEST_READY.md` when the test suite is complete and ready.

### Code Layout
The workspace layout is defined as follows:
- Content Files:
  - `style_profile.md`
  - `master_outline.md`
  - `prologue.md`
  - `chapter_01.md` through `chapter_12.md`
  - `interlude_01.md` through `interlude_06.md`
  - `epilogue.md`
  - `appendices.md`
- Reader App:
  - `index.html` (vanilla HTML/CSS/JS with marked.js for rendering, Lora, Inter, and Fira Code fonts, and LocalStorage caching)
  - `the_vicarious_complete.md` (assembled single file)
- Build System:
  - `assemble.py` (concatenates chapters in order with TOC)
  - `word_count.py` (verifies word counts against mins)
  - `validate.py` (checks validation rules, name consistency, bans, etc.)
- Test Suite:
  - `e2e_tests/` (directory containing E2E test runner and scripts)
  - `TEST_READY.md` (status of the E2E testing track)
  - `TEST_INFRA.md` (test architecture, feature inventory, tiers mapping)

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| M1 | E2E Testing Track | Define test infra, draft test cases for Tiers 1-4, publish `TEST_READY.md` and `TEST_INFRA.md` | None | PLANNED |
| M2 | Style & Outline | Write `style_profile.md` and `master_outline.md` | None | PLANNED |
| M3 | Content Gen | Generate all chapters, interludes, prologue, epilogue, appendices | M2 | PLANNED |
| M4 | Reader & Build | Implement `index.html`, `assemble.py`, `word_count.py`, `validate.py` | M1, M3 | PLANNED |
| M5 | Integration & Test | Run assemble and validate; run full E2E test suite (Phase 1); run adversarial hardening (Phase 2) | M4 | PLANNED |
| M6 | Forensic Audit | Run Victory Auditor for final integrity check and validation | M5 | PLANNED |

## Interface Contracts
### `validate.py` Validation Rules
- Must verify existence of all 24 markdown files.
- Must verify that each chapter file has >= 3,000 words and each interlude has >= 3,500 words, and the total book word count is >= 80,000.
- Must verify that no forbidden phrase from `style_profile.md` is present in any narrative chapter.
- Must check character name consistency.
- Must verify that each interlude has >= 2 ASCII diagrams (fenced code blocks) and >= 1 "Vicarious Insight" box and >= 1 "Reality Check" box.

### Web Reader ↔ Markdown Interface
- Web Reader must load `the_vicarious_complete.md` via `fetch()`.
- Markdown must be split into sections at `H1` boundaries for pagination.
- LocalStorage keys: `vicarious_current_section`, `vicarious_theme`, `vicarious_font_size`.
