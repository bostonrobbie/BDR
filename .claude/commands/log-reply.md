# Log Reply - Record a prospect reply and update the feedback loop

You are Rob's BDR assistant. Rob received a reply and wants to log it so the system learns.

## Files to Load
- `work/reply-log.csv` — append the new reply record
- `work/results.json` — recompute analytics after logging
- `work/pipeline-state.json` — update warm leads or send totals
- `work/dnc-list.json` — add if negative/hostile reply

## Input
Rob will provide:
- Prospect name and company (or batch reference)
- The reply text (pasted or summarized)
- Optionally: which touch triggered it (Touch 1, 2, or 3)

## Process

### Step 1: Identify the prospect
Look up the prospect in:
1. `batch7-send-tracker.json` or relevant batch tracker
2. The SQLite DB (`outreach.db` contacts table)

Extract: name, company, title, vertical, persona_type, batch_number, touch_number, channel, proof_point_used, opener_style, personalization_score, ab_group, message word count.

### Step 2: Classify the reply
Determine the intent:
- **positive** — interested, wants to meet, asks for info
- **polite** — thanks, acknowledge, non-committal
- **negative** — not interested, remove me, wrong person
- **referral** — forwarded, "talk to [name]"
- **has_tool** — "we use [tool]"
- **timing** — not now, maybe later, next quarter
- **curiosity** — how does it work, tell me more

### Step 3: Tag what triggered the reply
- **opener** — they referenced the personalized question
- **pain_hook** — they engaged with the problem hypothesis
- **proof_point** — they asked about the customer story/numbers
- **timing** — they said "good timing" or "evaluating"
- **referral** — forwarded to someone
- **not_interested** — declined
- **unknown** — can't determine

### Step 4: Append to reply-log.csv
Add a row with all fields:
```
date,prospect_name,company,title,vertical,persona_type,batch_number,touch_number,channel,reply_intent,reply_tag,proof_point_used,opener_style,personalization_score,ab_group,message_length,response_drafted,next_action,notes
```

### Step 5: Recompute results.json
After appending, recompute the analytics:
```python
python scripts/update_results.py
```
If the script doesn't exist, manually update `work/results.json`:
- Increment `total_replies`
- Update `by_persona`, `by_vertical`, `by_proof_point`, `by_reply_tag` counts
- Recompute `overall_reply_rate` = total_replies / total_prospects_contacted
- Update `insights` if enough data (5+ replies in any category)

### Step 6: Update pipeline state
- If **positive** or **curiosity** → add to `warm_leads` in `pipeline-state.json`
- If **negative** with "remove me" → add to `work/dnc-list.json`
- If **referral** → note the referred person for next `/prospect` run

### Step 7: Confirm to Rob
Output a summary:
```
Reply logged:
  Prospect: [Name] @ [Company]
  Intent: [positive/negative/etc.]
  Tag: [opener/proof_point/etc.]
  Next action: [book meeting / draft response / set reminder / add to DNC]
  Results updated: [total replies now X, reply rate Y%]
```

## Rules
- Always log, even negative replies (they're data points for learning)
- If this is the first reply logged, congratulate Rob and note the feedback loop is now active
- After 5+ replies, start generating mini-insights (e.g., "3 of 5 replies triggered by proof points")
- After 10+ replies, the `/pre-brief` command will produce meaningful "What's Working" data
