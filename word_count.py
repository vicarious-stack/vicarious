import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))

thresholds = {
    "prologue.md": 2500,
    "chapter_01.md": 3000,
    "chapter_02.md": 3000,
    "chapter_03.md": 3000,
    "chapter_04.md": 3000,
    "chapter_05.md": 3000,
    "chapter_06.md": 3000,
    "chapter_07.md": 3000,
    "chapter_08.md": 3000,
    "chapter_09.md": 3000,
    "chapter_10.md": 3000,
    "chapter_11.md": 3000,
    "chapter_12.md": 3000,
    "interlude_01.md": 3500,
    "interlude_02.md": 3500,
    "interlude_03.md": 3500,
    "interlude_04.md": 3500,
    "interlude_05.md": 3500,
    "interlude_06.md": 3500,
    "epilogue.md": 2000,
    "appendices.md": 2000
}

def check_word_counts():
    total_words = 0
    all_passed = True
    
    print("=" * 60)
    print("VICARIOUS WORD COUNT CHECK")
    print("=" * 60)
    
    for filename, min_words in thresholds.items():
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            print(f"{filename:25} | MISSING | Threshold: {min_words}")
            all_passed = False
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            word_count = len(content.split())
            total_words += word_count
            
            # Use >= operator to satisfy test_t2_f2_exact_min_words
            if word_count >= min_words:
                status = "PASS"
            else:
                status = "FAIL (Below Minimum)"
                all_passed = False
                
            print(f"{filename:25} | Words: {word_count:5} | Threshold: {min_words:4} | Status: {status}")
            
    print("-" * 60)
    print(f"Total Book Word Count: {total_words}")
    
    # Check total target count of 80,000 words
    if total_words >= 80000:
        total_status = "PASS"
    else:
        total_status = "FAIL (Under 80k target)"
        all_passed = False
        
    print(f"80,000 Words Target:    {total_status}")
    print("=" * 60)
    
    if not all_passed:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    check_word_counts()
