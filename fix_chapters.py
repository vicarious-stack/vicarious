import os
import re

base_dir = r"C:\Users\Dell\.gemini\antigravity\scratch\vicarious_repo"

def fix_file(filename):
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        return
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 1. Remove "---" right below "# Chapter ..." header
    # Let's split into lines
    lines = content.split('\n')
    new_lines = []
    skip_next_hr = False
    
    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            new_lines.append(line)
            # Check if subsequent lines contain "---" before any other text
            # We will skip the first "---" we see in the next 3 lines
            skip_next_hr = True
            continue
            
        if skip_next_hr and line.strip() == '---':
            skip_next_hr = False
            continue
            
        if line.strip() != '':
            skip_next_hr = False
            
        new_lines.append(line)
        
    content = '\n'.join(new_lines)
    
    # 2. Ensure "Digital Ledger" string is present above the JSON block
    if "digital ledger" not in content.lower():
        # Find the json block
        match = re.search(r'```json', content)
        if match:
            idx = match.start()
            content = content[:idx] + "\n### Digital Ledger\n\n" + content[idx:]
            
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Fixed {filename}")

def main():
    for i in range(1, 13):
        fix_file(f"chapter_{i:02d}.md")
        
if __name__ == "__main__":
    main()
