# Email Outreach SOP — Drafting & Send Execution

## Scope
- This SOP is **Email-only**.
- Do not use LinkedIn send steps, LinkedIn cadence, or LinkedIn QA from `memory/sop-outreach.md`.
- LinkedIn InMail/follow-up operations are run separately in `memory/sop-outreach.md`.

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
- [ ] Tracker updated with sent date + next touch date.
- [ ] Bounce/reply exceptions logged.
- [ ] No LinkedIn statuses or IDs used in email tracking fields.
