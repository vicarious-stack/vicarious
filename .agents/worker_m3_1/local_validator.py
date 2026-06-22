import os
import re
import json

ROOT_DIR = r"C:\Users\Dell\.gemini\antigravity\scratch\vicarious"
BANNED_PHRASES = [
    "delve into", "testament to", "tapestry of", "beacon of", "it is important to note",
    "in conclusion", "not only... but also", "furthermore", "moreover", "crucial role",
    "multifaceted", "in today's fast-paced world", "unravel the", "in the realm of",
    "game changer", "paradigm shift", "pinnacle of", "embarks on a journey",
    "heart-pounding", "breathtaking", "shrouded in mystery", "meticulously",
    "unbeknownst to", "beacon of hope", "evolving landscape", "double-edged sword",
    "catalyst for change", "pave the way", "only time will tell", "in a world where",
    "stark reminder", "boundless", "echoes of the past", "treasure trove",
    "intricate dance", "captivating", "nestled in", "bustling hub",
    "seamlessly integrated", "veritable", "unwavering", "deep-seated",
    "shadows danced", "whispers of", "at the end of the day", "let's explore",
    "deep dive", "pioneer", "groundbreaking", "transformative",
    "underscores the importance", "myriad of", "couldn't help but",
    "in that moment", "a sense of", "something inside him shifted",
    "with a heavy heart", "took a deep breath", "heart skipped a beat",
    "cold shiver down his spine"
]

def check_banned_phrases(text, filename):
    errors = []
    # Check simple phrases
    for phrase in BANNED_PHRASES:
        if phrase == "not only... but also":
            # Check for pattern "not only ... but also"
            pattern = re.compile(r"not\s+only\b.*?\bbut\s+also\b", re.IGNORECASE | re.DOTALL)
            if pattern.search(text):
                errors.append(f"Contains banned phrase pattern: '{phrase}'")
        else:
            if phrase.lower() in text.lower():
                # Find occurrences
                matches = [m.start() for m in re.finditer(re.escape(phrase.lower()), text.lower())]
                for idx in matches:
                    snippet = text[max(0, idx - 40):min(len(text), idx + len(phrase) + 40)].replace("\n", " ")
                    errors.append(f"Contains banned phrase: '{phrase}' around: '... {snippet} ...'")
    return errors

def validate():
    files = {
        "prologue.md": {"min_words": 2500, "ledger": False, "diagrams": 0, "callouts": []},
        "chapter_01.md": {"min_words": 3500, "ledger": True, "diagrams": 0, "callouts": []},
        "chapter_02.md": {"min_words": 3500, "ledger": True, "diagrams": 0, "callouts": []},
        "interlude_01.md": {
            "min_words": 4000,
            "ledger": False,
            "diagrams": 2,
            "callouts": [
                "VICARIOUS INSIGHT: THE SLOT MACHINE IN THE POCKET",
                "REALITY CHECK: THE DOPAMINE MYTH"
            ]
        }
    }
    
    print("--- STARTING VALIDATION ---")
    all_ok = True
    
    for filename, spec in files.items():
        path = os.path.join(ROOT_DIR, filename)
        if not os.path.exists(path):
            print(f"FAIL: {filename} does not exist.")
            all_ok = False
            continue
            
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        words = content.split()
        word_count = len(words)
        print(f"File: {filename} | Word Count: {word_count} (Target: >= {spec['min_words']})")
        
        # Word count check
        if word_count < spec["min_words"]:
            print(f"  FAIL: Word count {word_count} is less than target {spec['min_words']}")
            all_ok = False
        else:
            print(f"  PASS: Word count meets target")
            
        # Header check (starts with #)
        if not content.strip().startswith("#"):
            print("  FAIL: Does not start with H1 header (#)")
            all_ok = False
            
        # Banned phrases check
        bp_errors = check_banned_phrases(content, filename)
        if bp_errors:
            print(f"  FAIL: Found {len(bp_errors)} banned phrases:")
            for err in bp_errors:
                print(f"    - {err}")
            all_ok = False
        else:
            print("  PASS: No banned phrases found")
            
        # Ledger check
        if spec["ledger"]:
            # Find json blocks
            json_blocks = re.findall(r"```json\n(.*?)\n```", content, re.DOTALL)
            print(f"  Found {len(json_blocks)} JSON block(s)")
            if len(json_blocks) != 1:
                print(f"  FAIL: Expected exactly 1 JSON block, found {len(json_blocks)}")
                all_ok = False
            else:
                try:
                    data = json.loads(json_blocks[0])
                    print(f"    Parsed JSON successfully: {list(data.keys())}")
                    if "ledger_entry" not in data:
                        print("    FAIL: Missing 'ledger_entry' key in JSON")
                        all_ok = False
                except Exception as e:
                    print(f"    FAIL: Invalid JSON block: {e}")
                    all_ok = False
                    
        # Diagrams check
        if spec["diagrams"] > 0:
            # Find fenced code blocks that are NOT json (diagrams usually have no language tag or a generic one)
            code_blocks = re.findall(r"```(\w*)\n(.*?)\n```", content, re.DOTALL)
            diagram_blocks = [cb for cb in code_blocks if cb[0] != "json"]
            print(f"  Found {len(diagram_blocks)} diagram code blocks (expected {spec['diagrams']})")
            if len(diagram_blocks) != spec["diagrams"]:
                print(f"  FAIL: Expected exactly {spec['diagrams']} diagram code blocks, found {len(diagram_blocks)}")
                all_ok = False
                
        # Callouts check
        if spec["callouts"]:
            bq_lines = re.findall(r"^>\s?(.*)$", content, re.MULTILINE)
            bq_text = "\n".join(bq_lines)
            print(f"  Found blockquotes. Checking callouts...")
            for callout in spec["callouts"]:
                if callout not in bq_text:
                    print(f"  FAIL: Missing callout box with header: '{callout}'")
                    all_ok = False
                else:
                    print(f"    Found callout header: '{callout}'")
                    
        # Character names check
        names = ["Kiran", "Priya", "Venky Sir", "Adi", "Dr. Meera", "Rohan"]
        # Look for spelling variations or lowercase versions that might be wrong
        for name in names:
            # Verify if lowercase version appears but uppercase is not match (or simple match)
            # Make sure we don't use 'Meera' without 'Dr.' or check common misspellings if any
            pass
            
    print("--- VALIDATION COMPLETE. RESULT:", "PASS" if all_ok else "FAIL", "---")

if __name__ == "__main__":
    validate()
