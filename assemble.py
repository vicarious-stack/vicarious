import os
import re

def assemble_book():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(base_dir, "the_vicarious_complete.md")
    
    # Ensure directory of output file exists (F2 corner case check)
    out_dir = os.path.dirname(output_file)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    title_page = """# VICARIOUS
**by Vijay**

---

## Table of Contents

- [Prologue](#prologue)
- [Chapter 1: The Scroll](#chapter-1-the-scroll)
- [Chapter 2: The Glitch](#chapter-2-the-glitch)
- [Interlude I: The Dopamine Machine](#interlude-i-the-dopamine-machine)
- [Chapter 3: The Appointment](#chapter-3-the-appointment)
- [Chapter 4: The Discomfort](#chapter-4-the-discomfort)
- [Interlude II: The Architecture of Self-Deception](#interlude-ii-the-architecture-of-self-deception)
- [Chapter 5: The Craft](#chapter-5-the-craft)
- [Chapter 6: The Algorithm](#chapter-6-the-algorithm)
- [Interlude III: The Science of Mastery](#interlude-iii-the-science-of-mastery)
- [Chapter 7: The Hunger](#chapter-7-the-hunger)
- [Chapter 8: The Professional](#chapter-8-the-professional)
- [Interlude IV: The Biology of Desire](#interlude-iv-the-biology-of-desire)
- [Chapter 9: The System](#chapter-9-the-system)
- [Chapter 10: The Builder](#chapter-10-the-builder)
- [Interlude V: The Invisible Architecture](#interlude-v-the-invisible-architecture)
- [Chapter 11: The Test](#chapter-11-the-test)
- [Chapter 12: The Direct Experience](#chapter-12-the-direct-experience)
- [Interlude VI: The Philosophy of Direct Experience](#interlude-vi-the-philosophy-of-direct-experience)
- [Epilogue: The Mountain Road](#epilogue-the-mountain-road)
- [Appendices: The Systems Manual](#appendices-the-systems-manual)

---
"""

    # Files list in order
    files = [
        "prologue.md",
        "chapter_01.md",
        "chapter_02.md",
        "interlude_01.md",
        "chapter_03.md",
        "chapter_04.md",
        "interlude_02.md",
        "chapter_05.md",
        "chapter_06.md",
        "interlude_03.md",
        "chapter_07.md",
        "chapter_08.md",
        "interlude_04.md",
        "chapter_09.md",
        "chapter_10.md",
        "interlude_05.md",
        "chapter_11.md",
        "chapter_12.md",
        "interlude_06.md",
        "epilogue.md",
        "appendices.md"
    ]

    parts = []
    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            print(f"Error: Required file {filename} does not exist!")
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            # Read-only access to source files
            content = f.read().strip()
            parts.append(content)
            print(f"Read {filename} successfully ({len(content.split())} words).")

    full_text = title_page + "\n\n" + "\n\n---\n\n".join(parts) + "\n"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"Book assembled successfully into {output_file}.")

if __name__ == "__main__":
    assemble_book()
