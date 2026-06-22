# E2E Test Suite Structure & Plan

This document drafts the structure and test cases for the E2E Test Suite for the "Vicarious" book content and reader application.

## Test Philosophy & Framework Selection
Due to the `CODE_ONLY` network isolation and interactive command-line permission constraints, standard browser automation tools (Selenium, Playwright) cannot be downloaded or executed. 
Therefore, we will design a lightweight, pure-Python testing framework (`e2e_tests/run_tests.py`) that:
1. Runs compilation and validation scripts (`assemble.py`, `word_count.py`, `validate.py`) and checks their outputs.
2. Statically parses and audits the HTML structures in `index.html` using `BeautifulSoup4`.
3. Performs deep static code audits and regular expression validation on the JavaScript implementation in `index.html` to verify state management, local storage key mapping, pagination algorithms, progress bar calculations, and callout parser rules.
4. Executes simulated browser behavior tests by parsing the DOM structure and checking it against structural and logical expectations.

---

## Feature Inventory (N = 11)
- **F1**: Content Presence & Layout
- **F2**: Book Assembly & Word Counts
- **F3**: Content Quality & Conventions
- **F4**: Web Reader Theme Switcher
- **F5**: Web Reader Typography & Header
- **F6**: Web Reader Pagination
- **F7**: Web Reader Table of Contents
- **F8**: Web Reader Text Controls
- **F9**: Web Reader State Persistence
- **F10**: Web Reader Custom Callout Parsing
- **F11**: Web Reader Progress & Layout

---

## Test Cases (127 total)

### Tier 1 - Feature Coverage (55 tests)
#### F1: Content Presence & Layout
1. `test_t1_f1_files_exist`: Verifies that all 24 individual markdown files exist.
2. `test_t1_f1_non_empty`: Verifies that each markdown file is non-empty.
3. `test_t1_f1_header_format`: Verifies that each markdown file starts with a valid header.
4. `test_t1_f1_narrative_h1`: Verifies that each narrative chapter file contains at least one H1 header.
5. `test_t1_f1_style_profile_structure`: Verifies that the style profile file contains expected style guidelines.

#### F2: Book Assembly & Word Counts
6. `test_t1_f2_assemble_correct_order`: Verifies that assemble.py compiles files in the correct sequence.
7. `test_t1_f2_compiled_file_exists`: Verifies that the compiled `the_vicarious_complete.md` exists.
8. `test_t1_f2_compiled_contains_title`: Verifies that `the_vicarious_complete.md` contains the title page.
9. `test_t1_f2_compiled_contains_toc`: Verifies that `the_vicarious_complete.md` contains the table of contents.
10. `test_t1_f2_word_count_output`: Verifies that `word_count.py` correctly computes and reports counts for all files.

#### F3: Content Quality & Conventions
11. `test_t1_f3_narrative_sensory_opening`: Verifies that narrative chapters open with physical/sensory verbs.
12. `test_t1_f3_sensory_details`: Verifies that each chapter contains >=3 sensory details (different senses).
13. `test_t1_f3_digital_ledger_presence`: Verifies that each chapter contains a Digital Ledger entry.
14. `test_t1_f3_interlude_ascii_diagrams`: Verifies that interludes contain >=2 ASCII diagrams.
15. `test_t1_f3_interlude_academic_citations`: Verifies that interludes cite >=3 researchers or studies.

