# Scope: Vicarious Implementation

## Architecture
The Implementation Track comprises content generation, build system automation, validation logic, and the user interface.
The workspace directory is `C:\Users\Dell\.gemini\antigravity\scratch\vicarious`.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M2 | Style & Outline | Write `style_profile.md` and `master_outline.md` | None | DONE |
| M3.1 | Content Gen Batch 1 | `prologue.md`, `chapter_01.md`, `chapter_02.md`, `interlude_01.md` | M2 | IN_PROGRESS |
| M3.2 | Content Gen Batch 2 | `chapter_03.md`, `chapter_04.md`, `interlude_02.md` | M3.1 | PLANNED |
| M3.3 | Content Gen Batch 3 | `chapter_05.md`, `chapter_06.md`, `interlude_03.md` | M3.2 | PLANNED |
| M3.4 | Content Gen Batch 4 | `chapter_07.md`, `chapter_08.md`, `interlude_04.md` | M3.3 | PLANNED |
| M3.5 | Content Gen Batch 5 | `chapter_09.md`, `chapter_10.md`, `interlude_05.md` | M3.4 | PLANNED |
| M3.6 | Content Gen Batch 6 | `chapter_11.md`, `chapter_12.md`, `interlude_06.md`, `epilogue.md`, `appendices.md` | M3.5 | PLANNED |
| M4 | Reader & Build | Implement `assemble.py`, `word_count.py`, `validate.py`, and `index.html` | M3.6 | PLANNED |
| M5 | Integration & Test | Run validation, compile book, run E2E test suite (Phase 1), perform adversarial hardening (Phase 2) | M4 | PLANNED |
| M6 | Forensic Audit | Coordinate Forensic Auditor for validation and final verification | M5 | PLANNED |

## Interface Contracts
### `validate.py` Requirements
- Verifies all 24 markdown files exist.
- Validates word count thresholds for each file.
- Checks name consistency (Kiran, Priya, Venky Sir, Adi, Dr. Meera, Rohan).
- Verifies no forbidden phrases from `style_profile.md` are present.
- Checks interlude specific elements (>= 2 ASCII diagrams inside fenced code blocks, >= 1 "Vicarious Insight" box, >= 1 "Reality Check" box).

### Web Reader (`index.html`) Requirements
- Loads `the_vicarious_complete.md` via `fetch()`.
- Splits sections at H1 markdown headers.
- Implements 3 color themes (Midnight Void, Warm Alabaster, Amber Night).
- Implements font size adjustment.
- Supports collapsible sidebar with table of contents.
- Features horizontal scroll progress bar.
- Calculates and displays read time (~200 wpm).
- Persists user preferences (section, theme, font size) in LocalStorage.
