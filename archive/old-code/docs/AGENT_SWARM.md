# Agent Swarm Design

## Overview

The OCC uses a Coordinator + Worker swarm pattern. A Supervisor Agent orchestrates specialized worker agents, routing tasks, managing handoffs, and ensuring quality gates are passed before outputs reach Rob.

```
                    ┌─────────────────┐
                    │   SUPERVISOR    │
                    │   (Coordinator) │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────┴─────┐     ┌─────┴─────┐     ┌─────┴─────┐
    │ Research   │     │  Draft    │     │ Analysis  │
    │  Cluster   │     │  Cluster  │     │  Cluster  │
    └─────┬─────┘     └─────┬─────┘     └─────┬─────┘
          │                  │                  │
    ┌─────┴─────┐     ┌─────┴─────┐     ┌─────┴─────┐
    │Prospector │     │ Message   │     │ Pre-Brief │
    │  Agent    │     │  Writer   │     │  Agent    │
    ├───────────┤     ├───────────┤     ├───────────┤
    │ Research  │     │ Sequencer │     │ Insights  │
    │  Agent    │     │  Agent    │     │  Agent    │
    ├───────────┤     ├───────────┤     ├───────────┤
    │ Signal    │     │ Call Prep │     │ Experiment│
    │ Scanner   │     │  Agent    │     │  Analyst  │
    └───────────┘     ├───────────┤     └───────────┘
                      │ Reply     │
                      │ Triage    │
                      ├───────────┤
                      │ Quality   │
                      │  Gate     │
                      └───────────┘
```

## Supervisor Agent

**Role:** Orchestrates all other agents. Routes tasks. Manages handoffs. Decides what needs to run and in what order.

**Capabilities:**
- Receives task requests from the dashboard UI
- Decomposes tasks into sub-tasks for worker agents
- Manages execution order and dependencies
- Aggregates outputs from multiple agents
- Enforces quality gates before delivering to Rob
- Tracks token usage across all agents

**Decision Logic:**
```
IF task = "build_batch":
  1. Run Pre-Brief Agent (if previous batches exist)
  2. Run Prospector Agent (extract from Sales Nav)
  3. For each prospect:
     a. Run Research Agent (person + company)
     b. Run Message Writer (all 6 touches)
     c. Run Quality Gate (validate all messages)
  4. Run Sequencer Agent (schedule follow-ups)
  5. Deliver batch to dashboard

IF task = "handle_reply":
  1. Run Reply Triage Agent (classify intent)
  2. Run Message Writer (draft response if needed)
  3. Run Quality Gate (validate response)
  4. Deliver recommendation to dashboard

IF task = "prep_call":
  1. Load research data from DB
  2. Run Call Prep Agent (build call card)
  3. Deliver to Calls Workspace

IF task = "weekly_analysis":
  1. Run Insights Agent (analyze all data)
  2. Run Experiment Analyst (evaluate A/B tests)
  3. Deliver to Intelligence page
```

## Worker Agents

### 1. Prospector Agent
**Input:** Sales Navigator saved search reference, batch config (size, mix ratio, A/B variable)
**Output:** Qualified prospect list with basic data
**Process:**
1. Read search results page via Chrome tools
2. Extract names, titles, companies, headlines
3. Run qualification checklist (manager+, ICP title, US-based, software QA)
4. Check for prior interactions (Messaged/Viewed in Sales Nav)
5. Dedupe against existing contacts in DB
6. Apply mix ratio (12-15 QA + 8-10 VP Eng + 2-3 Buyer Intent)
7. Flag Buyer Intent signals

**Stored Data:** accounts, contacts, icp_scores, batch_prospects

### 2. Research Agent
**Input:** Contact ID, Account ID
**Output:** Structured research snapshot (person + company)
**Process:**
1. Visit LinkedIn profile via Chrome tools
2. Extract: headline, about section, responsibilities, career history, recent activity
3. Check if company already has research snapshot in DB (cache hit = skip)
4. If no company snapshot: web search for company website, news, job postings, engineering blog
5. Extract: products, metrics, tech stack signals, pain indicators, recent news
6. Store structured JSON with source URLs

**Stored Data:** research_snapshots (person + company), agent_runs
**Token Efficiency:** Company research is cached. If another contact is at the same company, reuse the existing snapshot.

### 3. Signal Scanner Agent
**Input:** Account ID or batch scan request
**Output:** Detected signals (buyer intent, job postings, funding, leadership changes)
**Process:**
1. Check Sales Navigator for buyer intent signals
2. Search for recent QA/testing job postings at the company
3. Search for recent funding announcements
4. Search for leadership changes in QA/engineering
5. Check for major product launches
6. Store signals with timestamps and source URLs

**Stored Data:** signals table, re-engagement triggers

