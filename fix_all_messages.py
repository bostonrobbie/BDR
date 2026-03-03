#!/usr/bin/env python3
"""
Fix 25 failing prospect messages in the HTML outreach file.
Comprehensive fixes for all identified issues.
"""

import re

# Define all fixes with EXACT patterns
FIXES = {
    # Prospect 2: Buzzword - cut execution time 5X → cut execution by 80%
    2: [("cut execution time 5X with", "cut execution time by 80% with")],
    
    # Prospect 3: Banking as a service (already fixed)
    3: [],
    
    # Prospect 5: Micro investing (already fixed)
    5: [],
    
    # Prospect 6: compliance grade (already fixed)
    6: [],
    
    # Prospect 8: hit 5X faster execution → cut execution by 80%
    8: [("hit cut execution by 80%", "cut execution by 80%")],
    
    # Prospect 10: 4X faster execution + multi-market hyphen
    10: [
        ("hitting 4X faster execution", "cut execution by 75%"),
        ("If 4X faster test execution", "If cutting test execution by 75%"),
    ],
    
    # Prospect 11: 5X faster execution → cut execution by 80%
    11: [
        ("hit 5X faster execution", "cut execution by 80%"),
        ("If cut regression time by 80% cycles", "If cutting regression by 80%"),
    ],
    
    # Prospect 16: Already fixed in previous run
    16: [],
    
    # Prospect 17: Proof point fix
    17: [("using Testsigma's codeless au", "using Testsigma")],
    
    # Prospect 22: FDA regulated (already fixed)
    22: [],
    
    # Prospect 23: Already fixed in previous run
    23: [],
    
    # Prospect 24: Proof point
    24: [("freeing their team to ", "freeing their team to cover new content workflows")],
    
    # Prospect 32: Already fixed in previous run
    32: [],
    
    # Prospect 33: Low-code platforms issue
    33: [("They cut it in half w", "They cut maintenance by 50% using Testsigma")],
    
    # Prospect 34: Already fixed in previous run
    34: [],
    
    # Prospect 35: Already fixed in previous run
    35: [],
    
    # Prospect 37: Already fixed in previous run
    37: [],
    
    # Prospect 39: Proof point duplication
    39: [("using Testsigma, freeing their team to focus on new compliance features by using AI codeless test healing with Testsigma, freeing the team to focus",
          "using Testsigma, freeing their team to focus on new compliance features")],
    
    # Prospect 40: Already fixed in previous run
    40: [],
    
    # Prospect 41: Already fixed in previous run
    41: [],
    
    # Prospect 43: 5X faster execution
    43: [("hitting 5X faster execution", "cut execution by 80%")],
    
    # Prospect 45: Proof point
    45: [("integrations technology, freeing their team from constant script repairs while coverage",
          "integrations")],
    
    # Prospect 47: AI-driven duplication
    47: [("With AI-driven planning changes that happen weekly changes weekly", 
          "With AI-driven planning changes that happen weekly")],
    
    # Prospect 48: Already fixed in previous run
    48: [],
    
    # Prospect 50: 4X faster automation scaling
    50: [
        ("scaled test automation 4X faster", "scaled test automation by 75%"),
        ("If 4X faster automation scaling", "If scaling automation by 75%"),
    ],
}

def read_file(filepath):
    """Read the HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Write the HTML file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def apply_fixes(content):
    """Apply all fixes to the content."""
    changes = []
    
    for prospect_id in sorted(FIXES.keys()):
        fix_patterns = FIXES[prospect_id]
        if not fix_patterns:
            continue
            
        # Extract the message field
        pattern = rf'(id:\s*{prospect_id}\s*,.*?message:\s*")([^"]*?)(",\s*abGroup)'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            print(f"Warning: Could not find prospect {prospect_id}")
            continue
        
        original_message = match.group(2)
        new_message = original_message
        
        # Apply each pattern fix
        for old_text, new_text in fix_patterns:
            if old_text in new_message:
                new_message = new_message.replace(old_text, new_text)
                changes.append({
                    "id": prospect_id,
                    "old": old_text[:70],
                    "new": new_text[:70]
                })
            else:
                print(f"Warning: Pattern not found in prospect {prospect_id}: '{old_text[:50]}'")
        
        # Replace in the content
        if new_message != original_message:
            old_full = match.group(1) + original_message + match.group(3)
            new_full = match.group(1) + new_message + match.group(3)
            content = content.replace(old_full, new_full)
    
    return content, changes

def main():
    filepath = "/sessions/epic-cool-bell/mnt/Work/prospect-outreach-8-2026-03-02.html"
    
    print("Reading HTML file...")
    content = read_file(filepath)
    
    print("Applying fixes...")
    content, changes = apply_fixes(content)
    
    print("Writing updated HTML file...")
    write_file(filepath, content)
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY OF ADDITIONAL CHANGES")
    print("="*80)
    
    if changes:
        for i, change in enumerate(changes, 1):
            print(f"\n{i}. Prospect #{change['id']}")
            print(f"   Old: {change['old']}...")
            print(f"   New: {change['new']}...")
    else:
        print("No additional changes made")
    
    print(f"\nTotal new changes: {len(changes)}")
    print("\nFile updated successfully!")

if __name__ == "__main__":
    main()
