# Objection Handling

## Pre-Mapping (per prospect)

Based on company research, predict the most likely objection and pre-load the response in the tracker.

| Research Signal | Likely Objection | Pre-loaded Response |
|----------------|-----------------|-------------------|
| Uses TOSCA, Katalon, Testim, or mabl | "We already have a tool" | "Totally fair. A lot of teams we work with had [tool] too. The gap they kept hitting was [specific limitation]. Worth comparing?" |
| 50K+ employee company | "Security/procurement is complex" | "We offer on-prem, private cloud, and hybrid. SOC2/ISO certified. A few Fortune 500s run us behind their firewall." |
| No dedicated QA team visible | "QA isn't a priority" | "That's actually why teams like yours use us. Plain English means devs write tests without a dedicated QA team." |
| Recently hired QA leader | "Too early, still assessing" | "Makes sense. A lot of QA leaders in their first 90 days use our free trial to benchmark what's possible before committing." |
| Pharma/healthcare/finance | "Compliance requirements" | "We work with Sanofi, Oscar Health, and several banks. Happy to walk through our compliance story." |
| Startup/small team (<200 employees) | "Budget is tight" | "Totally get it. One company your size (Spendflo) cut manual testing 50% and saw ROI in the first quarter." |

**Rules:**
- Assign ONE predicted objection per prospect (the most likely one based on research).
- If no clear signal, default to "We already have a tool" since that's the most common objection.

## Reply Patterns (from 384 analyzed replies)

| Type | % of Replies | Action |
|------|-------------|--------|
| Polite ("thanks") | 37.9% | Follow up with value. Not commitment. |
| Positive ("interested") | 22.8% | Book meeting immediately. Don't over-explain. |
| Negative ("not interested") | 9.4% | Log objection. May re-engage 60+ days. |
| Curiosity ("how", "tell me more") | 8.3% | Answer directly, then bridge to meeting. |
| Referral ("talk to [name]") | 7.4% | High value. Reach out to referred person immediately. |
| Has tool ("we use [X]") | 2.3% | Objection handle: ask about gaps. |
| Timing ("not right now") | 2.1% | Set calendar reminder. Re-engage per triggers. |

## Reply Tagging

When a prospect replies, Rob tags WHAT triggered the reply:
- **Opener** - Reacted to the personalized opener
- **Pain hook** - Engaged with the problem hypothesis
- **Proof point** - Asked about the customer story or numbers
- **Timing** - Said "good timing" or "we're evaluating"
- **Referral** - Forwarded to someone else
- **Not interested** - Replied but declined (still useful data)
- **Unknown** - Can't tell what triggered it

Even negative replies are data. "Not interested" with a reason tells us the pain hook missed. "Talk to [name]" tells us we hit the right company but wrong person.
