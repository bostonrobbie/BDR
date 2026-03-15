#!/usr/bin/env python3
"""
One-time script to split CLAUDE.md (136KB monolith) into modular files.
Creates:
  .claude/rules/outbound-intelligence.md  - Data-driven rules (HC, SP, MQS, QA Gate, patterns)
  .claude/rules/message-structure.md      - C2 structure, writing rules, proof points, research
  .claude/rules/safety.md                 - Draft safety, LinkedIn compliance, incident log
  .claude/rules/sops.md                   - All operational SOPs (send, Apollo, warm leads, etc.)
  work/pipeline-state.json                - Live operational state (send log, credits, batches)
  work/dnc-list.json                      - Do Not Contact list
  work/follow-up-schedule.json            - Computed follow-up dates
"""
import os
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = ROOT / "CLAUDE.md"

def read_claude_md():
    return CLAUDE_MD.read_text(encoding="utf-8")

def extract_section(lines, start_marker, end_markers):
    """Extract lines from start_marker to the first end_marker found."""
    capturing = False
    result = []
    for i, line in enumerate(lines):
        if not capturing and start_marker in line:
            capturing = True
        if capturing:
            # Check if we've hit an end marker (but not on the start line)
            if i > 0 and any(em in line for em in end_markers) and start_marker not in line:
                break
            result.append(line)
    return "\n".join(result)

