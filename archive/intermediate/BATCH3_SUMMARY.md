# BATCH 3 EXTRACTION SUMMARY

**Source File:** /sessions/confident-laughing-ritchie/mnt/Work/prospect-outreach-3-2026-02-25.html
**Extraction Date:** 2026-02-27
**Total Prospects Extracted:** 25

## EXTRACTION RESULTS

### By Status
- **Skipped:** 1
- **Touch 1 Sent:** 24

### By Priority Score
- **Priority 3:** 16
- **Priority 4:** 9

### Complete Prospect List

| ID | Name | Company | Title | Email | Priority | Status |
|:--:|------|---------|-------|-------|:--------:|--------|
| 1 | Irfan Syed | Progress Software | Director of QA | isyed@progress.com | 3 | Touch 1 Sent |
| 2 | Katie Hotard | Lucid Software | Director of QA | katieb@lucid.co | 4 | Touch 1 Sent |
| 3 | Rachana Jagetia | Housecall Pro | Director, QA Eng | rachana.jagetia@housecallpro.com | 4 | Touch 1 Sent |
| 4 | Giang Hoang | Employee Navigator | Director of QA | ghoang@employeenavigator.com | 4 | Touch 1 Sent |
| 5 | Kevin Caulfield | Bottomline | Director of QA | kcaulfield@bottomline.com | 4 | Touch 1 Sent |
| 6 | Rick Kowaleski | Alteryx | Sr Principal SDET | rick.kowaleski@alteryx.com | 3 | Touch 1 Sent |
| 7 | Tyler Hackett | Ava Labs | QA Engineering Manager | tyler.hackett@avalabs.org | 3 | Touch 1 Sent |
| 8 | Abe Blanco | Kapitus | QA Engineering Manager | ablanco@kapitus.com | 3 | Touch 1 Sent |
| 9 | Susan Lin | Robinhood | Staff QA Engineer | susan.lin@robinhood.com | 3 | Touch 1 Sent |
| 10 | Aliaksei Ausianka | NerdWallet | Staff QA Engineer | aausianka@nerdwallet.com | 3 | Touch 1 Sent |
| 11 | Susan Cohan-Lendzian | BHG Financial | QA Engineering Manager | slendzian@bhg-inc.com | 3 | Touch 1 Sent |
| 12 | Jayati Srivastava | Cvent | Principal SDET | jsrivastava@cvent.com | 4 | Touch 1 Sent |
| 13 | Suraphel Amde | BILL | Staff QA Engineer | samdeberhan@hq.bill.com | 3 | Skipped |
| 14 | Steven Mays | Medallia | Staff QA Engineer | smays@medallia.com | 3 | Touch 1 Sent |
| 15 | Christopher Edwards | Tanium | Staff QA Engineer | chris.edwards@tanium.com | 3 | Touch 1 Sent |
| 16 | Max Iglehart | Amwell | Staff QA Engineer | max.iglehart@americanwell.com | 3 | Touch 1 Sent |
| 17 | Mazie Roxx | Phreesia | QA Director, Payments | mroxx@phreesia.com | 4 | Touch 1 Sent |
| 18 | Ram Bulusu | LiveRamp | Head of QA | ram.bulusu@liveramp.com | 4 | Touch 1 Sent |
| 19 | Dexter Alon | Blackhawk Network | Software QA Eng Manager | dexter.alon2@bhnetwork.com | 3 | Touch 1 Sent |
| 20 | Phil Jones | Litera | Director, Quality Engineering | phil.jones@litera.com | 4 | Touch 1 Sent |
| 21 | Sebastien Pambu | ecoATM Gazelle | Sr SDET / Test Architect | sebastien.pambu@ecoatm.com | 3 | Touch 1 Sent |
| 22 | Shanil Jain | Sling TV | PM & Test Architect | shanil.jain@dish.com | 3 | Touch 1 Sent |
| 23 | Andre Maestas | Unity | Sr SDET / XR QA Architect IC7 | andre.maestas@unity3d.com | 3 | Touch 1 Sent |
| 24 | Animesh Patcha | Arista Networks | Test Architect & Eng Manager | animesh.patcha@arista.com | 3 | Touch 1 Sent |
| 25 | Natalie Gitelman | Acentra Health | Test Architect, Sr Test Engineer | natalie.gitelman@cns-inc.com | 4 | Touch 1 Sent |

## DELIVERABLES CREATED

1. **batch3_extracted.json** - Machine-readable JSON format with all prospect data
2. **BATCH3_EXTRACTION_REPORT.md** - Comprehensive markdown report with all prospect cards and full message text
3. **BATCH3_SUMMARY.md** - This summary document

## DATA STRUCTURE

Each prospect record contains:
- **id, name, title, company** - Basic information
- **priority** - Priority score (1-5)
- **email** - Contact email address (when available)
- **status** - Current outreach status
- **linkedinUrl** - LinkedIn Sales Navigator profile URL
- **touch1** - InMail message (subject + body)
- **touch2** - InMail follow-up message (subject + body)
- **touch3** - Email message (subject + body)

## USAGE

To use this data for sending:
1. Open batch3_extracted.json in a text editor or JSON viewer
2. Copy the full message text from the `touch1.body`, `touch2.body`, or `touch3.body` fields
3. Paste into LinkedIn InMail or Gmail compose windows
4. Use the subject lines as provided in the subject fields

All messages have already been extracted in their exact form from the HTML tracker file.
