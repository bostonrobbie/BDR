"""
End-to-end pipeline test for the BDR Outreach Command Center.
Tests all 10 phases of the batch pipeline + new model functions.
"""
import sys
import os
import json
import traceback

sys.path.insert(0, os.path.dirname(__file__))

# Use test DB
os.environ["OCC_DB_PATH"] = "/sessions/jolly-keen-franklin/BDR/test_pipeline.db"

from src.db import models, init_db

def run_test():
    results = []

    def log(phase, success, detail=""):
        status = "PASS" if success else "FAIL"
        results.append((phase, status, detail))
        print(f"  [{status}] {phase}: {detail}")

    # ─── SETUP ────────────────────────────────────────────
    print("\n=== SETUP: Initialize test database ===")
    try:
        # Remove old test DB if exists
        db_path = os.environ["OCC_DB_PATH"]
        if os.path.exists(db_path):
            os.remove(db_path)
        if os.path.exists(db_path + "-wal"):
            os.remove(db_path + "-wal")
        if os.path.exists(db_path + "-shm"):
            os.remove(db_path + "-shm")

        init_db.init_db()
        log("DB Init", True, "Database created with all tables")
    except Exception as e:
        log("DB Init", False, str(e))
        traceback.print_exc()
        return results

    # ─── PHASE 1: Initialize (BatchBuilder) ───────────────
    print("\n=== PHASE 1: Initialize ===")
    try:
        from src.agents.batch_builder import BatchPipeline as BatchBuilder

        config = {
            "target_count": 3,
            "ab_variable": "pain_hook",
            "ab_groups": {
                "A": "Flaky/brittle tests angle",
                "B": "Release velocity angle"
            },
            "mix_ratio": {"qa_leaders": 2, "vp_eng": 1},
            "saved_search_url": "https://example.com/test-search",
        }

        builder = BatchBuilder(batch_number=99, config=config)
        builder.initialize()

        assert builder.batch_id is not None, "batch_id should be set"
        assert builder.run_id is not None, "run_id should be set"
        log("Initialize", True, f"batch_id={builder.batch_id}, run_id={builder.run_id}")
    except Exception as e:
        log("Initialize", False, str(e))
        traceback.print_exc()
        return results

    # ─── PHASE 2: Pre-Brief ───────────────────────────────
    print("\n=== PHASE 2: Pre-Brief ===")
    try:
        brief = builder.phase_pre_brief()
        log("Pre-Brief", True, f"Got brief with {len(brief.get('insights', []))} insights (first batch = defaults)")
    except Exception as e:
        log("Pre-Brief", False, str(e))
        traceback.print_exc()

    # ─── PHASE 3: Extract (simulate prospects) ────────────
    print("\n=== PHASE 3: Extract ===")
    try:
        # Create test accounts
        test_accounts = []
        companies = [
            {"name": "Acme FinTech", "domain": "acmefintech.com", "industry": "FinTech",
             "employee_count": 500, "employee_band": "201-500"},
            {"name": "HealthCo Digital", "domain": "healthco.com", "industry": "Healthcare",
             "employee_count": 2000, "employee_band": "1001-5000"},
            {"name": "RetailMax", "domain": "retailmax.com", "industry": "E-Commerce",
             "employee_count": 300, "employee_band": "201-500"},
        ]
        for comp in companies:
            acc = models.create_account(comp)
            test_accounts.append(acc)

        # Create test contacts
        test_contacts = []
        people = [
            {"first_name": "Alice", "last_name": "Chen", "title": "Director of QA",
             "persona_type": "qa_leader", "seniority_level": "Director",
             "email": "alice@acmefintech.com", "linkedin_url": "https://linkedin.com/in/alicechen",
             "tenure_months": 18, "recently_hired": 0, "source": "sales_nav"},
            {"first_name": "Bob", "last_name": "Kumar", "title": "VP Engineering",
             "persona_type": "vp_eng", "seniority_level": "VP",
             "email": "bob@healthco.com", "linkedin_url": "https://linkedin.com/in/bobkumar",
             "tenure_months": 4, "recently_hired": 1, "source": "sales_nav"},
            {"first_name": "Carol", "last_name": "Martinez", "title": "Head of Quality Engineering",
             "persona_type": "qa_leader", "seniority_level": "Director",
             "email": "carol@retailmax.com", "linkedin_url": "https://linkedin.com/in/carolm",
             "tenure_months": 36, "recently_hired": 0, "source": "sales_nav"},
        ]
        for i, person in enumerate(people):
            person["account_id"] = test_accounts[i]["id"]
            contact = models.create_contact(person)
            test_contacts.append(contact)

        # Add contacts to batch
        conn = models.get_db()
        for contact in test_contacts:
            conn.execute(
                "INSERT INTO batch_prospects (batch_id, contact_id) VALUES (?, ?)",
                (builder.batch_id, contact["id"])
            )
        conn.commit()

        # Update batch prospect count
        conn.execute(
            "UPDATE batches SET prospect_count=? WHERE id=?",
            (len(test_contacts), builder.batch_id)
        )
        conn.commit()
        conn.close()

        builder.contact_ids = [c["id"] for c in test_contacts]
        log("Extract", True, f"Created {len(test_contacts)} test contacts in {len(test_accounts)} accounts")
    except Exception as e:
        log("Extract", False, str(e))
        traceback.print_exc()

    # ─── PHASE 4: Research (simulate) ─────────────────────
    print("\n=== PHASE 4: Research ===")
    try:
        from src.agents.researcher import structure_person_research, structure_company_research, detect_signals

        # Simulate person research
        for i, contact in enumerate(test_contacts):
            person_data = structure_person_research("", {
                "headline": f"{people[i]['title']} at {companies[i]['name']}",
                "about": f"Experienced {people[i]['title']} focused on automation and quality.",
                "current_role_description": f"Leading QA and testing efforts at {companies[i]['name']}",
                "tenure_months": people[i]["tenure_months"],
                "career_history": [
                    {"company": companies[i]["name"], "title": people[i]["title"], "years": "2024-present"},
                    {"company": "Previous Corp", "title": "QA Manager", "years": "2020-2024"},
                ],
            })

            models.save_research({
                "contact_id": contact["id"],
                "account_id": test_accounts[i]["id"],
                "entity_type": "person",
                "headline": person_data.get("headline", ""),
                "summary": person_data.get("about", ""),
                "career_history": person_data.get("career_history", []),
                "responsibilities": person_data.get("current_role_description", ""),
                "sources": ["linkedin"],
            })

        # Simulate company research
        company_tools = [["selenium", "cypress"], ["katalon"], []]
        for i, acc in enumerate(test_accounts):
            company_data = structure_company_research({
                "description": f"{companies[i]['name']} is a {companies[i]['industry']} company.",
                "employee_count": companies[i]["employee_count"],
                "industry": companies[i]["industry"],
                "products": [f"{companies[i]['name']} Platform"],
                "tech_stack": company_tools[i],
                "recent_news": "Digital transformation initiative underway" if i == 0 else "",
                "hiring_signals": "Hiring Senior QA Engineer" if i < 2 else "",
                "funding_info": "$50M Series C" if i == 0 else "",
            })

            models.save_research({
                "account_id": acc["id"],
                "entity_type": "company",
                "summary": company_data.get("description", ""),
                "tech_stack_signals": company_data.get("known_tools", []),
                "company_products": company_data.get("products", []),
                "company_news": company_data.get("recent_news", ""),
                "hiring_signals": company_data.get("hiring_signals", ""),
                "sources": ["website", "news"],
            })

            # Detect and store signals
            signals = detect_signals(company_data, {"recently_hired": people[i]["recently_hired"]})
            for sig in signals:
                sig["contact_id"] = test_contacts[i]["id"]
                sig["account_id"] = acc["id"]
                models.create_signal(sig)

        log("Research", True, f"Saved person + company research for {len(test_contacts)} contacts")
    except Exception as e:
        log("Research", False, str(e))
        traceback.print_exc()

    # ─── PHASE 5: Score ───────────────────────────────────
    print("\n=== PHASE 5: Score ===")
    try:
        from src.agents.scorer import batch_score

        scored = batch_score([c["id"] for c in test_contacts])
        for i, s in enumerate(scored):
            name = f"{test_contacts[i]['first_name']} {test_contacts[i]['last_name']}" if i < len(test_contacts) else "?"
            print(f"    {name}: priority={s.get('priority_score', s.get('score', '?'))}")

        log("Score", True, f"Scored {len(scored)} contacts")
    except Exception as e:
        log("Score", False, str(e))
        traceback.print_exc()

    # ─── PHASE 6: A/B Assign ─────────────────────────────
    print("\n=== PHASE 6: A/B Assign ===")
    try:
        from src.agents.ab_assigner import assign_ab_groups

        ab_result = assign_ab_groups(
            contact_ids=[c["id"] for c in test_contacts],
            variable="pain_hook",
            batch_id=builder.batch_id
        )

        log("A/B Assign", True,
            f"Group A: {ab_result['group_a_count']}, Group B: {ab_result['group_b_count']}")
    except Exception as e:
        log("A/B Assign", False, str(e))
        traceback.print_exc()

    # ─── PHASE 7: Messages (simulate) ─────────────────────
    print("\n=== PHASE 7: Messages ===")
    try:
        touch_configs = [
            {"touch_number": 1, "touch_type": "inmail", "channel": "linkedin"},
            {"touch_number": 3, "touch_type": "inmail_followup", "channel": "linkedin"},
            {"touch_number": 5, "touch_type": "email", "channel": "email"},
            {"touch_number": 6, "touch_type": "breakup", "channel": "linkedin"},
        ]

        msg_count = 0
        for contact in test_contacts:
            for tc in touch_configs:
                msg = models.create_message_draft({
                    "contact_id": contact["id"],
                    "batch_id": builder.batch_id,
                    "channel": tc["channel"],
                    "touch_number": tc["touch_number"],
                    "touch_type": tc["touch_type"],
                    "subject_line": f"Testing at {contact.get('title', 'your company')}",
                    "body": f"Hi {contact['first_name']}, this is a test message for touch {tc['touch_number']}. "
                            f"We helped Sanofi cut regression from 3 days to 80 minutes. Worth a quick chat?",
                    "personalization_score": 2,
                    "proof_point_used": "sanofi",
                    "pain_hook": "flaky_tests",
                    "opener_style": "career_reference",
                    "ask_style": "soft",
                    "word_count": 30,
                })
                msg_count += 1

        # Also add call snippets as touch 2 and 4
        for contact in test_contacts:
            for tn in [2, 4]:
                models.create_message_draft({
                    "contact_id": contact["id"],
                    "batch_id": builder.batch_id,
                    "channel": "phone",
                    "touch_number": tn,
                    "touch_type": "call_snippet",
                    "body": f"Hey {contact['first_name']}, this is Rob from Testsigma. Quick question about testing at {companies[0]['name']}.",
                    "word_count": 15,
                })
                msg_count += 1

        log("Messages", True, f"Created {msg_count} message drafts")
    except Exception as e:
        log("Messages", False, str(e))
        traceback.print_exc()

    # ─── PHASE 8: QC Gate ─────────────────────────────────
    print("\n=== PHASE 8: QC Gate ===")
    try:
        from src.agents.quality_gate import run_quality_gate

        messages = models.list_messages(batch_id=builder.batch_id)
        passed = 0
        failed = 0
        for msg in messages:
            if msg.get("touch_type") == "call_snippet":
                continue
            qc = run_quality_gate(msg)
            if qc.get("passed"):
                passed += 1
            else:
                failed += 1
                # Show first failure reason
                if failed <= 2:
                    fails = [c["check"] for c in qc.get("checks", []) if not c.get("passed")]
                    print(f"    QC fail for touch {msg.get('touch_number')}: {fails[:3]}")

        log("QC Gate", True, f"{passed} passed, {failed} failed out of {passed+failed} messages")
    except Exception as e:
        log("QC Gate", False, str(e))
        traceback.print_exc()

    # ─── PHASE 9: Generate HTML ───────────────────────────
    print("\n=== PHASE 9: Generate HTML ===")
    try:
        from src.agents.deliverable_generator import generate_batch_html

        html_path = generate_batch_html(builder.batch_id, builder.batch_number)

        assert html_path is not None, "HTML path should not be None"
        assert os.path.exists(html_path), f"HTML file should exist at {html_path}"

        file_size = os.path.getsize(html_path)

        # Read and check for key elements
        with open(html_path, 'r') as f:
            html_content = f.read()

        checks = {
            "has_tracker_table": "prospect-row" in html_content or "tracker-table" in html_content,
            "has_prospect_cards": "card" in html_content,
            "has_copy_buttons": "copyMessage" in html_content or "copy-btn" in html_content,
            "has_alice": "Alice" in html_content,
            "has_bob": "Bob" in html_content,
            "has_carol": "Carol" in html_content,
        }

        all_ok = all(checks.values())
        failed_checks = [k for k, v in checks.items() if not v]

        if failed_checks:
            log("Generate HTML", False, f"Missing: {failed_checks}. File: {html_path} ({file_size} bytes)")
        else:
            log("Generate HTML", True, f"{html_path} ({file_size:,} bytes), all content checks passed")
    except Exception as e:
        log("Generate HTML", False, str(e))
        traceback.print_exc()

    # ─── PHASE 10: Finalize ───────────────────────────────
    print("\n=== PHASE 10: Finalize ===")
    try:
        builder.finalize()

        # Verify agent run completed
        conn = models.get_db()
        run = conn.execute("SELECT * FROM agent_runs WHERE id=?", (builder.run_id,)).fetchone()
        conn.close()

        assert run is not None, "Agent run should exist"
        assert run["status"] == "completed", f"Status should be completed, got {run['status']}"

        log("Finalize", True, f"Agent run {builder.run_id} marked completed")
    except Exception as e:
        log("Finalize", False, str(e))
        traceback.print_exc()

    # ─── BONUS: Test new model functions ──────────────────
    print("\n=== BONUS: Test new model functions ===")

    # get_batch_summary
    try:
        summary = models.get_batch_summary(builder.batch_id)
        assert "error" not in summary, f"Got error: {summary.get('error')}"
        assert summary["contact_count"] == 3, f"Expected 3 contacts, got {summary['contact_count']}"
        log("get_batch_summary", True, f"contact_count={summary['contact_count']}, messages={summary['messages_generated']}")
    except Exception as e:
        log("get_batch_summary", False, str(e))
        traceback.print_exc()

    # get_intelligence_data
    try:
        intel = models.get_intelligence_data()
        assert "by_persona" in intel, "Should have by_persona"
        log("get_intelligence_data", True, f"Keys: {list(intel.keys())}")
    except Exception as e:
        log("get_intelligence_data", False, str(e))
        traceback.print_exc()

    # get_prep_card
    try:
        prep = models.get_prep_card(test_contacts[0]["id"])
        assert "error" not in prep, f"Got error: {prep.get('error')}"
        assert "contact" in prep, "Should have contact data"
        log("get_prep_card", True, f"Keys: {list(prep.keys())}")
    except Exception as e:
        log("get_prep_card", False, str(e))
        traceback.print_exc()

    # sync_html_status
    try:
        sync_result = models.sync_html_status(
            contact_id=test_contacts[0]["id"],
            stage="touch_1_sent",
            reply_tag=None,
            notes="Test sync"
        )
        assert sync_result.get("success"), f"Sync failed: {sync_result}"
        log("sync_html_status", True, f"Synced stage to touch_1_sent")
    except Exception as e:
        log("sync_html_status", False, str(e))
        traceback.print_exc()

    # ─── SUMMARY ──────────────────────────────────────────
    print("\n" + "=" * 60)
    passed = sum(1 for _, s, _ in results if s == "PASS")
    failed = sum(1 for _, s, _ in results if s == "FAIL")
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(results)} tests")
    if failed > 0:
        print("\nFailed tests:")
        for phase, status, detail in results:
            if status == "FAIL":
                print(f"  - {phase}: {detail}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    run_test()
