# Guidelines for Milestone 3 Batch 1 Content Generation

You are tasked with drafting the first batch of narrative and scientific content for the book *Vicarious*. 

## Target Files and Word Counts
1. `prologue.md` - Target: >= 2,500 words. (Narrative: Month 0)
2. `chapter_01.md` - Target: >= 3,500 words. (Narrative: Month 1)
3. `chapter_02.md` - Target: >= 3,500 words. (Narrative: Month 2)
4. `interlude_01.md` - Target: >= 4,000 words. (Science: Dopamine neurobiology)

Total word count for these files must be at least 13,500 words.

## General Writing Rules (from `style_profile.md`)
- **Tone & Style Blend**: Synthesize the 8 literary traditions outlined in `style_profile.md` (Daniel Kahneman, Jiddu Krishnamurti, Yuval Noah Harari, Albert Camus, Seneca, Robert Sapolsky, Gabor Maté, James Baldwin).
- **Rule of Three Senses**: Every narrative scene must establish at least three distinct senses (using visual, auditory, olfactory, tactile, or gustatory markers localized to Pune).
- **Physiological Precision**: Describe somatic and physiological signatures of emotions (e.g. chest pressure, throat constriction, carpal tunnel ache) rather than naming them directly.
- **Banned AI Phrases**: Check the list of 60 banned phrases in `style_profile.md` (e.g., "delve into", "testament to", "tapestry of", "beacon of", "took a deep breath"). Do not use any of them. If you do, the validator will fail.
- **Name Consistency**: Use the exact character names: `Kiran`, `Priya`, `Venky Sir`, `Adi`, `Dr. Meera`, `Rohan`.

## Formatting Conventions
- **Callout Boxes**: Interludes must contain callout boxes formatted exactly as:
  ```markdown
  > **VICARIOUS INSIGHT: [Title in All Caps]**
  > [Text]
  ```
  ```markdown
  > **REALITY CHECK: [Title in All Caps]**
  > [Text]
  ```
- **Digital Ledger Entries**: Narrative units (Chapter 1 and Chapter 2) must each contain exactly one digital ledger entry formatted as a JSON block with the `json` language identifier. See `style_profile.md` or `master_outline.md` for the schema.

## Specific Outline Requirements (from `master_outline.md`)

### Prologue: "The Observer"
- **Setting**: A 10x12 PG room in Kothrud, Pune, at 11:45 PM on a sticky June night. Rusty ceiling fan rattle, muffled honks from Karve Road, scent of cold tiffin, cotton shirt sticking to spine.
- **Character Actions**: Kiran lies on his back scrolling. Declines a call from his mother in Nagpur. Stands up to drink warm water, looks at himself in the mirror, returns to scroll.
- **Ledger Entry**: None for the Prologue.

### Chapter 1: "The Scroll"
- **Setting**: PG room, lazy Saturday afternoon. Hot room, dust motes in white light, slippers slapping concrete in the corridor, diesel exhaust from the street.
- **Character Actions**: Kiran scrolls through Instagram reels (Ladakh, coding influencers, cricket). Adi sits on his bed checking LinkedIn. Kiran orders tiffin online, eats without looking, and dismisses his 41-hour weekly screen-time notification.
- **Ledger Entry**: Exactly 1 JSON ledger block (ledger_entry 1).

### Chapter 2: "The Glitch"
- **Setting**: QA bay at Neuralis, Hinjawadi, on a Monday morning. Dual monitors, sterile lights, hum of server room AC, keyboard clicks.
- **Character Actions**: Kiran copies test cases from Sprint 14 to Sprint 15 database schema. Clicks "Execute" without reading SQL. Truncates shipping addresses, halting 400 delivery trucks. Sunita pulls him into a meeting and places him on a 90-day Performance Improvement Plan (PIP).
- **Ledger Entry**: Exactly 1 JSON ledger block (ledger_entry 2).

### Interlude I: "The Dopamine Machine"
- **Scientific Focus**: Neurobiology of digital addiction. Anticipation vs. pleasure. Variable-ratio schedules (Skinner). Opponent-process theory (Lembke). Dopamine prediction error (Schultz).
- **Academic Citations**: Must include:
  1. *Schultz, W., Dayan, P., & Montague, P. R. (1997)*
  2. *Lembke, A. (2021)*
  3. *Skinner, B. F. (1953)*
- **ASCII Diagrams**: Must include exactly 2 ASCII diagrams inside fenced code blocks:
  1. "Dopamine Prediction Error (DPE) Cycle"
  2. "Pleasure-Pain Homeostasis"
  See `master_outline.md` section 5.1 for exact text of diagrams.
- **Callouts**: Must include:
  1. `VICARIOUS INSIGHT: THE Slot Machine in the Pocket`
  2. `REALITY CHECK: THE DOPAMINE MYTH`

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. Do not draft placeholder text or short-circuit word counts with repetitive padding or dummy text. The content must be high-quality literary writing meeting the exact minimum word counts.
