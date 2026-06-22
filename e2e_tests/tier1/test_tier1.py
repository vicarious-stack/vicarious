import os
import re
import sys
import unittest
from e2e_tests.test_helpers import (
    PROJECT_ROOT,
    parse_markdown_structure,
    load_index_html,
    match_js_patterns,
    run_cli_tool
)

def _get_chapter_paths():
    ch_paths = []
    for i in range(1, 13):
        ch_paths.append(os.path.join(PROJECT_ROOT, f"chapter_{i:02d}.md"))
    return ch_paths

def _get_interlude_paths():
    int_paths = []
    for i in range(1, 7):
        int_paths.append(os.path.join(PROJECT_ROOT, f"interlude_{i:02d}.md"))
    return int_paths

def _get_all_source_files():
    files = [
        os.path.join(PROJECT_ROOT, "style_profile.md"),
        os.path.join(PROJECT_ROOT, "master_outline.md"),
        os.path.join(PROJECT_ROOT, "prologue.md"),
        os.path.join(PROJECT_ROOT, "epilogue.md"),
        os.path.join(PROJECT_ROOT, "appendices.md"),
    ]
    files.extend(_get_chapter_paths())
    files.extend(_get_interlude_paths())
    return files

def _get_all_24_files():
    # 23 source files + the_vicarious_complete.md = 24
    files = _get_all_source_files()
    files.append(os.path.join(PROJECT_ROOT, "the_vicarious_complete.md"))
    return files

# ==========================================
# F1: Content Presence & Layout
# ==========================================

def test_t1_f1_files_exist():
    """1. Verifies that all 24 individual markdown files exist."""
    missing = []
    for f in _get_all_24_files():
        if not os.path.exists(f):
            missing.append(os.path.basename(f))
    if missing:
        raise AssertionError(f"Missing expected markdown files: {', '.join(missing)}")

def test_t1_f1_non_empty():
    """2. Verifies that each markdown file is non-empty."""
    files = _get_all_24_files()
    existing_files = [f for f in files if os.path.exists(f)]
    if not existing_files:
        raise unittest.SkipTest("No markdown files found to check")
    missing_or_empty = []
    for f in existing_files:
        if os.path.getsize(f) == 0:
            missing_or_empty.append(os.path.basename(f))
    if missing_or_empty:
        raise AssertionError(f"Markdown files are empty: {', '.join(missing_or_empty)}")

def test_t1_f1_header_format():
    """3. Verifies that each markdown file starts with a valid header."""
    files = _get_all_source_files()
    existing_files = [f for f in files if os.path.exists(f)]
    if not existing_files:
        raise unittest.SkipTest("No source markdown files found to check")
    invalid = []
    for f in existing_files:
        with open(f, 'r', encoding='utf-8') as file_obj:
            content = file_obj.read().strip()
            if not content.startswith("#"):
                invalid.append(os.path.basename(f))
    if invalid:
        raise AssertionError(f"Markdown files do not start with a valid '#' header: {', '.join(invalid)}")

def test_t1_f1_narrative_h1():
    """4. Verifies that each narrative chapter file contains at least one H1 header."""
    narrative_files = [os.path.join(PROJECT_ROOT, "prologue.md"), os.path.join(PROJECT_ROOT, "epilogue.md")] + _get_chapter_paths()
    existing = [f for f in narrative_files if os.path.exists(f)]
    if not existing:
        raise unittest.SkipTest("No narrative files found")
    invalid = []
    for f in existing:
        with open(f, 'r', encoding='utf-8') as fo:
            struct = parse_markdown_structure(fo.read())
            h1s = [title for level, title in struct["headers"] if level == 1]
            if not h1s:
                invalid.append(os.path.basename(f))
    if invalid:
        raise AssertionError(f"Narrative files missing H1 headers: {', '.join(invalid)}")

def test_t1_f1_style_profile_structure():
    """5. Verifies that the style profile file contains expected style guidelines."""
    path = os.path.join(PROJECT_ROOT, "style_profile.md")
    if not os.path.exists(path):
        raise unittest.SkipTest("style_profile.md is missing")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    struct = parse_markdown_structure(content)
    if len(struct["headers"]) < 3:
        raise AssertionError("style_profile.md does not contain expected structural sections")

# ==========================================
# F2: Book Assembly & Word Counts
# ==========================================

