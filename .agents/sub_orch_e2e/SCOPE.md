# Scope: E2E Testing Track

## Architecture
- The test suite is a standalone suite located in the `e2e_tests/` directory at the project root.
- It targets the book content files, the build scripts (`assemble.py`, `word_count.py`, `validate.py`), and the web reader application (`index.html`).
- The test runner must be executable from the command line and produce clear outputs detailing passed/failed test cases across all Tiers.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| M1.1 | Environment Exploration | Investigate available system dependencies (Python packages, Node.js, browsers) | None | DONE |
| M1.2 | Test Infrastructure Design | Create test runner skeleton, layout `e2e_tests/` directory, and define HTML validation strategy | M1.1 | IN_PROGRESS |
| M1.3 | Tier 1 Tests Implementation | Write >= 55 test cases covering F1-F11 happy paths | M1.2 | PLANNED |
| M1.4 | Tier 2 Tests Implementation | Write >= 55 boundary/corner test cases | M1.3 | PLANNED |
| M1.5 | Tier 3 & 4 Tests Implementation | Write >= 11 cross-feature tests and >= 6 real-world workloads | M1.4 | PLANNED |
| M1.6 | Execution Verification & Docs | Verify test suite execution, produce `TEST_INFRA.md` and `TEST_READY.md` | M1.5 | PLANNED |

## Interface Contracts
### E2E Test Suite Execution
- Running command: `python e2e_tests/run_tests.py` or similar
- Outputs: Detailed console print and JSON file containing test counts and execution status.
- Dependency verification: Checks if web reader works correctly without using external live internet (CODE_ONLY).
