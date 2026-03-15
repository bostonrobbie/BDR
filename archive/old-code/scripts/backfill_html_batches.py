#!/usr/bin/env python3
"""
Backfill the SQLite database from HTML batch tracker files.

Handles two HTML formats:
  Format A (JS array): Batches 1, 3 — data in `const prospects = [...]`
  Format B (HTML cards): Batches 5A, 5B, 6 — data in `<div class="prospect-card">`

Also links batch_prospects join table so batches connect to contacts.

Run: python scripts/backfill_html_batches.py
"""
import json
import os
import re
import sys
import html
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.db.models import gen_id

DB_PATH = os.environ.get("OCC_DB_PATH", str(ROOT / "outreach.db"))

# Batch file mapping
BATCH_FILES = {
    "batch_1": ROOT / "outreach-sent-feb13-batch1-v2.html",
    "batch_3": ROOT / "outreach-sent-feb26-batch3.html",
    "batch_5a": ROOT / "outreach-sent-feb27-batch5a.html",
    "batch_5b": ROOT / "outreach-sent-feb27-batch5b.html",
    "batch_6": ROOT / "outreach-batch6-unsent.html",
}

BATCH_NUMBERS = {
    "batch_1": 1,
    "batch_3": 3,
    "batch_5a": 5,
    "batch_5b": 5,
    "batch_6": 6,
}


def get_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=30000")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def extract_top_level_objects(array_text):
    """Extract top-level { ... } objects from a JS array string, handling nesting."""
    objects = []
    i = 0
    while i < len(array_text):
        if array_text[i] == '{':
            depth = 0
            in_str = False
            str_char = None
            start = i
            for j in range(i, len(array_text)):
                c = array_text[j]
                if in_str:
                    if c == '\\' and j + 1 < len(array_text):
                        j += 1  # skip escaped char (note: for loop still increments)
                        continue
                    if c == str_char:
                        in_str = False
                else:
                    if c in ('"', "'", '`'):
                        in_str = True
                        str_char = c
                    elif c == '{':
                        depth += 1
                    elif c == '}':
                        depth -= 1
                        if depth == 0:
                            objects.append(array_text[start:j + 1])
                            i = j + 1
                            break
            else:
                break
        else:
            i += 1
    return objects


def parse_js_array_file(filepath):
    """Parse HTML files with `const prospects = [...]` JS arrays (Batch 1, 3)."""
    text = filepath.read_text(encoding="utf-8")

    # Extract the JS array
    match = re.search(r'const\s+prospects\s*=\s*\[', text)
    if not match:
        return []

    start = match.start()
    # Find the matching closing bracket
    bracket_count = 0
    in_string = False
    string_char = None
    i = text.index('[', start)

    for j in range(i, len(text)):
        c = text[j]
        if in_string:
            if c == '\\':
                continue
            if c == string_char:
                in_string = False
        else:
            if c in ('"', "'", '`'):
                in_string = True
                string_char = c
            elif c == '[':
                bracket_count += 1
            elif c == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    array_text = text[i:j + 1]
                    break
    else:
        return []

    # Extract top-level objects from the array using bracket matching
    prospects = []
    top_objects = extract_top_level_objects(array_text)

    for obj_text in top_objects:
        prospect = {}

        # Extract simple key-value pairs
        for key in ['name', 'title', 'company', 'location', 'vertical', 'persona',
                     'abGroup', 'status', 'replyTag', 'email', 'linkedinUrl',
                     'profileUrl', 'proof', 'apolloId', 'messagingStatus',
                     'dateSent', 'sendChannel']:
            # Try single-quoted values first, then double-quoted
            val_match = re.search(rf"{key}\s*:\s*'((?:[^'\\]|\\.)*)'", obj_text)
            if not val_match:
                val_match = re.search(rf'{key}\s*:\s*"((?:[^"\\]|\\.)*)"', obj_text)
            if val_match:
                prospect[key] = html.unescape(val_match.group(1).replace("\\'", "'").replace('\\"', '"'))

        # Extract numeric values
        for key in ['id', 'priority', 'personalizationScore', 'wordCount']:
            val_match = re.search(rf'{key}\s*:\s*(\d+)', obj_text)
            if val_match:
                prospect[key] = int(val_match.group(1))

        # Extract boolean values
        for key in ['buyerIntent']:
            val_match = re.search(rf'{key}\s*:\s*(true|false)', obj_text)
            if val_match:
                prospect[key] = val_match.group(1) == 'true'

        # Extract subject/body for Touch 1
        for key in ['subject', 'body']:
            val_match = re.search(rf"(?<!\w){key}\s*:\s*'((?:[^'\\]|\\.)*)'", obj_text, re.DOTALL)
            if not val_match:
                val_match = re.search(rf'(?<!\w){key}\s*:\s*"((?:[^"\\]|\\.)*)"', obj_text, re.DOTALL)
            if not val_match:
                val_match = re.search(rf'(?<!\w){key}\s*:\s*`((?:[^`\\]|\\.)*)`', obj_text, re.DOTALL)
            if val_match:
                prospect[key] = html.unescape(val_match.group(1).replace("\\'", "'"))

        if prospect.get('name'):
            prospects.append(prospect)

    return prospects


