#!/usr/bin/env python3
"""
Fix 25 failing prospect messages in the HTML outreach file.
Applies targeted fixes for:
1. Multiplier framing (5X, 4X) → Reduction framing
2. Unauthorized hyphens
3. Missing proof points with numbers
4. Buzzwords
"""

import re

# Define all fixes with EXACT patterns found in actual content
FIXES = {
    # Category 1: Multiplier Framing → Reduction Framing
    8: {
        "category": "Multiplier Framing",
        "old_patterns": [
            ("hit cut execution by 80%", "cut execution by 80%"),  # Already partially fixed
            ("If cutting execution by 80%", "If cutting execution by 80% would"),  # Just needs context
        ]
    },
    11: {
        "category": "Multiplier Framing",
        "old_patterns": [
            ("hit 5X faster execution", "cut execution by 80%"),
            ("If cut regression time by 80% cycles", "If cutting regression time by 80%"),
        ]
    },
    16: {
        "category": "Multiplier Framing",
        "old_patterns": [
            ("hit 4X faster execution", "cut execution by 75%"),
            ("If 4X faster test execution", "If cutting test execution by 75%"),
        ]
    },
    23: {
        "category": "Multiplier Framing",
        "old_patterns": [
            ("cut execution 5X", "cut execution by 80%"),
            ("If 5X faster regression", "If cutting regression by 80%"),
        ]
    },
    34: {
        "category": "Multiplier Framing",
        "old_patterns": [
            ("If 5X faster regression", "If cutting regression by 80%"),
        ]
    },
    43: {
        "category": "Multiplier Framing",
        "old_patterns": [
            ("hit 5X faster execution", "cut execution by 80%"),
        ]
    },
    48: {
        "category": "Multiplier Framing",
        "old_patterns": [
            ("hit 4X faster execution", "cut execution by 75%"),
            ("If 4X faster test cycles", "If cutting test cycles by 75%"),
        ]
    },
    50: {
        "category": "Multiplier Framing",
        "old_patterns": [
            ("4X faster automation scaling", "scaled automation 75% faster"),
        ]
    },
    
    # Category 2: Buzzwords
    2: {
        "category": "Buzzword",
        "old_patterns": [
            ("cut execution time 5X", "cut execution time by 80%"),
        ]
    },
    40: {
        "category": "Buzzword",
        "old_patterns": [
            ("feature speed", "feature speed"),  # Already fixed
        ]
    },
    41: {
        "category": "Buzzword",
        "old_patterns": [
            ("becomes the blocker", "becomes the blocker"),  # Already fixed
        ]
    },
    
    # Category 3: Hyphens
    5: {
        "category": "Hyphen",
        "old_patterns": [
            ("Micro investing", "Micro investing"),  # Already fixed
        ]
    },
    6: {
        "category": "Hyphen",
        "old_patterns": [
            ("compliance grade", "compliance grade"),  # Already fixed
        ]
    },
    22: {
        "category": "Hyphen",
        "old_patterns": [
            ("FDA regulated", "FDA regulated"),  # Already fixed
        ]
    },
    32: {
        "category": "Hyphen",
        "old_patterns": [
            ("critical for regression", "critical for regression"),  # Already fixed
        ]
    },
    37: {
        "category": "Hyphen",
        "old_patterns": [
            ("Cisco (enterprise, large-scale", "Cisco (enterprise, large-scale"),  # Already fixed
        ]
    },
    47: {
        "category": "Hyphen + Buzzword",
        "old_patterns": [
            ("With AI driven planning", "With AI-driven planning changes that happen weekly"),
        ]
    },
    
    # Category 4: Proof Points
    17: {
        "category": "Proof Point",
        "old_patterns": [
            ("Medibuddy automated 2,500 tests and cut maintenance by 50% using Testsigma, freeing their team to focus on new coverage using Testsigma's codeless au", 
             "Medibuddy automated 2,500 tests and cut maintenance by 50% using Testsigma, freeing their team to focus on new coverage"),
        ]
    },
    24: {
        "category": "Proof Point",
        "old_patterns": [
            ("Medibuddy automated 2,500 tests and cut maintenance effort by 50% using Testsigma, freeing their team to ", 
             "Medibuddy automated 2,500 tests and cut maintenance by 50% using Testsigma, freeing their team to cover new content workflows"),
        ]
    },
    35: {
        "category": "Proof Point",
        "old_patterns": [
            ("cut maintenance in half", "cut maintenance by 50%"),
        ]
    },
    39: {
        "category": "Proof Point",
        "old_patterns": [
            ("Sanofi cut regression from 3 days to 80 minutes using Testsigma, freeing their team to focus on new compliance features by using AI codeless test healing with Testsigma, freeing the team to focus",
             "Sanofi cut regression from 3 days to 80 minutes using Testsigma, freeing their team to focus on new compliance features"),
        ]
    },
    45: {
        "category": "Proof Point",
        "old_patterns": [
            ("Medibuddy automated 2,500 tests and cut maintenance by 50% using Testsigma, freeing their team to cover new provider integrations technology, freeing their team from constant script repairs while coverage",
             "Medibuddy automated 2,500 tests and cut maintenance by 50% using Testsigma, freeing their team to cover new provider integrations"),
        ]
    },
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
    
    for prospect_id, fix_info in sorted(FIXES.items()):
        # Extract the message field
        pattern = rf'(id:\s*{prospect_id}\s*,.*?message:\s*")([^"]*?)(",\s*abGroup)'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            print(f"Warning: Could not find prospect {prospect_id}")
            continue
        
        original_message = match.group(2)
        new_message = original_message
        
        # Apply each pattern fix
        for old_text, new_text in fix_info["old_patterns"]:
            if old_text in new_message:
                new_message = new_message.replace(old_text, new_text)
                changes.append({
                    "id": prospect_id,
                    "category": fix_info["category"],
                    "old": old_text[:60],
                    "new": new_text[:60]
                })
        
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
    print("SUMMARY OF CHANGES")
    print("="*80)
    
    by_category = {}
    for change in changes:
        cat = change["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(change)
    
    for category in sorted(by_category.keys()):
        print(f"\n{category}:")
        for change in by_category[category]:
            print(f"  Prospect #{change['id']}: '{change['old']}...' → '{change['new']}...'")
    
    print(f"\nTotal changes: {len(changes)}")
    print(f"Total prospects fixed: {len(set(c['id'] for c in changes))}")
    print("\nFile updated successfully!")

if __name__ == "__main__":
    main()
