# Email Outreach SOP — Drafting & Send Execution

## Scope
- This SOP is **Email-only**.
- Do not use LinkedIn send steps, LinkedIn cadence, or LinkedIn QA from `memory/sop-outreach.md`.
- LinkedIn InMail/follow-up operations are run separately in `memory/sop-outreach.md`.

⛔ **AUTHORIZED ACCOUNT RESTRICTION (Effective Mar 9, 2026):** Email outreach follows the same account universe restriction as all other channels. Every prospect receiving a T2 email must have their company in the Factor Accounts (38) list at `memory/target-accounts.md` or the TAM Accounts (312) list at `/Work/tam-accounts-mar26.csv`. This is enforced at batch-build time in `sop-prospect.md` and `sop-send.md` — if you are drafting a T2 email, the prospect should already have passed that gate.

## Multi-Channel T2 Email (After LinkedIn InMail T1) — Locked Formula Mar 9

When email is used as Touch 2 in the LinkedIn Outbound sequence (Day 5 after T1 InMail).

**CRITICAL — Reply Threading (INC-014, Mar 19 2026):** All T2 emails MUST be sent as replies to the T1 thread, NOT as new standalone emails. In the Apollo sequence builder, Step 2 must have "Reply to previous thread" checked. This was discovered unchecked Mar 19 and fixed. Before any T2 send session, verify this setting is still correct. Subject lines for T2 tasks will auto-inherit from the T1 thread with "RE:" prefix when reply mode is active.

### Locked Formula: Variant A (approved Mar 9, 2026)

The T2 email follows a 5-part structure. Each part must be executed in order. The formula must be INVISIBLE — it should read as a human wrote one cohesive message, not as a fill-in-the-blank template.

**Part 1 — Opening company fact (1 sentence)**
A specific, undeniably true statement about what the company does, builds, or sells. NOT an industry generalization. NOT a quality/emotion word (e.g., "rigor," "excellence"). A concrete, factual claim about their product or business model.
- ✅ "AuditBoard builds the platform that companies use to manage their internal audits, risk, and compliance programs."
- ✅ "Kaseya runs one of the largest portfolios of IT management products in the industry."
- ✅ "Fairfax Software's payment processing platform is deployed across tax and revenue agencies in half the states in the US."
- ❌ "AuditBoard sells rigor to its customers." (rigor = emotion, not a product)
- ❌ "Healthcare IT companies face complex compliance requirements." (industry generalization)

**Part 2 — "I'd imagine..." empathy bridge (1 sentence)**
Connects the opening fact to the specific QA/release pressure it creates for THEIR team. Makes the logic feel inevitable. Uses "I'd imagine" as the entry phrase.
- ✅ "I'd imagine that puts a certain pressure on your own releases, knowing the teams using your platform are auditors and compliance officers who notice everything."
- ✅ "I'd imagine every acquisition brings in a codebase with its own test environment that nobody outside that original team fully understands."

**Part 3 — LinkedIn callback (1 sentence)**
References the T1 InMail naturally as a bridge, naming the specific topic covered. Explains the channel switch practically — "but thought X was worth adding/sending separately." Does NOT apologize for reaching out again. Does NOT say "following up."
- Format: "I reached out on LinkedIn about [specific T1 topic], but thought [specific angle] was worth [adding / sending separately]."
- ✅ "I reached out on LinkedIn about Selenium overhead, but thought a coverage angle was worth adding."
- ✅ "I reached out on LinkedIn about regression efficiency, but thought a maintenance angle was worth sending separately."
- ❌ "I sent you a LinkedIn message but figured email was a better spot to share a proof point." (too corporate, announces the formula)

**Part 4 — Customer story + connection (2 sentences)**
Sentence 1: "One of our customers, [Name], [brief story — what they were dealing with and what changed]."
Sentence 2: Tie the result back to the prospect's specific situation. Use "Reminded me of..." or "Felt like the kind of thing..." — NOT "I thought you might find this interesting."
- ✅ "One of our customers, Hansard, was in a similar spot and cut their regression window from 8 weeks to 5 with AI that generates and heals tests automatically. Reminded me of the pressure your team is probably navigating."
- ✅ "One of our customers, CRED, reached 90% regression coverage using AI tests written in plain English. Reminded me of the kind of confidence that matters when government agencies are depending on your platform to process payments without interruption."