#### F4: Web Reader Theme Switcher
16. `test_t1_f4_theme_buttons_exist`: Verifies that `index.html` contains theme toggle buttons.
17. `test_t1_f4_midnight_void_css`: Verifies "Midnight Void" theme colors exist (#0b0d10, #e2e8f0, #00b4d8).
18. `test_t1_f4_warm_alabaster_css`: Verifies "Warm Alabaster" theme colors exist (#fcfaf6, #1e2022, #c05c3c).
19. `test_t1_f4_amber_night_css`: Verifies "Amber Night" theme colors exist (#161412, #ebd8b2, #d4af37).
20. `test_t1_f4_default_theme_handling`: Verifies that the default theme is set when no preference is saved.

#### F5: Web Reader Typography & Header
21. `test_t1_f5_google_fonts_loaded`: Verifies that `index.html` loads Inter, Lora, and Fira Code.
22. `test_t1_f5_body_font_css`: Verifies body CSS specifies Lora as font family.
23. `test_t1_f5_header_font_css`: Verifies header CSS specifies Inter as font family.
24. `test_t1_f5_code_font_css`: Verifies code blocks/ASCII diagrams specify Fira Code.
25. `test_t1_f5_header_title_credits`: Verifies that the reader app header displays "VICARIOUS" and "by Vijay".

#### F6: Web Reader Pagination
26. `test_t1_f6_js_split_boundaries`: Verifies JS contains logic to split markdown at H1 boundaries.
27. `test_t1_f6_next_button_exists`: Verifies "Next" navigation button exists.
28. `test_t1_f6_prev_button_exists`: Verifies "Previous" navigation button exists.
29. `test_t1_f6_content_update_navigation`: Verifies content updates when page navigation functions are called.
30. `test_t1_f6_bounds_checking`: Verifies pagination bounds are checked (prev disabled on page 1).

#### F7: Web Reader Table of Contents
31. `test_t1_f7_sidebar_exists`: Verifies collapsible sidebar element exists in `index.html`.
32. `test_t1_f7_dynamic_toc_logic`: Verifies JavaScript builds TOC dynamically from H1 headers.
33. `test_t1_f7_toc_click_nav`: Verifies TOC items are clickable and trigger navigation.
34. `test_t1_f7_toc_highlight_active`: Verifies active section in the TOC is highlighted.
35. `test_t1_f7_sidebar_toggle`: Verifies sidebar state (open/collapsed) is toggleable.

#### F8: Web Reader Text Controls
36. `test_t1_f8_increase_button_exists`: Verifies "Increase Font Size" button exists.
37. `test_t1_f8_decrease_button_exists`: Verifies "Decrease Font Size" button exists.
38. `test_t1_f8_reset_button_exists`: Verifies "Reset Font Size" button exists.
39. `test_t1_f8_click_modifies_dom`: Verifies clicking font control buttons modifies content container CSS.
40. `test_t1_f8_font_size_bounds`: Verifies font size stays within limits.

#### F9: Web Reader State Persistence
41. `test_t1_f9_theme_saves`: Verifies JS contains `localStorage.setItem` for active theme.
42. `test_t1_f9_section_saves`: Verifies JS contains `localStorage.setItem` for active section.
43. `test_t1_f9_font_size_saves`: Verifies JS contains `localStorage.setItem` for active font size.
44. `test_t1_f9_load_restores`: Verifies JS contains `localStorage.getItem` on page load to restore settings.
45. `test_t1_f9_restore_applies_dom`: Verifies settings are successfully applied to DOM on startup.

#### F10: Web Reader Custom Callout Parsing
46. `test_t1_f10_insight_js_parsing`: Verifies JS parses blockquotes containing "Vicarious Insight:" correctly.
47. `test_t1_f10_reality_check_js_parsing`: Verifies JS parses blockquotes containing "Reality Check:" correctly.
48. `test_t1_f10_callout_classes_applied`: Verifies parsed callouts are wrapped in custom CSS classes.
49. `test_t1_f10_insight_css_styles`: Verifies CSS contains distinct styling rules for "Vicarious Insight" cards.
50. `test_t1_f10_reality_check_css_styles`: Verifies CSS contains distinct styling rules for "Reality Check" cards.

#### F11: Web Reader Progress & Layout
51. `test_t1_f11_progress_bar_exists`: Verifies reading progress bar element exists in `index.html`.
52. `test_t1_f11_scroll_listener`: Verifies scroll event listener is attached to update progress bar.
53. `test_t1_f11_hamburger_exists`: Verifies hamburger menu button exists and is visible on narrow viewports.
54. `test_t1_f11_transition_animations`: Verifies transition animations (fade class/CSS transition) exist.
55. `test_t1_f11_reading_time_indicator`: Verifies reading time indicator exists and calculates (~200 wpm).

---

### Tier 2 - Boundary & Corner Cases (55 tests)
#### F1 Content Boundaries
56. `test_t2_f1_empty_content_files`: Checks behavior with empty or whitespace-only files.
57. `test_t2_f1_only_headers`: Checks behavior with files containing only headers.
58. `test_t2_f1_large_content`: Checks behavior with excessively large content (word count threshold limits).
59. `test_t2_f1_duplicate_headers`: Checks behavior when a file has duplicate header names.
60. `test_t2_f1_missing_file_validation`: Verifies validation fails when any of the 24 files are missing.

#### F2 Assembly Boundaries
61. `test_t2_f2_read_only_source`: Checks assemble.py when source file is read-only.
62. `test_t2_f2_missing_out_dir`: Checks assemble.py when output file directory doesn't exist.
63. `test_t2_f2_exact_min_words`: Checks word_count.py when file has exactly minimum required words.
64. `test_t2_f2_exact_min_minus_one`: Checks word_count.py when file has exactly minimum - 1 words (must fail).
65. `test_t2_f2_mixed_case_names`: Checks validate.py when name consistency check encounters mixed-case names.

#### F3 Quality Boundaries
66. `test_t2_f3_sensory_verb_in_header`: Checks sensory details checker when sensory verbs are in headers only (should not count).
67. `test_t2_f3_concatenated_sensory_words`: Checks sensory details validation when sensory words are concatenated.
68. `test_t2_f3_partial_forbidden_match`: Checks forbidden phrase checker when a forbidden phrase is part of another word.
69. `test_t2_f3_zero_ascii_diagrams`: Checks ASCII diagram parser with zero diagrams in interlude (must fail).
70. `test_t2_f3_one_ascii_diagram`: Checks ASCII diagram parser with exactly 1 diagram in interlude (must fail).

#### F4 Theme Switcher Boundaries
71. `test_t2_f4_invalid_theme_value`: Checks behavior when an invalid theme is set in LocalStorage (should default to Midnight Void).
72. `test_t2_f4_system_theme_query`: Checks theme switcher under dark/light system preference queries.
73. `test_t2_f4_rapid_theme_clicks`: Checks theme application when theme button is double-clicked rapidly.
74. `test_t2_f4_theme_class_target`: Checks theme class application on body vs layout wrapper.
75. `test_t2_f4_accent_contrast_ratio`: Checks accent color contrast ratios for accessibility.

#### F5 Typography Boundaries
76. `test_t2_f5_google_fonts_offline`: Checks font loading fallback behavior when Google Fonts CDN is slow or fails.
77. `test_t2_f5_readability_metrics`: Checks line-height and letter-spacing settings for text readability.
78. `test_t2_f5_theme_codeblock_styles`: Checks styling of tables and inline code blocks under all three themes.
79. `test_t2_f5_standard_blockquote_styles`: Checks styling of standard blockquotes that are NOT custom callouts.
80. `test_t2_f5_superscript_formatting`: Checks formatting of superscript citations (academic citations).

#### F6 Pagination Boundaries
81. `test_t2_f6_single_page_book`: Checks pagination on a book with exactly one page (H1).
82. `test_t2_f6_prev_first_page`: Checks pagination bounds: clicking "Prev" on page 1 does nothing/doesn't throw.
83. `test_t2_f6_next_last_page`: Checks pagination bounds: clicking "Next" on the last page does nothing/doesn't throw.
84. `test_t2_f6_no_h1_headers`: Checks behavior when book content has multiple nested headers without H1.
85. `test_t2_f6_scroll_reset_on_nav`: Checks scroll recovery when navigating between chapters (does it scroll to top?).

#### F7 TOC Boundaries
86. `test_t2_f7_empty_h1_title`: Checks TOC generation when a chapter has an empty H1 title.
87. `test_t2_f7_active_toc_boundary`: Checks active TOC highlighting when scroll position is exactly at a boundary.
88. `test_t2_f7_special_char_headers`: Checks TOC behavior with special characters or HTML entities in headers.
89. `test_t2_f7_ultrasmall_viewport`: Checks sidebar toggle under very small screen widths (e.g. 320px).
90. `test_t2_f7_large_toc_overflow`: Checks sidebar behavior when the book has 100+ chapters (overflow scrolling).

#### F8 Font Size Boundaries
91. `test_t2_f8_min_font_limit`: Checks minimum font size constraint (e.g., cannot decrease below 12px).
92. `test_t2_f8_max_font_limit`: Checks maximum font size constraint (e.g., cannot increase above 32px).
93. `test_t2_f8_reset_font_value`: Checks font size reset returns to precisely the default (e.g. 18px).
94. `test_t2_f8_step_increment_value`: Checks font size steps increase/decrease in consistent increments (e.g. 2px).
95. `test_t2_f8_max_reflow_limit`: Checks layout reflow when font size is at its maximum limit.

#### F9 LocalStorage Boundaries
96. `test_t2_f9_localstorage_disabled`: Checks behavior when LocalStorage is disabled or throws an exception.
97. `test_t2_f9_corrupt_storage_data`: Checks LocalStorage with corrupted state values (e.g. non-numeric font size, invalid section name).
98. `test_t2_f9_missing_section_restore`: Checks state recovery when section in LocalStorage no longer exists in book.
99. `test_t2_f9_save_frequency`: Checks state save frequency (does it save immediately on interaction?).
100. `test_t2_f9_storage_side_effects`: Checks LocalStorage quota handling or clearing side-effects.

#### F10 Callouts Boundaries
101. `test_t2_f10_nested_blockquotes`: Checks callout parsing with nested blockquotes.
102. `test_t2_f10_lowercase_markers`: Checks callout parsing when callout marker is lowercased (e.g., "vicarious insight:").
103. `test_t2_f10_padded_markers`: Checks callout parsing when callout has leading/trailing whitespaces.
104. `test_t2_f10_multiline_callouts`: Checks callout parsing when callout spans multiple paragraphs.
105. `test_t2_f10_markdown_in_callouts`: Checks callout rendering when callout contains markdown elements (bold, links).

#### F11 Layout Boundaries
106. `test_t2_f11_breakpoint_exact`: Checks layout responsiveness at exactly 768px viewport width.
107. `test_t2_f11_breakpoint_below`: Checks layout responsiveness at 767px (mobile view active).
108. `test_t2_f11_breakpoint_above`: Checks layout responsiveness at 769px (desktop view active).
109. `test_t2_f11_short_content_scroll`: Checks reading progress bar calculation when page content is very short.
110. `test_t2_f11_zero_words_reading_time`: Checks estimated reading time calculation when a chapter has 0 words.

---

### Tier 3 - Cross-Feature Combinations (11 tests)
111. `test_t3_theme_preserves_page`: Test that switching themes preserves the current reading page/section and scroll progress.
112. `test_t3_fontsize_updates_progress`: Test that changing font size updates progress bar percentage correctly.
113. `test_t3_toc_updates_persistence`: Test that navigating via TOC updates the active page, progress bar, and saves new section to LocalStorage.
114. `test_t3_callout_theme_variations`: Test that custom callouts render with appropriate styling variations depending on the active theme.
115. `test_t3_sidebar_state_nav_preserves`: Test that sidebar state (open/collapsed) is maintained across page navigation.
116. `test_t3_resize_updates_progress`: Test that resizing the browser window updates the reading progress bar and collapsible menu layout.
117. `test_t3_double_click_toc`: Test that double-clicking a TOC item does not break pagination or cause UI glitch.
118. `test_t3_fontsize_limits_theme`: Test that font size limits work correctly when switching themes back and forth.
119. `test_t3_marked_errors_graceful`: Test that marked.js parsing errors (if any) are handled gracefully without breaking pagination or TOC.
120. `test_t3_toc_transition_fade`: Test that layout transitions (fading) work correctly when navigating via TOC compared to Next/Prev buttons.
121. `test_t3_reading_time_adjustments`: Test that estimated reading time adjusts dynamically if reading speed parameters or word densities change.

---

### Tier 4 - Real-World Application Scenarios (6 tests)
122. `test_t4_complete_assembled_book_verification`: Run build scripts to compile `the_vicarious_complete.md`, count words, run validations, and check that the resulting markdown is loaded and parsed correctly in the reader.
123. `test_t4_first_time_user_journey`: Load the reader with empty LocalStorage. Verify default theme (Midnight Void), page 1 (Prologue), default font size (18px), and check that TOC is generated and visible.
124. `test_t4_active_reader_session`: Navigate to Chapter 3, switch theme to Warm Alabaster, increase font size twice, scroll to 50%, reload page. Verify theme is Warm Alabaster, font size is increased, page is Chapter 3, and scroll position/progress is restored or correctly aligned.
125. `test_t4_mobile_reading_session`: Simulate viewport < 768px. Verify sidebar collapses into hamburger menu, click hamburger to open sidebar, click a section to navigate, check sidebar auto-collapses, and progress bar works correctly on touch scroll.
126. `test_t4_interactive_validation_cli`: Verify that the CLI output of the validation scripts reports passing status when all book constraints are met, and failing status when a constraint is intentionally violated (e.g. introducing a forbidden phrase or removing a file).
127. `test_t4_e2e_assembly_html_ui_verification`: Simulate the full pipeline. Compile the book, mock browser loading, parse elements, and verify content formatting (headers, citations, ASCII diagrams, custom callouts) matches expected DOM structures.
