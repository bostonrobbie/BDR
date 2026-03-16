"""Batch 2 auto-import module for Vercel serverless deployment."""
import os
import json
import uuid
from datetime import datetime


def gen_id(prefix=""):
    short = uuid.uuid4().hex[:12]
    return f"{prefix}_{short}" if prefix else short


def _auto_import_batch2(conn):
    """Auto-import batch 2 run bundle if not already imported."""
    # Check if batch 2 already exists
    existing = conn.execute("SELECT COUNT(*) FROM batches WHERE batch_number=2").fetchone()[0]
    if existing > 0:
        return  # Already imported

    # Find batch 2 bundle file
    bundle_paths = [
        os.path.join(os.path.dirname(__file__), "data", "run-bundle-batch2.json"),
        os.path.join(os.path.dirname(__file__), "..", "public", "data", "run-bundle-batch2.json"),
        "/var/task/api/data/run-bundle-batch2.json",
        "/var/task/public/data/run-bundle-batch2.json",
    ]
    bundle_path = None
    for p in bundle_paths:
        if os.path.exists(p):
            bundle_path = p
            break
    if not bundle_path:
        return  # No batch 2 file

    print(f"Auto-import batch 2: Loading from {bundle_path}")
    conn.execute("PRAGMA foreign_keys=OFF")
    with open(bundle_path) as f:
        bundle = json.load(f)

    prospects = bundle.get("prospects", [])
    if not prospects:
        return

    now = datetime.utcnow().isoformat()

    batch_id = gen_id("batch")
    conn.execute("""INSERT INTO batches (id, batch_number, created_date, prospect_count,
        ab_variable, status, source, created_at)
        VALUES (?,?,?,?,?,?,?,?)""",
        (batch_id, 2, now[:10], len(prospects), "pain_hook", "imported", "run_bundle", now))

    run_id = gen_id("rr")
    conn.execute("""INSERT INTO research_runs (id, name, import_type, prospect_count, status,
        sop_checklist, progress_pct, logs, ab_variable, config, created_at, completed_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (run_id, f"Batch 2 Auto-Import - {now[:10]}", "run_bundle", len(prospects), "completed",
         json.dumps([{"step": "import", "status": "completed", "label": "Batch 2 Auto-Import"}]),
         100, json.dumps([f"Auto-imported batch 2 at {now}"]),
         "pain_hook", "{}", now, now))

    # Batch 2 uses different field names than batch 1
    touch_map_b2 = [
        (1, "inmail", "touch_1_subject", "touch_1_body"),
        (2, "call", None, "touch_2_call"),
        (3, "inmail_followup", None, "touch_3_body"),
        (4, "call", None, "touch_4_call"),
        (5, "email", "touch_5_subject", "touch_5_body"),
        (6, "breakup", None, "touch_6_body"),
    ]

    proof_map = {
        "FinTech": ("cred", "CRED achieved 90% regression automation with 5x faster execution"),
        "FinServ": ("cred", "CRED achieved 90% regression automation with 5x faster execution"),
        "Healthcare": ("medibuddy", "Medibuddy automated 2,500 tests and cut maintenance 50%"),
        "Pharma": ("sanofi", "Sanofi cut regression from 3 days to 80 minutes"),
        "SaaS": ("spendflo", "Spendflo cut manual testing 50% and saw ROI in the first quarter"),
        "Tech": ("fortune100", "A Fortune 100 company achieved 3X productivity increase"),
        "E-Commerce": ("medibuddy", "Medibuddy automated 2,500 tests and cut maintenance 50%"),
        "Energy": ("fortune100", "A Fortune 100 company achieved 3X productivity increase"),
    }

    imported_contacts = 0
    imported_drafts = 0

    for idx, p in enumerate(prospects):
        name = p.get("name", "")
        if not name:
            continue

        first_name = p.get("first_name", name.split(" ", 1)[0])
        parts = name.strip().split(" ", 1)
        last_name = parts[1] if len(parts) > 1 else ""

        company = p.get("company", "")
        title = p.get("title", "")
        vertical = p.get("vertical", "")
        linkedin_url = p.get("linkedin", p.get("linkedin_url", ""))

        persona_type = p.get("persona_type", "qa_leader")
        seniority = p.get("seniority", "director").lower().replace(" ", "_")
        priority = p.get("priority_score", 3)

        # Create or find account
        acc = conn.execute("SELECT id FROM accounts WHERE name=?", (company,)).fetchone()
        if acc:
            account_id = acc[0]
        else:
            account_id = gen_id("acc")
            emp_count = p.get("employee_count")
            emp_band = "enterprise" if emp_count and emp_count > 5000 else "mid_market" if emp_count and emp_count > 200 else "smb"
            conn.execute("""INSERT INTO accounts (id, name, industry, employee_count, employee_band,
                source, created_at) VALUES (?,?,?,?,?,?,?)""",
                (account_id, company, vertical, emp_count, emp_band, "run_bundle", now))

        contact_id = gen_id("con")
        conn.execute("""INSERT INTO contacts (id, account_id, first_name, last_name, title,
            persona_type, seniority_level, linkedin_url, stage, priority_score,
            personalization_score, predicted_objection, objection_response,
            source, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (contact_id, account_id, first_name, last_name, title,
             persona_type, seniority, linkedin_url, "new", priority,
             p.get("personalization_score", 3),
             p.get("predicted_objection", ""), p.get("objection_response", ""),
             "run_bundle", now))
        imported_contacts += 1

        # Research snapshot
        person_detail = p.get("person_detail", "")
        company_desc = p.get("company_desc", "")
        proof_key, proof_text = proof_map.get(vertical, ("spendflo", "Spendflo cut manual testing 50%"))

        pain_indicators = []
        vl = vertical.lower()
        if "fin" in vl:
            pain_indicators = ["Regression testing across payment/transaction flows", "Compliance validation", "API test coverage"]
        elif "health" in vl or "pharma" in vl:
            pain_indicators = ["Regulatory compliance testing", "Patient data validation", "Cross-platform testing"]
        elif "commerce" in vl:
            pain_indicators = ["Product catalog test coverage", "Multi-brand regression testing", "UI test maintenance"]
        else:
            pain_indicators = ["Test automation coverage gaps", "Regression cycle duration", "Manual testing overhead"]

        snap_id = gen_id("rs")
        conn.execute("""INSERT INTO research_snapshots (id, contact_id, account_id, entity_type,
            headline, summary, pain_indicators, company_products, company_metrics,
            sources, confidence_score, agent_run_id, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (snap_id, contact_id, account_id, "prospect",
             person_detail or f"{title} at {company}",
             company_desc or f"{company} - {vertical} company",
             json.dumps(pain_indicators),
             company_desc or "",
             json.dumps({"employee_count": p.get("employee_count"), "industry": vertical}),
             json.dumps(["run_bundle_import"]), 3, run_id, now))

        # Batch-prospect link
        conn.execute("""INSERT INTO batch_prospects (id, batch_id, contact_id, ab_group,
            sequence_status, position_in_batch) VALUES (?,?,?,?,?,?)""",
            (gen_id("bp"), batch_id, contact_id, p.get("ab_group", ""), "not_started", idx+1))

        # Create message drafts using batch 2 field names
        for touch_num, touch_type, subj_field, body_field in touch_map_b2:
            body_text = p.get(body_field, "")
            if not body_text:
                continue
            subj_text = p.get(subj_field, "") if subj_field else ""

            # Determine channel
            channel = "linkedin" if touch_type in ("inmail", "inmail_followup", "breakup", "call") else "email"

            draft_id = gen_id("md")
            wc = len(body_text.split())
            qc_passed = 1
            qc_flags = []
            if "\u2014" in body_text or "\u2013" in body_text:
                qc_passed = 0
                qc_flags.append("em_dash_found")

            # Use proof point from prospect data if available
            pp_used = p.get("proof_points_used", {})
            pp_key = ""
            if touch_num == 1:
                pp_key = pp_used.get("touch_1", proof_key)
            elif touch_num == 2:
                pp_key = pp_used.get("call_1", proof_key)
            elif touch_num == 3:
                pp_key = pp_used.get("touch_3", proof_key)
            elif touch_num == 4:
                pp_key = pp_used.get("call_2", proof_key)
            elif touch_num == 5:
                pp_key = pp_used.get("touch_5", proof_key)

            conn.execute("""INSERT INTO message_drafts (id, contact_id, batch_id, channel,
                touch_number, touch_type, subject_line, body, version, personalization_score,
                proof_point_used, pain_hook, opener_style, word_count, qc_passed, qc_flags,
                approval_status, ab_group, ab_variable, source, created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (draft_id, contact_id, batch_id, channel,
                 touch_num, touch_type, subj_text, body_text, 1,
                 p.get("personalization_score", 3),
                 pp_key, "", "", wc, qc_passed, json.dumps(qc_flags),
                 "draft", p.get("ab_group", ""),
                 "pain_hook", "run_bundle", now))
            imported_drafts += 1

            if touch_num == 1:
                conn.execute("""INSERT INTO draft_research_link (id, draft_id, contact_id,
                    profile_bullets, company_bullets, pain_hypothesis, why_testsigma,
                    confidence_score, template_name, created_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (gen_id("drl"), draft_id, contact_id,
                     json.dumps([person_detail]) if person_detail else "[]",
                     json.dumps([company_desc]) if company_desc else "[]",
                     json.dumps(pain_indicators[:1]),
                     proof_text, 3, "touch_1_inmail", now))

    wf_id = gen_id("wfrun")
    conn.execute("""INSERT INTO workflow_runs (id, workflow_id, workflow_type, channel, status,
        input_data, output_data, total_steps, completed_steps, started_at, completed_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (wf_id, "", "linkedin_batch_2_auto", "linkedin", "succeeded",
         json.dumps({"source": "auto_import_batch2", "bundle_prospects": len(prospects)}),
         json.dumps({"imported_contacts": imported_contacts, "imported_drafts": imported_drafts}),
         4, 4, now, now))

    conn.execute("""INSERT INTO activity_timeline (id, activity_type, channel, description, metadata, created_at)
        VALUES (?,?,?,?,?,?)""",
        (gen_id("evt"), "batch_auto_import", "linkedin",
         f"Auto-imported Batch 2: {imported_contacts} contacts, {imported_drafts} drafts",
         json.dumps({"batch_id": batch_id, "workflow_run_id": wf_id}), now))

    conn.execute("PRAGMA foreign_keys=ON")
    conn.commit()
    print(f"Auto-import batch 2: Done. {imported_contacts} contacts, {imported_drafts} drafts")