def parse_html_card_file(filepath):
    """Parse HTML files with prospect-card divs (Batch 5A, 5B, 6)."""
    text = filepath.read_text(encoding="utf-8")
    prospects = []

    # Find all prospect-card divs
    card_starts = [m.start() for m in re.finditer(r'<div\s+class="prospect-card"', text)]

    for idx, card_start in enumerate(card_starts):
        # Find the end of this card (next card start or end of file)
        card_end = card_starts[idx + 1] if idx + 1 < len(card_starts) else len(text)
        card_html = text[card_start:card_end]

        prospect = {}

        # Extract data attributes
        priority_match = re.search(r'data-priority="(\d+)"', card_html)
        if priority_match:
            prospect['priority'] = int(priority_match.group(1))

        ab_match = re.search(r'data-ab="([^"]*)"', card_html)
        if ab_match:
            prospect['abGroup'] = ab_match.group(1).upper()

        status_match = re.search(r'data-status="([^"]*)"', card_html)
        if status_match:
            prospect['status'] = status_match.group(1)

        # Format B1: Batch 5A/5B style — prospect-name/prospect-title classes
        name_match = re.search(r'class="prospect-name">([^<]+)<', card_html)
        if name_match:
            prospect['name'] = html.unescape(name_match.group(1).strip())

        title_match = re.search(r'class="prospect-title">([^<]+)<', card_html)
        if title_match:
            full_title = html.unescape(title_match.group(1).strip())
            if ' @ ' in full_title:
                prospect['title'], prospect['company'] = full_title.rsplit(' @ ', 1)
            else:
                prospect['title'] = full_title

        # Format B2: Batch 6 style — <h3> for name, inline div for title
        if not prospect.get('name'):
            h3_match = re.search(r'<h3[^>]*>([^<]+)', card_html)
            if h3_match:
                prospect['name'] = html.unescape(h3_match.group(1).strip())

            # Title in a color:#4b5563 div
            title6_match = re.search(r'color:#4b5563[^>]*>([^<]+)', card_html)
            if title6_match:
                full_title = html.unescape(title6_match.group(1).strip())
                if ' @ ' in full_title:
                    prospect['title'], prospect['company'] = full_title.rsplit(' @ ', 1)
                else:
                    prospect['title'] = full_title

        # Extract vertical from tag or text
        vert_match = re.search(r'class="tag tag-vertical">([^<]+)<', card_html)
        if vert_match:
            prospect['vertical'] = html.unescape(vert_match.group(1).strip())
        else:
            # Batch 6: vertical in the subtitle line
            vert6_match = re.search(r'color:#6b7280[^>]*>([^<|]+)\|', card_html)
            if vert6_match:
                prospect['vertical'] = html.unescape(vert6_match.group(1).strip())

        # Extract persona from tag
        persona_match = re.search(r'class="tag tag-persona">([^<]+)<', card_html)
        if persona_match:
            prospect['persona'] = html.unescape(persona_match.group(1).strip()).lower()

        # Extract LinkedIn URL
        linkedin_match = re.search(r'href="(https?://[^"]*linkedin[^"]*)"', card_html)
        if linkedin_match:
            prospect['linkedinUrl'] = linkedin_match.group(1)

        # Extract email
        email_match = re.search(r'(?:Email:\s*|Email:</strong>\s*)([^\s<]+@[^\s<]+)', card_html)
        if email_match:
            email = email_match.group(1).strip()
            if email != "No":
                prospect['email'] = email

        # Extract personalization score
        pscore_match = re.search(r'Personalization:\s*(\d+)/3', card_html)
        if not pscore_match:
            pscore_match = re.search(r'P-Score:</strong>\s*(\d+)/3', card_html)
        if pscore_match:
            prospect['personalizationScore'] = int(pscore_match.group(1))

        # Extract MQS score
        mqs_match = re.search(r'MQS:\s*(\d+)/12', card_html)
        if mqs_match:
            prospect['mqs'] = int(mqs_match.group(1))

        # Check for buyer intent
        if 'BUYER INTENT' in card_html or 'buyer-intent' in card_html.lower():
            prospect['buyerIntent'] = True

        # Extract Apollo ID
        apollo_match = re.search(r'apollo\.io/#/contacts/([a-f0-9]+)', card_html)
        if apollo_match:
            prospect['apolloId'] = apollo_match.group(1)

        if prospect.get('name'):
            prospects.append(prospect)

    return prospects


