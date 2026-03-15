#!/usr/bin/env python3
"""
Final comprehensive fix for all 25 failing prospect messages.
"""

import re

# Final fixes
FINAL_FIXES = {
    # Prospect 8: Fix awkward multiplier to reduction phrasing
    8: [
        ("If cutting by 80% regression", "If cutting regression time by 80%"),
    ],
    
    # Prospect 17: Fix corrupted text "coverageto-healing"
    17: [
        ("focus on new coverageto-healing, which freed their team from constant script repairs",
         "focus on new coverage"),
    ],
    
    # Prospect 39: Fix duplicate "on new product features" and cleanup
    39: [
        ("focus on new compliance features on new product features instead of firefighting",
         "focus on new compliance features"),
    ],
    
    # Prospect 45: Fix "cover new provider integrations grew across new providers"
    45: [
        ("freeing their team to cover new provider integrations grew across new providers",
         "freeing their team to cover new provider integrations"),
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
    """Apply all final fixes to the content."""
    changes = []
    
    for prospect_id in sorted(FINAL_FIXES.keys()):
        fix_patterns = FINAL_FIXES[prospect_id]
        
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
                print(f"Warning: Pattern not found in prospect {prospect_id}")
        
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
    
    print("Applying final fixes...")
    content, changes = apply_fixes(content)
    
    print("Writing updated HTML file...")
    write_file(filepath, content)
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY OF FINAL FIXES")
    print("="*80)
    
    if changes:
        for i, change in enumerate(changes, 1):
            print(f"\n{i}. Prospect #{change['id']}")
            print(f"   OLD: {change['old']}...")
            print(f"   NEW: {change['new']}...")
    else:
        print("No changes made")
    
    print(f"\nTotal final fixes: {len(changes)}")
    print("\nFile updated successfully!")

if __name__ == "__main__":
    main()