def main():
    content = read_claude_md()
    lines = content.split("\n")

    # Define section boundaries by line numbers (0-indexed)
    # Section: Outbound Intelligence System (lines 644-926)
    outbound_intel = "\n".join(lines[644:927])

    # Section: Outreach SOP (lines 111-642), split out draft safety
    message_structure_part1 = "\n".join(lines[111:240])  # Before draft safety
    draft_safety = "\n".join(lines[240:329])              # Draft safety + incident log
    message_structure_part2 = "\n".join(lines[329:642])   # After draft safety
    message_structure = message_structure_part1 + "\n\n> **Draft Safety Rules:** See `.claude/rules/safety.md` for cadence enforcement, date-gating, and incident log.\n\n" + message_structure_part2

    # Section: LinkedIn Safety (lines 1372-1418)
    linkedin_safety = "\n".join(lines[1372:1419])

    # Section: Safety = draft safety + LinkedIn safety
    safety = draft_safety + "\n\n---\n\n" + linkedin_safety

    # Section: All operational SOPs
    sop_sections = []
    sop_ranges = [
        (929, 1077),   # LinkedIn Sales Navigator Live Send SOP
        (1078, 1098),  # End-to-End Process Map
        (1100, 1135),  # SOP B
        (1136, 1167),  # SOP C
        (1168, 1193),  # SOP Module A1
        (1194, 1231),  # SOP Module A2
        (1232, 1315),  # SOP D
        (1316, 1371),  # Active Warm Leads
        (1420, 1514),  # Apollo Integration (skip LinkedIn safety already extracted)
        (1515, 1646),  # Cycle Logging
        (1647, 1659),  # Salesforce CRM
        (1660, 1687),  # Plugin Customization
        (1688, 1726),  # Warm/Inbound Lead SOP
        (1727, 1748),  # Google Drive KB
        (1747, 1815),  # Key Deliverables Index
        (1816, 1909),  # Intent Pipeline SOP
        (1910, 1982),  # Email SOP
        (2027, 2101),  # Run the Daily
    ]
    for start, end in sop_ranges:
        sop_sections.append("\n".join(lines[start:end]))
    sops = "\n\n---\n\n".join(sop_sections)

    # Write rule files
    rules_dir = ROOT / ".claude" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)

    (rules_dir / "outbound-intelligence.md").write_text(
        "# Outbound Intelligence System (Data-Driven Rules)\n\n"
        "> Loaded by: `/score-message`, `/write-batch`, `/pre-brief`\n"
        "> Source: Analysis of 1,326 LinkedIn conversations (381 replies, 945 no-replies)\n\n"
        + outbound_intel,
        encoding="utf-8"
    )
    print(f"  Created: .claude/rules/outbound-intelligence.md ({len(outbound_intel)} chars)")

    (rules_dir / "message-structure.md").write_text(
        "# Outreach Message Structure & Writing Rules\n\n"
        "> Loaded by: `/write-batch`, `/follow-up`\n"
        "> Defines: C2 message structure, pre-draft steps, proof points, research requirements\n\n"
        + message_structure,
        encoding="utf-8"
    )
    print(f"  Created: .claude/rules/message-structure.md ({len(message_structure)} chars)")

    (rules_dir / "safety.md").write_text(
        "# Safety & Compliance Rules\n\n"
        "> Loaded by: `/follow-up`, `/write-batch`, send sessions\n"
        "> Defines: Draft cadence enforcement, LinkedIn compliance, incident log\n\n"
        + safety,
        encoding="utf-8"
    )
    print(f"  Created: .claude/rules/safety.md ({len(safety)} chars)")

    (rules_dir / "sops.md").write_text(
        "# Operational SOPs\n\n"
        "> Loaded by: specific skills as needed\n"
        "> Contains: LinkedIn send SOP, Apollo integration, warm leads, daily workflow, etc.\n\n"
        + sops,
        encoding="utf-8"
    )
    print(f"  Created: .claude/rules/sops.md ({len(sops)} chars)")

    # Extract live data into JSON files
    work_dir = ROOT / "work"
    work_dir.mkdir(exist_ok=True)

    # Pipeline state (extracted from Master Send Log + Follow-Up Schedule)
    pipeline_state = {
        "_comment": "Live operational state. Updated by skills after each action. Read by session_start.sh.",
        "last_updated": "2026-03-02",
        "inmail_credits_remaining": 24,
        "total_sends_all_time": 148,
        "total_emails_all_time": 15,
        "active_batches": {
            "batch_3": {
                "status": "complete",
                "prospects": 24,
                "touch1_sent_dates": ["2026-02-25", "2026-02-26"],
                "notes": "4 prospects had premature Touch 3 (INC-001)"
            },
            "batch_5a": {
                "status": "complete",
                "prospects": 25,
                "touch1_sent_dates": ["2026-02-27", "2026-02-28"]
            },
            "batch_5b": {
                "status": "complete",
                "prospects": 23,
                "touch1_sent_dates": ["2026-02-27"],
                "notes": "Terene Lee blocked (messaging disabled), Sanjay DNC"
            },
            "batch_6": {
                "status": "complete",
                "prospects": 27,
                "touch1_sent_dates": ["2026-02-28"]
            },
            "batch_7": {
                "status": "complete",
                "prospects": 41,
                "touch1_sent_dates": ["2026-02-28"],
                "notes": "1 NOT FOUND (Jonathan Lavoie)"
            }
        },
        "warm_leads": [
            {
                "name": "Namita Jain",
                "company": "OverDrive",
                "email": "njain@overdrive.com",
                "last_touch": "2026-02-27",
                "channel": "email",
                "status": "awaiting_reply",
                "next_action": "Touch 2 InMail if no reply by Mar 4"
            }
        ],
        "apollo_sequences": {
            "q1_priority_accounts": {
                "id": "69a05801fdd140001d3fc014",
                "active_contacts": 144,
                "current_step": 1
            },
            "q1_website_visitor": {
                "id": "69a1b3564fa5fa001152eb66",
                "active_contacts": 9
            }
        },
        "credit_alert": "CRITICAL - 24 credits for ~113 Touch 2 InMails due this week. Prioritize Hot/Warm only.",
        "unsent_prospects": 0,
        "latest_batch_number": 7
    }

    (work_dir / "pipeline-state.json").write_text(
        json.dumps(pipeline_state, indent=2),
        encoding="utf-8"
    )
    print(f"  Created: work/pipeline-state.json")

    # DNC list
    dnc_list = {
        "_comment": "Do Not Contact list. Check before ANY outreach. Updated by /reply-handle.",
        "last_updated": "2026-03-02",
        "contacts": [
            {
                "name": "Sanjay Singh",
                "company": "ServiceTitan",
                "reason": "Hostile reply to prior outreach (2022 mabl era). Requested no further contact.",
                "date_added": "2026-02-27",
                "permanent": True
            },
            {
                "name": "Lance Silverman",
                "company": "Batch 5B",
                "reason": "Polite decline. Re-engage only after 60+ days with new trigger.",
                "date_added": "2026-03-01",
                "permanent": False,
                "reengagement_eligible": "2026-05-01"
            }
        ]
    }

    (work_dir / "dnc-list.json").write_text(
        json.dumps(dnc_list, indent=2),
        encoding="utf-8"
    )
    print(f"  Created: work/dnc-list.json")

    # Follow-up schedule
    followup_schedule = {
        "_comment": "Computed from Touch 1 send dates. Updated after each send session.",
        "last_updated": "2026-03-02",
        "cadence": {
            "touch2_offset_days": 5,
            "touch3_offset_days": 10,
            "touch2_eligible_offset_days": 4,
            "touch3_eligible_offset_days": 9
        },
        "batches": {
            "batch_3": {
                "prospects": 24,
                "touch1_sent": "2026-02-25/26",
                "touch2_eligible": "2026-03-01/02",
                "touch2_send": "2026-03-02/03",
                "touch3_eligible": "2026-03-06/07",
                "touch3_send": "2026-03-07/08",
                "special_cases": "Irfan, Katie, Rachana, Giang: premature Touch 3 already sent (INC-001). Skip official Touch 3."
            },
            "batch_5b": {
                "prospects": 23,
                "touch1_sent": "2026-02-27",
                "touch2_eligible": "2026-03-03",
                "touch2_send": "2026-03-04",
                "touch3_eligible": "2026-03-08",
                "touch3_send": "2026-03-09"
            },
            "batch_5a": {
                "prospects": 25,
                "touch1_sent": "2026-02-27/28",
                "touch2_eligible": "2026-03-03/04",
                "touch2_send": "2026-03-04/05",
                "touch3_eligible": "2026-03-08/09",
                "touch3_send": "2026-03-09/10"
            },
            "batch_6": {
                "prospects": 27,
                "touch1_sent": "2026-02-28",
                "touch2_eligible": "2026-03-04",
                "touch2_send": "2026-03-05",
                "touch3_eligible": "2026-03-09",
                "touch3_send": "2026-03-10"
            },
            "batch_7": {
                "prospects": 41,
                "touch1_sent": "2026-02-28",
                "touch2_eligible": "2026-03-04",
                "touch2_send": "2026-03-05",
                "touch3_eligible": "2026-03-09",
                "touch3_send": "2026-03-10"
            },
            "buyer_intent": {
                "prospects": 9,
                "touch1_sent": "2026-02-27",
                "touch2_eligible": "2026-03-03",
                "touch2_send": "2026-03-04",
                "touch3_eligible": "2026-03-08",
                "touch3_send": "2026-03-09"
            }
        },
        "week_summary": {
            "2026-03-02_to_03-06": {
                "touch2_inmail_due": 113,
                "touch3_email_due": 0,
                "note": "CRITICAL: 24 credits for 113 Touch 2s. Prioritize Hot/Warm only, email for rest."
            }
        }
    }

    (work_dir / "follow-up-schedule.json").write_text(
        json.dumps(followup_schedule, indent=2),
        encoding="utf-8"
    )
    print(f"  Created: work/follow-up-schedule.json")

    print(f"\nDone! Original CLAUDE.md preserved. Now create the new slim CLAUDE.md manually.")

if __name__ == "__main__":
    main()