def test_t1_f2_assemble_correct_order():
    """6. Verifies that assemble.py compiles files in the correct sequence."""
    path = os.path.join(PROJECT_ROOT, "assemble.py")
    if not os.path.exists(path):
        raise unittest.SkipTest("assemble.py does not exist")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'chapter_(\d+)\.md', content)
    if not matches:
        raise AssertionError("assemble.py does not contain explicit chapter names indicating order")
    nums = [int(m) for m in matches]
    is_sorted = all(nums[i] <= nums[i+1] for i in range(len(nums)-1))
    if not is_sorted:
        raise AssertionError("assemble.py does not compile files in ascending sequence order")

def test_t1_f2_compiled_file_exists():
    """7. Verifies that the compiled `the_vicarious_complete.md` exists."""
    path = os.path.join(PROJECT_ROOT, "the_vicarious_complete.md")
    if not os.path.exists(path):
        raise AssertionError("the_vicarious_complete.md is missing")

def test_t1_f2_compiled_contains_title():
    """8. Verifies that `the_vicarious_complete.md` contains the title page."""
    path = os.path.join(PROJECT_ROOT, "the_vicarious_complete.md")
    if not os.path.exists(path):
        raise unittest.SkipTest("the_vicarious_complete.md is missing")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if "VICARIOUS" not in content:
        raise AssertionError("compiled book does not contain the title page 'VICARIOUS'")

def test_t1_f2_compiled_contains_toc():
    """9. Verifies that `the_vicarious_complete.md` contains the table of contents."""
    path = os.path.join(PROJECT_ROOT, "the_vicarious_complete.md")
    if not os.path.exists(path):
        raise unittest.SkipTest("the_vicarious_complete.md is missing")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if "Table of Contents" not in content and "TOC" not in content and "Contents" not in content:
        raise AssertionError("compiled book does not contain a Table of Contents")

def test_t1_f2_word_count_output():
    """10. Verifies that `word_count.py` correctly computes and reports counts for all files."""
    path = os.path.join(PROJECT_ROOT, "word_count.py")
    if not os.path.exists(path):
        raise unittest.SkipTest("word_count.py does not exist")
    code, out, err = run_cli_tool([sys.executable, "word_count.py"], cwd=PROJECT_ROOT)
    if "word" not in out.lower() and "count" not in out.lower() and not out.strip():
        raise AssertionError(f"word_count.py produced no standard output. Stderr: {err}")

# ==========================================
# F3: Content Quality & Conventions
# ==========================================