**Part 5 — Tied CTA (1 sentence) — Updated Mar 16, 2026**
An engagement question — NOT a meeting ask. Must echo the specific tension established in Parts 1-2. Generic CTAs ("Is this relevant for your team?") are not acceptable. This engagement-first CTA rule is now locked as the default for all T2 emails.
- ✅ "Does that tension actually show up in how you approach releases?" (mirrors Part 1: AuditBoard compliance irony)
- ✅ "Is the maintenance side something your team is trying to get ahead of?" (mirrors Part 1: Kaseya M&A complexity)
- ✅ "Is test coverage something your team is actively working to improve?" (mirrors Part 1: Fairfax state agency stakes)
- ❌ "What day works for a quick call?" (DO NOT use as T2 CTA — save for T3 or after engagement)
- ❌ "Is this something your team deals with?" (too generic)

### Hard Rules (non-negotiable)

- No em dashes anywhere
- No "I noticed" / "I saw" / "I came across"
- No "following up" / "circling back"
- No testsigma.com URL in body (removed entirely from T2)
- No "proof point" language (too corporate)
- No "figured email was a better spot" phrasing
- No meeting ask — T2 CTA is engagement only
- LinkedIn callback MUST name the specific T1 topic (not generic "about test automation")
- Opening MUST be a concrete company fact, not an industry observation
- Proof point rotation REQUIRED — T2 customer story must be different from T1 story
- Word count: 60-90 words (slightly longer than original 40-70 due to fuller structure)
- Subject line: "[topic] at [Company]" format (e.g., "QA cycles at AuditBoard", "Test maintenance at Kaseya")
- Send via: **Apollo UI only** — complete the Apollo sequence task to send. robert.gorham@testsigma.com is the linked sending account in Apollo. NEVER send outreach directly through Gmail MCP.
- NEVER SEND without Rob's explicit "APPROVE SEND"

### Proof Point Rotation Reference

| Story | Key fact | Best for |
|-------|----------|----------|
| Hansard | Regression window: 8 wks → 5 wks | Companies with long release cycles, compliance pressure |
| Sanofi | Test creation: 3 days → 80 min | Large enterprises, pharma, healthcare IT |
| CRED | 90% regression coverage, 5x faster | Coverage gaps, scale challenges |
| Medibuddy | 50% test maintenance reduction | Maintenance overhead, growing codebases, M&A complexity |
| Cisco | 35% regression reduction | Enterprise, platform companies, hardware-software complexity |

### Opening Angle Patterns

- **Irony angle:** Company's product/standards create internal QA pressure (AuditBoard audits compliance but must pass their own releases, HackerRank tests developers but must test their own platform, Datto protects MSPs from downtime but must be downtime-free)
- **M&A / portfolio complexity:** Multiple acquisitions = multiple inherited codebases with unknown test environments (Kaseya, Upland, Persistent, Tavant)
- **Regulatory / mission-critical:** Platform failures affect regulated customers or critical operations (Fairfax/state agencies, IDB Bank/banking, Ncontracts/banking compliance, Prevail Legal/legal case management)
- **Campaign criticality:** Platform errors during live campaigns have outsized impact (Mediaocean ad spend, Bynder brand campaigns)
- **Field operations:** Software embedded in deployed hardware or field systems (Trimble construction, Digi remote devices, Simpro field services)

### Sequence Position

- Step 2 of "LinkedIn Outbound - Q1 Priority Accounts" (Day 5, Manual Email task)
- Apollo task note instructs: "Send via Apollo UI using robert.gorham@testsigma.com linked account. Use T2 locked formula. Do NOT reference T1 InMail directly."
- Day count starts from Day 1 InMail send date

## Canonical References
- Primary detailed process: `docs/sops/outreach_email_sop.md`
- Sequence policy and workflow notes: `docs/sops/Tier1_Intent_Sequence_SOP_MASTER.md`

## Channel Isolation Rules (Mandatory)
1. Use a separate working draft doc for email runs.
2. Use only email QA checks during email review.
3. Track send/reply status in email systems only (Apollo email task queue + email tracker).
4. Never blend LinkedIn touch IDs/statuses into email tracking.
5. If LinkedIn outreach is needed, handoff to `memory/sop-outreach.md` as a separate workflow.

