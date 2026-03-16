================================================================================
BATCH 5A EXTRACTION - COMPLETE DATA PACKAGE
================================================================================

OVERVIEW
========

Batch 5A is a 25-prospect FinServ/Insurance outreach batch with complete 3-touch
sequences ready for copy-paste sending. All messages have been extracted from
the original HTML tracker and are ready to use without any editing.

Source File: prospect-outreach-5a-2026-02-26.html
Extraction Date: 2026-02-27
Total Prospects: 25 (3 Hot, 10 Warm, 12 Standard)
Email Status: 0/25 have verified emails (prospects will receive Email on Day 10 via alternative methods)
Message Quality: All 25/25 messages pass QA gate (MQS 9-10/12)

================================================================================
DELIVERABLES (4 Files)
================================================================================

1. batch_5a_prospects.json (43 KB)
   - Structured JSON with complete prospect data
   - Includes: names, titles, companies, priorities, LinkedIn URLs
   - Contains: All 3 message touches (subject + body) for each prospect
   - Best for: Programmatic use, automation, integration with tools
   - Format: Standard JSON array of prospect objects

2. BATCH_5A_PROSPECTS.csv (36 KB)
   - Spreadsheet-friendly CSV export
   - Includes: All prospect data + messages in tabular format
   - Best for: Excel/Google Sheets use, data analysis, filtering/sorting
   - Format: One row per prospect with 15 columns

3. BATCH_5A_EXTRACTION.md (49 KB)
   - Markdown document with full prospect details
   - Includes: Summary table + detailed cards for all 25 prospects
   - Shows: Complete message text for each touch
   - Best for: Reading in GitHub, documentation, reference guide
   - Format: Markdown with code blocks for messages

4. BATCH_5A_QUICK_REFERENCE.txt (6.3 KB)
   - Executive summary and copy-paste workflow guide
   - Includes: Prospect selection cheat sheet, step-by-step send workflow
   - Shows: Example complete prospect (Pam Bice @ Bread Financial)
   - Best for: Quick lookups, workflow reference, new user onboarding
   - Format: Plain text with sections and examples

(This file) BATCH_5A_README.txt
   - Index and guide to all deliverables
   - Includes: How to use each file, data format guide
   - Best for: Understanding what you have, which file to use when
   - Format: Plain text documentation

Also created:
   BATCH_5A_EXTRACTION_REPORT.txt - Technical extraction summary and statistics

================================================================================
QUICK START
================================================================================

IF YOU WANT TO...                           USE THIS FILE...
Send InMails right now                      BATCH_5A_QUICK_REFERENCE.txt
Sort/filter prospects in Excel              BATCH_5A_PROSPECTS.csv
Read full details about all prospects       BATCH_5A_EXTRACTION.md
Use with programming/automation             batch_5a_prospects.json
See data statistics                         BATCH_5A_EXTRACTION_REPORT.txt

================================================================================
DATA STRUCTURE GUIDE
================================================================================

PROSPECT OBJECT (all formats):

{
  "index": 1,                          # Prospect number (1-25)
  "name": "Pam Bice",                  # Full name
  "title": "Director of Quality Assurance",
  "company": "Bread Financial",
  "priority_score": 5,                 # 3-5 (5 = highest)
  "ab_group": "a",                     # A/B test group
  "status": "not_started",             # Initial status
  "linkedin_url": "http://...",        # Direct LinkedIn profile link
  "email": null,                       # null = not available
  
  "touch1_subject": "Lending QA strategy",
  "touch1_body": "Hey Pam,\n\nWhat's harder...",
  
  "touch2_subject": "Quick follow-up",
  "touch2_body": "Hey Pam,\n\nCircling back...",
  
  "touch3_subject": "Lending test automation",
  "touch3_body": "Hey Pam,\n\nConsumer lending..."
}

================================================================================
HOW TO USE (For Sending)
================================================================================

WORKFLOW: Select prospect → Copy message → Paste into LinkedIn → Send manually

STEP 1: Choose a prospect
   - Pick one from the "Hot" list (Priority 5) if starting today
   - Or pick one from "Warm" list (Priority 4) for high likelihood
   
STEP 2: Find their profile
   - Copy their LinkedIn URL from any of the data files
   - Open the URL in LinkedIn Sales Navigator
   
STEP 3: Start InMail
   - Click the "Message" button on their profile
   - Wait for InMail composer to load
   
STEP 4: Copy message text
   - Open batch_5a_prospects.json (or CSV / MD file)
   - Find the prospect by name
   - Copy the Touch 1 subject line
   - Copy the Touch 1 message body
   
STEP 5: Paste into InMail
   - Paste subject in the Subject field
   - Paste body in the message box
   - Review for any formatting issues
   
STEP 6: Submit for approval
   - Show the composed message to Rob
   - Wait for "APPROVE SEND" confirmation
   
STEP 7: Rob sends manually
   - Rob reviews the message
   - Rob clicks Send button
   - Claude logs the send to the HTML tracker
   
STEP 8: Wait 5 days, repeat for Touch 2
   - Use Touch 2 message (InMail follow-up)
   - Same LinkedIn channel
   
STEP 9: Wait 5 more days, send Touch 3
   - Use Touch 3 message (Email)
   - Send via Gmail or Apollo (since no email addresses are enriched)
   - Or call if they've replied by then

================================================================================
PROSPECT PRIORITY LEVELS
================================================================================

PRIORITY 5 (HOT - 3 prospects)
- Best signal, highest conversion likelihood
- Send first, give them priority
- Prospects:
  1. Pam Bice @ Bread Financial
  2. Kerri McGee @ Sapiens
  3. Cindy Holsinger @ Early Warning