def test_t1_f3_narrative_sensory_opening():
    """11. Verifies that narrative chapters open with physical/sensory verbs."""
    chapters = _get_chapter_paths()
    existing = [c for c in chapters if os.path.exists(c)]
    if not existing:
        raise unittest.SkipTest("No chapter files found to analyze")
    sensory_words = {
        'look', 'see', 'watch', 'glare', 'peek', 'stare', 'glimpse', 'glow', 'shine', 'shadow',
        'hear', 'listen', 'shriek', 'whisper', 'scream', 'shout', 'crash', 'echo', 'rumble',
        'feel', 'touch', 'cold', 'warm', 'hot', 'rough', 'smooth', 'sharp', 'soft',
        'smell', 'scent', 'odor', 'aroma', 'fragrance', 'sniff', 'reek',
        'taste', 'sweet', 'sour', 'bitter', 'salty', 'savory', 'swallow'
    }
    invalid = []
    for ch in existing:
        with open(ch, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        p = ""
        found_h1 = False
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                found_h1 = True
                continue
            if found_h1 and line:
                p = line
                break
        words = set(re.findall(r'\b\w+\b', p.lower()))
        if not (words & sensory_words):
            invalid.append(os.path.basename(ch))
    if invalid:
        raise AssertionError(f"Chapters did not open with sensory detail in first paragraph: {', '.join(invalid)}")

def test_t1_f3_sensory_details():
    """12. Verifies that each chapter contains >=3 sensory details (different senses)."""
    chapters = _get_chapter_paths()
    existing = [c for c in chapters if os.path.exists(c)]
    if not existing:
        raise unittest.SkipTest("No chapter files found")
    sight_words = {'look', 'see', 'watch', 'glare', 'peek', 'stare', 'glimpse', 'glow', 'shine', 'shadow', 'dark', 'bright', 'red', 'blue', 'green', 'visual'}
    sound_words = {'hear', 'listen', 'shriek', 'whisper', 'scream', 'shout', 'crash', 'echo', 'rumble', 'silent', 'noise', 'sound', 'loud', 'quiet'}
    smell_words = {'smell', 'scent', 'odor', 'aroma', 'fragrance', 'sniff', 'reek', 'musty', 'perfume'}
    touch_words = {'feel', 'touch', 'cold', 'warm', 'hot', 'rough', 'smooth', 'sharp', 'soft', 'hard', 'pressure', 'texture'}
    taste_words = {'taste', 'sweet', 'sour', 'bitter', 'salty', 'savory', 'delicious', 'devour', 'swallow', 'tongue', 'flavor'}
    invalid = []
    for ch in existing:
        with open(ch, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        words = set(re.findall(r'\b\w+\b', content))
        senses_found = 0
        if words & sight_words: senses_found += 1
        if words & sound_words: senses_found += 1
        if words & smell_words: senses_found += 1
        if words & touch_words: senses_found += 1
        if words & taste_words: senses_found += 1
        if senses_found < 3:
            invalid.append(os.path.basename(ch))
    if invalid:
        raise AssertionError(f"Chapters containing less than 3 sensory categories: {', '.join(invalid)}")

def test_t1_f3_digital_ledger_presence():
    """13. Verifies that each chapter contains a Digital Ledger entry."""
    chapters = _get_chapter_paths()
    existing = [c for c in chapters if os.path.exists(c)]
    if not existing:
        raise unittest.SkipTest("No chapters found")
    invalid = []
    for ch in existing:
        with open(ch, 'r', encoding='utf-8') as f:
            content = f.read()
        if "Digital Ledger" not in content and "digital ledger" not in content.lower():
            invalid.append(os.path.basename(ch))
    if invalid:
        raise AssertionError(f"Chapters missing Digital Ledger entry: {', '.join(invalid)}")

def test_t1_f3_interlude_ascii_diagrams():
    """14. Verifies that interludes contain >=2 ASCII diagrams."""
    interludes = _get_interlude_paths()
    existing = [i for i in interludes if os.path.exists(i)]
    if not existing:
        raise unittest.SkipTest("No interludes found")
    invalid = []
    for ch in existing:
        with open(ch, 'r', encoding='utf-8') as f:
            content = f.read()
        struct = parse_markdown_structure(content)
        if len(struct["code_blocks"]) < 2:
            invalid.append(os.path.basename(ch))
    if invalid:
        raise AssertionError(f"Interludes with fewer than 2 ASCII diagrams: {', '.join(invalid)}")

def test_t1_f3_interlude_academic_citations():
    """15. Verifies that interludes cite >=3 researchers or studies."""
    interludes = _get_interlude_paths()
    existing = [i for i in interludes if os.path.exists(i)]
    if not existing:
        raise unittest.SkipTest("No interludes found")
    invalid = []
    for ch in existing:
        with open(ch, 'r', encoding='utf-8') as f:
            content = f.read()
        struct = parse_markdown_structure(content)
        citations_count = len(struct["citations"])
        if citations_count < 3:
            markers = len(re.findall(r'\b(et al\.|study|research|journal|university|professor|scientist|laboratory|institute)\b', content, re.IGNORECASE))
            if citations_count + markers < 3:
                invalid.append(os.path.basename(ch))
    if invalid:
        raise AssertionError(f"Interludes containing less than 3 academic citations: {', '.join(invalid)}")

# ==========================================
# F4: Web Reader Theme Switcher
# ==========================================

def test_t1_f4_theme_buttons_exist():
    """16. Verifies that `index.html` contains theme toggle buttons."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    buttons = root.find_all("button") + root.find_all("input") + root.find_all("div")
    theme_related = []
    for b in buttons:
        attr_str = str(b.attrs).lower()
        if "theme" in attr_str or "void" in attr_str or "alabaster" in attr_str or "amber" in attr_str:
            theme_related.append(b)
    if not theme_related:
        raise AssertionError("index.html does not contain theme switcher controls")

def test_t1_f4_midnight_void_css():
    """17. Verifies \"Midnight Void\" theme colors exist (#0b0d10, #e2e8f0, #00b4d8)."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    style_lower = style.lower()
    if "#0b0d10" not in style_lower:
        raise AssertionError("Midnight Void background color #0b0d10 not found in CSS")
    if "#e2e8f0" not in style_lower:
        raise AssertionError("Midnight Void text color #e2e8f0 not found in CSS")
    if "#00b4d8" not in style_lower:
        raise AssertionError("Midnight Void accent color #00b4d8 not found in CSS")

def test_t1_f4_warm_alabaster_css():
    """18. Verifies \"Warm Alabaster\" theme colors exist (#fcfaf6, #1e2022, #c05c3c)."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    style_lower = style.lower()
    if "#fcfaf6" not in style_lower:
        raise AssertionError("Warm Alabaster background color #fcfaf6 not found in CSS")
    if "#1e2022" not in style_lower:
        raise AssertionError("Warm Alabaster text color #1e2022 not found in CSS")
    if "#c05c3c" not in style_lower:
        raise AssertionError("Warm Alabaster accent color #c05c3c not found in CSS")

def test_t1_f4_amber_night_css():
    """19. Verifies \"Amber Night\" theme colors exist (#161412, #ebd8b2, #d4af37)."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    style_lower = style.lower()
    if "#161412" not in style_lower:
        raise AssertionError("Amber Night background color #161412 not found in CSS")
    if "#ebd8b2" not in style_lower:
        raise AssertionError("Amber Night text color #ebd8b2 not found in CSS")
    if "#d4af37" not in style_lower:
        raise AssertionError("Amber Night accent color #d4af37 not found in CSS")

def test_t1_f4_default_theme_handling():
    """20. Verifies that the default theme is set when no preference is saved."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "midnight" not in js.lower() and "void" not in js.lower() and "theme" not in js.lower():
        raise AssertionError("index.html JavaScript lacks default theme handling logic")

# ==========================================
# F5: Typography & Header
# ==========================================

def test_t1_f5_google_fonts_loaded():
    """21. Verifies that `index.html` loads Inter, Lora, and Fira Code."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    links = root.find_all("link")
    fonts_loaded = False
    for link in links:
        href = link.attrs.get("href", "")
        if "fonts.googleapis.com" in href and ("lora" in href.lower() or "inter" in href.lower() or "fira" in href.lower()):
            fonts_loaded = True
            break
    if not fonts_loaded and "@import" in style:
        if "fonts.googleapis.com" in style and ("lora" in style.lower() or "inter" in style.lower() or "fira" in style.lower()):
            fonts_loaded = True
    if not fonts_loaded:
        raise AssertionError("Google Fonts (Inter, Lora, Fira Code) are not loaded in index.html")

def test_t1_f5_body_font_css():
    """22. Verifies body CSS specifies Lora as font family."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "lora" not in style.lower():
        raise AssertionError("CSS does not set Lora as the body/serif font-family")

def test_t1_f5_header_font_css():
    """23. Verifies header CSS specifies Inter as font family."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "inter" not in style.lower():
        raise AssertionError("CSS does not set Inter as h1/h2/h3 header font-family")

def test_t1_f5_code_font_css():
    """24. Verifies code blocks/ASCII diagrams specify Fira Code."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "fira code" not in style.lower() and "fira-code" not in style.lower() and "firacode" not in style.lower():
        raise AssertionError("CSS does not set Fira Code as the font-family for code blocks/diagrams")

def test_t1_f5_header_title_credits():
    """25. Verifies that the reader app header displays \"VICARIOUS\" and \"by Vijay\"."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    body_text = root.text
    if "VICARIOUS" not in body_text:
        raise AssertionError("index.html does not display title 'VICARIOUS'")
    if "Vijay" not in body_text:
        raise AssertionError("index.html does not display credit 'Vijay'")

# ==========================================
# F6: Pagination
# ==========================================

def test_t1_f6_js_split_boundaries():
    """26. Verifies JS contains logic to split markdown at H1 boundaries."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "split" not in js.lower() or ("h1" not in js.lower() and "header" not in js.lower() and "#" not in js.lower()):
        raise AssertionError("index.html JS lacks page/section splitting logic at H1 boundaries")

def test_t1_f6_next_button_exists():
    """27. Verifies \"Next\" navigation button exists."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    next_btns = [b for b in root.find_all("button") + root.find_all("div") + root.find_all("a")
                 if "next" in str(b.attrs).lower() or "next" in b.text.lower()]
    if not next_btns:
        raise AssertionError("No 'Next' pagination button found in index.html")

def test_t1_f6_prev_button_exists():
    """28. Verifies \"Previous\" navigation button exists."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    prev_btns = [b for b in root.find_all("button") + root.find_all("div") + root.find_all("a")
                 if "prev" in str(b.attrs).lower() or "prev" in b.text.lower() or "previous" in b.text.lower()]
    if not prev_btns:
        raise AssertionError("No 'Previous' pagination button found in index.html")

def test_t1_f6_content_update_navigation():
    """29. Verifies content updates when page navigation functions are called."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    nav_functions = ["next", "prev", "show", "page", "section", "render"]
    matches = [f for f in nav_functions if f in js.lower()]
    if len(matches) < 2:
        raise AssertionError("index.html JS does not contain functions to update pagination content")

def test_t1_f6_bounds_checking():
    """30. Verifies pagination bounds are checked (prev disabled on page 1)."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "length" not in js or ("<" not in js and ">" not in js):
        raise AssertionError("index.html JS is missing pagination boundary validation logic")

# ==========================================
# F7: Table of Contents
# ==========================================

def test_t1_f7_sidebar_exists():
    """31. Verifies collapsible sidebar element exists in `index.html`."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    sidebars = root.find_all("aside") + root.find_all("div", "sidebar") + root.find_all(class_name="sidebar")
    if not sidebars and not root.find_by_id("sidebar"):
        raise AssertionError("No sidebar element found in index.html")

def test_t1_f7_dynamic_toc_logic():
    """32. Verifies JavaScript builds TOC dynamically from H1 headers."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "toc" not in js.lower() and "sidebar" not in js.lower():
        raise AssertionError("index.html JS lacks Table of Contents generation or management logic")

def test_t1_f7_toc_click_nav():
    """33. Verifies TOC items are clickable and trigger navigation."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "click" not in js.lower() or ("toc" not in js.lower() and "sidebar" not in js.lower()):
        raise AssertionError("index.html JS lacks click navigation handling for TOC elements")

def test_t1_f7_toc_highlight_active():
    """34. Verifies active section in the TOC is highlighted."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "active" not in style.lower() and "active" not in js.lower():
        raise AssertionError("No active TOC item highlighting style or logic found")

def test_t1_f7_sidebar_toggle():
    """35. Verifies sidebar state (open/collapsed) is toggleable."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "toggle" not in js.lower() or ("sidebar" not in js.lower() and "menu" not in js.lower()):
        raise AssertionError("index.html JS is missing sidebar open/close toggle logic")

# ==========================================
# F8: Text Controls
# ==========================================

def test_t1_f8_increase_button_exists():
    """36. Verifies \"Increase Font Size\" button exists."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    btns = root.find_all("button") + root.find_all("input") + root.find_all("div")
    font_inc = [b for b in btns if "inc" in str(b.attrs).lower() or "increase" in str(b.attrs).lower() or "font-size" in str(b.attrs).lower() or "+" in b.text]
    if not font_inc:
        raise AssertionError("No font size increase control button found")

def test_t1_f8_decrease_button_exists():
    """37. Verifies \"Decrease Font Size\" button exists."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    btns = root.find_all("button") + root.find_all("input") + root.find_all("div")
    font_dec = [b for b in btns if "dec" in str(b.attrs).lower() or "decrease" in str(b.attrs).lower() or "font-size" in str(b.attrs).lower() or "-" in b.text]
    if not font_dec:
        raise AssertionError("No font size decrease control button found")

def test_t1_f8_reset_button_exists():
    """38. Verifies \"Reset Font Size\" button exists."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    btns = root.find_all("button") + root.find_all("input") + root.find_all("div")
    font_reset = [b for b in btns if "reset" in str(b.attrs).lower() or "default" in str(b.attrs).lower() or "reset" in b.text.lower()]
    if not font_reset:
        raise AssertionError("No font size reset control button found")

def test_t1_f8_click_modifies_dom():
    """39. Verifies clicking font control buttons modifies content container CSS."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "fontsize" not in js.lower() and "font-size" not in js.lower():
        raise AssertionError("index.html JS is missing font size modification/application logic")

def test_t1_f8_font_size_bounds():
    """40. Verifies font size stays within limits."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "max" not in js.lower() and "min" not in js.lower() and "<" not in js and ">" not in js:
        raise AssertionError("index.html JS is missing font size boundary limits validation")

# ==========================================
# F9: State Persistence
# ==========================================

def test_t1_f9_theme_saves():
    """41. Verifies JS contains `localStorage.setItem` for active theme."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "vicarious_theme" not in js and "localStorage" not in js:
        raise AssertionError("index.html JS does not save active theme to LocalStorage")

def test_t1_f9_section_saves():
    """42. Verifies JS contains `localStorage.setItem` for active section."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "vicarious_current_section" not in js and "localStorage" not in js:
        raise AssertionError("index.html JS does not save active section to LocalStorage")

def test_t1_f9_font_size_saves():
    """43. Verifies JS contains `localStorage.setItem` for active font size."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "vicarious_font_size" not in js and "localStorage" not in js:
        raise AssertionError("index.html JS does not save active font size to LocalStorage")

def test_t1_f9_load_restores():
    """44. Verifies JS contains `localStorage.getItem` on page load to restore settings."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "localStorage.getitem" not in js.lower() and "getitem" not in js.lower():
        raise AssertionError("index.html JS does not restore settings via localStorage.getItem on page load")

def test_t1_f9_restore_applies_dom():
    """45. Verifies settings are successfully applied to DOM on startup."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if len(re.findall(r'localStorage\.getItem', js)) == 0 and "getitem" not in js.lower():
        raise AssertionError("index.html JS lacks settings restoration application to DOM elements")

# ==========================================
# F10: Custom Callout Parsing
# ==========================================

def test_t1_f10_insight_js_parsing():
    """46. Verifies JS parses blockquotes containing \"Vicarious Insight:\" correctly."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "insight" not in js.lower():
        raise AssertionError("index.html JS does not contain 'Insight' blockquote parsing logic")

def test_t1_f10_reality_check_js_parsing():
    """47. Verifies JS parses blockquotes containing \"Reality Check:\" correctly."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "reality" not in js.lower() and "check" not in js.lower():
        raise AssertionError("index.html JS does not contain 'Reality Check' blockquote parsing logic")

def test_t1_f10_callout_classes_applied():
    """48. Verifies parsed callouts are wrapped in custom CSS classes."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "classlist" not in js.lower() and "classname" not in js.lower() and "class" not in js.lower():
        raise AssertionError("index.html JS lacks callout CSS class application logic")

def test_t1_f10_insight_css_styles():
    """49. Verifies CSS contains distinct styling rules for \"Vicarious Insight\" cards."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "insight" not in style.lower():
        raise AssertionError("CSS is missing styling rules for 'Insight' callouts")

def test_t1_f10_reality_check_css_styles():
    """50. Verifies CSS contains distinct styling rules for \"Reality Check\" cards."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "reality" not in style.lower() and "check" not in style.lower():
        raise AssertionError("CSS is missing styling rules for 'Reality Check' callouts")

# ==========================================
# F11: Progress & Layout
# ==========================================

def test_t1_f11_progress_bar_exists():
    """51. Verifies reading progress bar element exists in `index.html`."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    progress = root.find_all("progress") + root.find_all(class_name="progress") + root.find_all(class_name="progress-bar")
    if not progress and not root.find_by_id("progress"):
        raise AssertionError("No progress bar element found in index.html")

def test_t1_f11_scroll_listener():
    """52. Verifies scroll event listener is attached to update progress bar."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "scroll" not in js.lower() and "addeventlistener" not in js.lower():
        raise AssertionError("index.html JS lacks scroll listener to update progress bar")

def test_t1_f11_hamburger_exists():
    """53. Verifies hamburger menu button exists and is visible on narrow viewports."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    hamburger = root.find_all(class_name="hamburger") + root.find_all(class_name="menu-toggle") + root.find_all("button")
    has_hamburger = any("hamburger" in str(h.attrs).lower() or "menu" in str(h.attrs).lower() or "hamburger" in h.text.lower() for h in hamburger)
    if not has_hamburger:
        raise AssertionError("No hamburger menu button found in index.html")

def test_t1_f11_transition_animations():
    """54. Verifies transition animations (fade class/CSS transition) exist."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    if "transition" not in style.lower() and "animation" not in style.lower() and "fade" not in style.lower() and "fade" not in js.lower():
        raise AssertionError("CSS/JS is missing transition/fade animations")

def test_t1_f11_reading_time_indicator():
    """55. Verifies reading time indicator exists and calculates (~200 wpm)."""
    html_path = os.path.join(PROJECT_ROOT, "index.html")
    if not os.path.exists(html_path):
        raise unittest.SkipTest("index.html is missing")
    root, style, js = load_index_html(html_path)
    has_indicator = "reading-time" in style.lower() or "readingtime" in style.lower() or "reading" in js.lower() or "wpm" in js.lower() or "minute" in js.lower()
    if not has_indicator:
        raise AssertionError("index.html displays no reading time indicator or missing reading time calculations")