## Email Cadence (Channel-Local)
- **Touch 1:** Personalized first outreach email.
- **Touch 2:** Follow-up (new angle/proof point).
- **Touch 3:** Respectful close-out/breakup.

Rules:
- Each touch must use a distinct angle/proof point.
- Do not reuse LinkedIn wording patterns verbatim.
- Email sequence progression is controlled in Apollo task queue, not LinkedIn tooling.

## Writing & QA Standards (Email)
- No em dashes in body text.
- Subject line required and personalized.
- 4-6 concise sentences, clean paragraph spacing.
- One clear CTA, low-pressure tone, natural human wording.
- Proof point must be real and tied to the contact context.
- No copy/paste residue (wrong name/company/details).
- Signature must be complete and consistent.

## Execution Flow (Email)
1. Pull pending email tasks from Apollo sequence queue.
2. Draft or paste personalized email copy from email working doc.
3. Run QA checklist (style, personalization, CTA, factual correctness).
4. Send by completing task in Apollo UI.
5. Verify send registered on contact activity timeline.
6. Update email tracker status and notes.
7. Monitor bounce/reply/engagement and queue next touch.

## Apollo + Local DB Update Procedure (Required)
Every completed email action must update BOTH systems in this order:

1. **Apollo update (source of sequence truth)**
   - Complete/send from Apollo task queue.
   - Confirm contact advanced to next step (or marked complete/stopped).
   - If not advancing, add a disposition note (blocked/bounce/manual hold).
2. **Local DB update (internal analytics + audit)**
   - Insert/update contact status and stage in local email DB.
   - Log touch event with channel=`email`, touch number, state, and timestamp.
   - Store/refresh draft metadata and final sent version reference.
   - Log reply/bounce outcomes as they arrive.
   - Append activity timeline entry for each material action.

### Minimum fields to track per email send
- contact identifier (id + email)
- channel (`email`)
- touch number
- message/draft id
- send state (`queued`/`sent`/`failed`/`bounced`)
- sent timestamp
- Apollo sequence/task reference
- owner/operator
- next-step due date

### Reconciliation check (end of run)
- Apollo sent count == Local DB sent count for this run window.
- Apollo stopped/paused contacts are reflected in local status.
- Any mismatch gets logged as `sync_gap` in run notes and fixed before close.

## Data & Tracking (Email DB)
Email records are isolated in the email database:
- **DB path:** `api/data/outreach_email.db`
- Typical objects to audit: contacts, message drafts, send events, replies, activity timeline
- Keep email operational metrics and logs in this channel DB only

If database bootstrap/reset is needed, run:
```bash
python scripts/init_isolated_channel_dbs.py \
  --source api/data/outreach_seed.db \
  --email-db api/data/outreach_email.db \
  --linkedin-db api/data/outreach_linkedin.db
```

## Exit Checklist (Email Run)
- [ ] All pending tasks processed or explicitly deferred with reason.
- [ ] All sent emails reflected in Apollo activity.
- [ ] All sent emails reflected in local email DB activity/touch logs.
- [ ] Apollo and local DB counts reconciled for the run window.
- [ ] Tracker updated with sent date + next touch date.
- [ ] Bounce/reply exceptions logged.
- [ ] No LinkedIn statuses or IDs used in email tracking fields.

---

## Run Learnings Log (Email)

### Wave 6 Batch 2 (Mar 12, 2026)
- **Ownership-blocked enrollment:** Existing Apollo contacts owned by other team members cannot be enrolled via API even with `contacts_without_ownership_permission: true`. Casey Florig was the affected contact. Must enroll manually in Apollo UI or transfer ownership first.
- **Apollo enrollment flags for multi-contact batches:** Always include `sequence_same_company_in_same_campaign: true`, `sequence_finished_in_other_campaigns: true`, and `sequence_active_in_other_campaigns: true` when enrolling email batches with multiple contacts per company.
- **Catchall domain prevalence:** 8 of 12 companies in W6B2 have catchall domains (BeyondTrust, Jack Henry, Bluevine, hims & hers, SingleStore, Skedulo, EverBank, KIBO). Catchall means bounces won't show as hard bounces. Monitor open/click signals as deliverability proxy.