### 4. Message Writer Agent
**Input:** Contact ID with research data, touch number, channel, A/B group assignment
**Output:** Copy-paste-ready message
**Process:**
1. Load research data for person and company
2. Load SOP rules from CLAUDE.md (word count, structure, voice rules)
3. Load learning data (what proof points and angles are working)
4. Select proof point matched to prospect's pain and vertical
5. Apply A/B variable if applicable
6. Generate message following the 6-element structure (Touch 1) or appropriate structure (Touch 3-6)
7. Calculate word count and personalization score
8. Pass to Quality Gate before delivery

**Stored Data:** message_drafts
**Voice Rules Enforced:**
- No em dashes
- 70-120 words (Touch 1), 40-70 (Touch 3), 30-50 (Touch 6), <40 (call snippets)
- One question max
- No feature dumping
- Personalized opener referencing specific research data
- Soft ask with easy out

### 5. Sequencer Agent
**Input:** Contact ID, Touch 1 sent timestamp
**Output:** Follow-up schedule for Touches 2-6
**Process:**
1. Calculate due dates: T2=Day 3, T3=Day 5, T4=Day 8, T5=Day 10, T6=Day 15
2. If no email available, skip T5 and move T6 to Day 12
3. Check prospect's timezone for call window optimization
4. Create followup records in DB
5. If prospect replies at any point, pause remaining follow-ups

**Stored Data:** followups

### 6. Call Prep Agent
**Input:** Contact ID
**Output:** Call card with 3-line snippet, objection card, context panel
**Process:**
1. Load research data and previous touchpoints
2. Generate 3-line call snippet (opener, pain hypothesis, bridge to ask)
3. Use DIFFERENT proof point and angle from written touches
4. Load predicted objection and pre-loaded response
5. Generate discovery questions tailored to their situation
6. Include company snapshot and LinkedIn activity summary

**Stored Data:** message_drafts (touch_type = 'call_snippet')

### 7. Reply Triage Agent
**Input:** Reply text, contact context
**Output:** Intent classification, reply tag, recommended next step
**Process:**
1. Classify intent: positive, neutral, not_now, referral, unsubscribe, negative
2. Assign reply tag: opener, pain_hook, proof_point, timing, referral, not_interested, unknown
3. Generate recommended next step based on intent
4. If positive: draft meeting time proposal
5. If referral: create new contact record for referred person
6. If negative/unsubscribe: mark as Do Not Contact if explicit
7. Update contact stage accordingly

**Stored Data:** replies, contacts (stage update)

### 8. Quality Gate Agent
**Input:** Any agent output (message, research, call snippet)
**Output:** PASS or FAIL with specific flags
**Checks:**
1. No hallucinated customer names (must exist in proof points table)
2. No hallucinated stats (must match known proof points)
3. No placeholder text ([Name], [Company], [specific], etc.)
4. No em dashes (U+2014)
5. Personalization exists (references specific research data)
6. Research has 2+ source citations
7. Word count in range per touch type
8. One question max per message
9. Opener variety (no more than 3 "I noticed" in a batch)
10. Proof point rotation (no consecutive same proof point)

**Blocking:** Failed messages are flagged and cannot be marked as "ready" until fixed.

### 9. Pre-Brief Agent
**Input:** All historical batch data
**Output:** 5-line "What's Working" summary
**Process:**
1. Query reply rates by persona type
2. Query reply rates by proof point
3. Query reply rates by vertical
4. Analyze A/B test results
5. Identify patterns in high-performing messages
6. Generate: best persona, best proof point, best vertical, best pattern, stop doing

**Stored Data:** batches.pre_brief

### 10. Insights Agent
**Input:** All historical data
**Output:** Actionable insights and recommendations
**Process:**
1. Calculate funnel conversion rates across all batches
2. Identify statistically significant patterns
3. Generate opportunity attribution analysis
4. Recommend adjustments to mix ratio, proof point selection, persona targeting
5. Estimate token efficiency trends

**Stored Data:** analytics reports

### 11. Experiment Analyst Agent
**Input:** Experiment configuration and accumulated data
**Output:** Experiment results and recommendations
**Process:**
1. Calculate metrics per A/B group (reply rate, meetings, opportunities)
2. Assess sample size sufficiency
3. Declare winner or inconclusive
4. Recommend next experiment variable
5. Generate written conclusion

**Stored Data:** experiments (results, conclusion, winner)

## Agent Communication Protocol

Agents communicate through the Supervisor via structured JSON messages:

```json
{
  "from": "research_agent",
  "to": "supervisor",
  "type": "task_complete",
  "task_id": "uuid",
  "status": "success",
  "output": { ... },
  "tokens_used": 1250,
  "duration_ms": 8400,
  "sources_used": ["url1", "url2"]
}
```

## Safety Constraints

1. **No autonomous sending** - Agents prepare, Rob sends
2. **No credential storage** - Agents use Rob's active browser session
3. **No hallucination** - Quality Gate blocks ungrounded claims
4. **No platform violations** - No mass scraping, no bot behavior
5. **Full transparency** - Every agent run is logged with inputs, outputs, and decisions
6. **Human override** - Rob can edit any agent output before using it
