import re
import os

style_path = r"C:\Users\Dell\AppData\Local\Temp" # Wait, the path is:
# C:\Users\Dell\.gemini\antigravity\scratch\vicarious\style_profile.md
# C:\Users\Dell\.gemini\antigravity\scratch\vicarious\master_outline.md
style_path = r"C:\Users\Dell\.gemini\antigravity\scratch\vicarious\style_profile.md"
outline_path = r"C:\Users\Dell\.gemini\antigravity\scratch\vicarious\master_outline.md"

def count_words(text):
    # Split by whitespace to match standard word count
    words = text.split()
    return len(words)

def analyze_file(path, name):
    if not os.path.exists(path):
        print(f"File {name} NOT FOUND at {path}")
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    w_count = count_words(content)
    print(f"File: {name}")
    print(f"Path: {path}")
    print(f"Word count: {w_count}")
    print(f"Characters: {len(content)}")
    print("-" * 40)

analyze_file(style_path, "style_profile.md")
analyze_file(outline_path, "master_outline.md")
