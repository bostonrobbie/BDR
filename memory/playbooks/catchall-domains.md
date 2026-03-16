# Playbook: Catchall Domain Handling

## When to Use
When a contact's email domain is flagged as "catchall" by Apollo. Catchall means the mail server accepts ALL emails to any address at that domain, so Apollo can't verify if the specific address actually reaches a real inbox.

---

## What Catchall Means

A catchall (or "accept-all") mail server configuration accepts email sent to any address at the domain, even nonexistent ones. This means:
- `realuser@company.com` — gets delivered
- `fakeuser12345@company.com` — ALSO gets delivered (to a catch-all inbox or /dev/null)
- Apollo shows email_status as "verified" but with `email_domain_catchall: true`

The email won't bounce, but it might not reach the intended person. The risk is that the address was extrapolated (pattern-matched) rather than confirmed.

---

## Known Catchall Domains (from our work)

| Domain | Company | Confirmed Catchall | Notes |
|--------|---------|-------------------|-------|
| beyondtrust.com | BeyondTrust | Yes (Session 26) | Emails deliverable but unverified |
| northerntrust.com | Northern Trust | Yes (Session 26) | Emails deliverable but unverified |
| ntrs.com | Northern Trust | Yes (Session 26) | Alternate domain, same behavior |
| google.com | Google/YouTube | Yes (Session 7) | Used for Des Keane, Hrishikesh Aradhye |

## Known NON-Catchall Domains

| Domain | Company | Notes |
|--------|---------|-------|
| epicor.com | Epicor | Emails are verified normally |
| fidelity.com | Fidelity | Emails are verified normally |
| chase.com | JPMorgan Chase | Verified (some extrapolated like Rose Serao) |
| cboe.com | Cboe Global Markets | Verified |

---

## Decision Framework

### Proceed with catchall emails when:
1. The email pattern matches the company's known format (e.g., `first.last@company.com` and you see other employees using that pattern)
2. The contact was found via Apollo with a confidence score
3. The contact is at a high-priority TAM or Factor account
4. There's no alternative way to reach them (no InMail credits, no verified alternate email)

### Skip or flag catchall emails when:
1. The email was purely extrapolated with no supporting evidence
2. The contact is at a low-priority account (not worth the risk to sender reputation)
3. You have InMail credits and can reach them on LinkedIn instead
4. Multiple contacts at the same catchall company are all extrapolated (high risk of multiple bad sends)

### How to assess the risk:
- Check `email_true_status` in Apollo: "Verified" is better than "User Managed" or blank
- Check if `extrapolated_email_confidence` is set — higher is better
- Check `email_from_customer` — if true, the email came from CRM data (more reliable)
- Look at other contacts at the same company — if some emails are confirmed working (e.g., from CRM import), the pattern is likely valid

---

## Tracking Catchall Sends

When sending to catchall domains:
1. Note "catchall" in the batch tracker HTML for that contact
2. Monitor for soft bounces (which won't happen with catchall, but monitor for no-opens after 3+ days)
3. If 0 opens across all contacts at a catchall domain after 5+ days, the emails may be going to a black hole

---

## SOP Reference
Per `sop-tam-outbound.md` Part 5: Catchall domains are handled case-by-case. They are NOT automatically excluded, but the risk should be noted and tracked.

---

*Last updated: 2026-03-12 — consolidated from Sessions 7, 16, 26*