def import_prospects(conn, batch_key, prospects, batch_id):
    """Import parsed prospects into the DB and link to batch."""
    now = datetime.utcnow().isoformat()
    imported = 0

    for prospect in prospects:
        name = prospect.get('name', '')
        if not name:
            continue

        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        # Check if already exists
        existing = conn.execute(
            "SELECT id FROM contacts WHERE first_name=? AND last_name=?",
            (first_name, last_name)
        ).fetchone()

        if existing:
            contact_id = existing[0]
        else:
            company = prospect.get('company', '')

            # Create or find account
            account_id = None
            if company:
                acc_row = conn.execute(
                    "SELECT id FROM accounts WHERE name=?", (company,)
                ).fetchone()
                if acc_row:
                    account_id = acc_row[0]
                else:
                    account_id = gen_id("acc")
                    conn.execute("""
                        INSERT INTO accounts (id, name, industry, created_at, updated_at)
                        VALUES (?,?,?,?,?)
                    """, (account_id, company, prospect.get('vertical', ''), now, now))

            # Create contact
            contact_id = gen_id("con")
            linkedin_url = prospect.get('linkedinUrl', prospect.get('profileUrl', ''))

            conn.execute("""
                INSERT INTO contacts (id, account_id, first_name, last_name, title,
                    persona_type, email, linkedin_url, priority_score,
                    personalization_score, status, source, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                contact_id, account_id, first_name, last_name,
                prospect.get('title', ''),
                prospect.get('persona', ''),
                prospect.get('email', ''),
                linkedin_url if linkedin_url else None,
                prospect.get('priority', 3),
                prospect.get('personalizationScore'),
                prospect.get('status', 'active'),
                f"{batch_key}_backfill",
                now, now
            ))
            imported += 1

        # Link to batch via batch_prospects
        existing_link = conn.execute(
            "SELECT id FROM batch_prospects WHERE batch_id=? AND contact_id=?",
            (batch_id, contact_id)
        ).fetchone()

        if not existing_link:
            bp_id = gen_id("bp")
            conn.execute("""
                INSERT INTO batch_prospects (id, batch_id, contact_id, ab_group, sequence_status)
                VALUES (?,?,?,?,?)
            """, (
                bp_id, batch_id, contact_id,
                prospect.get('abGroup', ''),
                'sent' if 'sent' in str(prospect.get('status', '')).lower() else 'not_started'
            ))

    return imported


def link_batch7_prospects(conn):
    """Link existing batch7 contacts to their batch via batch_prospects."""
    batch7 = conn.execute(
        "SELECT id FROM batches WHERE batch_number=7"
    ).fetchone()
    if not batch7:
        return 0

    batch_id = batch7[0]
    contacts = conn.execute(
        "SELECT id FROM contacts WHERE source='batch7_backfill'"
    ).fetchall()

    linked = 0
    for contact in contacts:
        contact_id = contact[0]
        existing = conn.execute(
            "SELECT id FROM batch_prospects WHERE batch_id=? AND contact_id=?",
            (batch_id, contact_id)
        ).fetchone()
        if not existing:
            bp_id = gen_id("bp")
            conn.execute("""
                INSERT INTO batch_prospects (id, batch_id, contact_id, sequence_status)
                VALUES (?,?,?,?)
            """, (bp_id, batch_id, contact_id, 'sent'))
            linked += 1

    return linked


def main():
    print("=== HTML Batch Backfill ===\n")

    conn = get_db()

    # Show current state
    for table in ['accounts', 'contacts', 'batches', 'batch_prospects']:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count}")

    total_imported = 0

    for batch_key, filepath in BATCH_FILES.items():
        if not filepath.exists():
            print(f"\n  Skipping {batch_key}: file not found ({filepath.name})")
            continue

        print(f"\n--- {batch_key} ({filepath.name}) ---")

        # Determine parser
        batch_num = BATCH_NUMBERS[batch_key]
        if batch_key in ("batch_1", "batch_3"):
            prospects = parse_js_array_file(filepath)
            print(f"  Parsed {len(prospects)} prospects (JS array format)")
        else:
            prospects = parse_html_card_file(filepath)
            print(f"  Parsed {len(prospects)} prospects (HTML card format)")

        # Find or create batch record
        batch_row = conn.execute(
            "SELECT id FROM batches WHERE batch_number=?", (batch_num,)
        ).fetchone()

        if batch_row:
            batch_id = batch_row[0]
        else:
            batch_id = gen_id("bat")
            now = datetime.utcnow().isoformat()
            conn.execute("""
                INSERT INTO batches (id, batch_number, prospect_count, status,
                    html_file_path, created_at)
                VALUES (?,?,?,?,?,?)
            """, (batch_id, batch_num, len(prospects), 'complete',
                  str(filepath), now))
            print(f"  Created batch record: batch_number={batch_num}")

        # Import prospects and link to batch
        imported = import_prospects(conn, batch_key, prospects, batch_id)
        total_imported += imported
        print(f"  Imported {imported} new contacts, linked all to batch")

    # Link batch7 contacts
    print("\n--- Linking batch7 contacts ---")
    linked = link_batch7_prospects(conn)
    print(f"  Linked {linked} batch7 contacts to batch record")

    conn.commit()

    # Final stats
    print("\n=== Final Database Stats ===")
    for table in ['accounts', 'contacts', 'batches', 'batch_prospects',
                   'message_drafts', 'touchpoints', 'replies']:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count}")

    # Show batch-to-contact links
    print("\n=== Batch-Contact Links ===")
    rows = conn.execute("""
        SELECT b.batch_number, COUNT(bp.id) as contacts
        FROM batches b
        LEFT JOIN batch_prospects bp ON bp.batch_id = b.id
        GROUP BY b.batch_number
        ORDER BY b.batch_number
    """).fetchall()
    for row in rows:
        print(f"  Batch {row[0]}: {row[1]} contacts linked")

    conn.close()
    print(f"\nTotal new contacts imported: {total_imported}")


if __name__ == "__main__":
    main()
