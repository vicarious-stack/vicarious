# Project Plan - Vicarious

## Objective
Deliver a complete 80,000+ word premium book ("Vicarious") and a high-quality vanilla web-based reader application. Ensure total adherence to quality requirements, style profiling, validation scripts, and integrity checks.

## Milestones & Timeline
1. **Milestone 0: Project Decomposition & Architecture (PROJECT.md)**
   - Define exact chapters, interludes, and target word counts.
   - Specify build/validate script behaviors.
   - Establish E2E testing framework/structure.

2. **Milestone 1: E2E Test Suite Creation (Dual Track - Testing)**
   - Build test runner and infrastructure.
   - Define 4 Tiers of E2E tests (minimum threshold calculations).
   - Verify test suite readiness and write `TEST_READY.md`.

3. **Milestone 2: Content & Reader App Implementation (Dual Track - Implementation)**
   - Generate all chapters and interludes matching structural and formatting requirements.
   - Implement premium vanilla reader app (`index.html`) supporting multiple themes, pagination, typography, size controls, custom callout rendering, and persistence.
   - Build scripts: `assemble.py`, `word_count.py`, and `validate.py`.

4. **Milestone 3: Integration, E2E Testing, & Hardening**
   - Run `word_count.py` and `validate.py` on implemented content and code.
   - Integrate build scripts, run E2E test suite.
   - Execute Phase 2 (Adversarial Coverage Hardening) for unit/integration/E2E test gaps.

5. **Milestone 4: Victory Audit (Forensic Audit)**
   - Run the Forensic Auditor (`teamwork_preview_auditor`) to verify implementation authenticity.
   - Review audit verdict (must be CLEAN, zero-tolerance policy for cheats/facades).
   - Deliver final handoff to parent Sentinel.

## Resource Allocation & Spawning Strategy
- We will spawn specialists:
  - **Explorer** to analyze and plan content structures, app code base, and tests.
  - **Worker** to write python scripts, reader application code, and test suite files.
  - **Reviewer** to check correctness, word count validations, and formatting constraints.
  - **Challenger** to write adversarial tests and stress test the web application.
  - **Auditor** to perform forensic checks.

## Coordination & Fault Tolerance
- Recurring heartbeat check every 10 minutes.
- Safety timers on every subagent dispatch.
- Self-succession at 16 spawn threshold.