PRIORITY 4 (WARM - 10 prospects)
- Strong signal, good conversion likelihood
- Send second in batch
- Includes: Directors of QA with strong fit signals

PRIORITY 3 (STANDARD - 12 prospects)
- Solid ICP fit, standard conversion likelihood
- Fill out the queue after priorities 5 and 4
- Lower signal but still qualified

================================================================================
MESSAGE QUALITY METRICS
================================================================================

All 25 messages have been graded and verified:

MQS (Message Quality Score): 9-10/12 for all prospects
- MQS 10/12: 12 prospects (highest quality)
- MQS 9/12: 13 prospects (excellent quality)
- MQS < 9/12: NONE (all messages passed QA threshold)

QA Gate: 100% pass rate (25/25 prospects)
- All 14 mandatory checks passed
- No editing needed before sending
- Use messages exactly as written

Expected Reply Rates (based on historical data):
- This batch (FinServ/Insurance): 28-40% likely
- General baseline: 28.7%
- FinServ bonus: +5-10% above baseline (strong vertical)
- Expected replies: 7-10 people per 25

================================================================================
A/B TEST INFORMATION
================================================================================

Variable Being Tested: Proof Point Style
- Group A (13 prospects): Named customer stories (Hansard, CRED, Sanofi, Medibuddy)
- Group B (12 prospects): Anonymous/other customer stories (one analytics platform, etc.)

Purpose: Determine if named brand names in proof points convert better than anonymous

How to read results:
- Track reply rate separately for Group A vs Group B
- Compare in next batch analysis
- Adjust message strategy based on winner

Group assignments in data:
- "ab_group": "a" → Group A (named customers)
- "ab_group": "b" → Group B (anonymous/other)

================================================================================
EMAIL ADDRESSES
================================================================================

IMPORTANT: No email addresses were enriched for this batch

Email status: 0/25 have verified emails in Apollo enrichment

For Touch 3 (Day 10), you have options:
1. Skip email, call instead (recommended for warm batch)
2. Find emails manually via LinkedIn, company directory
3. Use email finder tool if available
4. Send via InMail Thread (convert to email in the conversation)

Since 53.7% of replies come by Touch 2 (Day 5), you'll likely have
a positive response by the time Day 10 email is needed.

================================================================================
TRACKING & STATUS UPDATES
================================================================================

Once you send messages, track status in the HTML file:

Status Options:
- not_started → Touch1_sent → Touch2_sent → Touch3_sent → Replied → Meeting_booked
- not_interested → do not contact again
- bounced → invalid profile/no access
- dormant → no reply after all touches, eligible for re-engagement after 60 days

Reply Tags (when they respond):
- opener → They referenced the opening question
- pain_hook → They said "yes, that's our exact problem"
- proof_point → They asked about the customer story
- timing → They said "good timing, we're evaluating"
- referral → They said "talk to [name]"
- not_interested → They declined
- unknown → Can't tell what triggered the reply

All tracking fields are in the original prospect-outreach-5a-2026-02-26.html file.

================================================================================
TROUBLESHOOTING
================================================================================

"Where's the email address?"
→ Not enriched. Use LinkedIn direct message or find email separately.

"Can I edit the messages?"
→ No. All messages passed QA gate. Use exactly as written for best results.

"What if LinkedIn blocks me?"
→ This is unlikely if you stay within pacing limits (max 25/day, max 15/week).
  Contact Rob if you get account warnings.

"How do I know if my send worked?"
→ LinkedIn shows "Conversation started" or "Sent" confirmation.
  Update the status in the HTML tracker to "Touch1_sent" after you send.

"What if they don't reply?"
→ Totally normal. 71% don't reply to Touch 1 alone.
  Send Touch 2 on Day 5. 53.7% reply by Touch 2.
  Send Touch 3 on Day 10. Additional 31.1% reply after 3+ touches.

"Can I send to multiple people same day?"
→ Yes, but space them out. Send 1-2 per hour minimum.
  Max 25 per day, 20 per week safe pace.

"Should I call anyone?"
→ Only after they reply and agree to a call.
  Never cold call - it violates the BDR SOP.

================================================================================
FILES AT A GLANCE
================================================================================

Absolute Paths (in /sessions/confident-laughing-ritchie/mnt/Work/):

1. batch_5a_prospects.json               [JSON structured data]
2. BATCH_5A_PROSPECTS.csv                [Spreadsheet format]
3. BATCH_5A_EXTRACTION.md                [Markdown documentation]
4. BATCH_5A_QUICK_REFERENCE.txt          [Quick start guide]
5. BATCH_5A_EXTRACTION_REPORT.txt        [Statistics & metrics]
6. BATCH_5A_README.txt                   [This file]

All files are in the Work folder where Rob can find them.

================================================================================
SUCCESS CRITERIA
================================================================================

For this 25-person batch, realistic targets (based on historical data):

Minimum (conservative): 5-6 replies (20-24% rate)
Expected (realistic): 7-10 replies (28-40% rate, high for FinServ)
Stretch goal: 12+ replies (48%+ rate, requires perfect execution)

Positive replies (actual interest): 2-3 people
Meeting bookings: 1-2 people

If you hit expected replies, this batch is a success.

================================================================================
QUESTIONS?
================================================================================

For how to use this data: See BATCH_5A_QUICK_REFERENCE.txt
For message details: See BATCH_5A_EXTRACTION.md
For statistics: See BATCH_5A_EXTRACTION_REPORT.txt
For all data: See batch_5a_prospects.json

All files are ready to use. No further processing needed.

================================================================================
