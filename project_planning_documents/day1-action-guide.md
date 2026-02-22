# Day 1 Action Guide v3.0
## Start Right Now — No GCP Project Creation Required

> Everything here uses either GitHub (free), your existing Google Workspace, or your terminal.
> Zero GCP infrastructure to create.

---

## Pre-Check (5 minutes)

Before starting, verify you have:
- [ ] GitHub account (personal)
- [ ] Node.js installed: `node --version` (need v18+; install from nodejs.org if missing)
- [ ] Python installed: `python3 --version` (need 3.9+)
- [ ] Git installed: `git --version`
- [ ] Your work Gemini API key (from console.cloud.google.com → APIs → Gemini → Credentials, OR your IT team)
- [ ] Your Gemini Enterprise access confirms Gemini 2.5 Pro is available

---

## Block 1 (60 min): GitHub Repository

### Step 1.1 — Create repo
1. Go to github.com → **New repository**
2. Name: `bd-content-platform`
3. Select: **Private**
4. Check: **Add a README file**
5. Click **Create repository**

### Step 1.2 — Clone and build structure
```bash
# Clone locally
git clone https://github.com/YOUR-USERNAME/bd-content-platform.git
cd bd-content-platform

# Create all folders
mkdir -p .github/workflows
mkdir -p config
mkdir -p prompts
mkdir -p scripts
mkdir -p topics
mkdir -p pipeline
mkdir -p published

# Add placeholder files so folders commit
touch config/.keep prompts/.keep scripts/.keep topics/.keep

# First commit
git add .
git commit -m "Initial folder structure"
git push origin main
```

### Step 1.3 — Install Gemini CLI
```bash
# Install globally
npm install -g @google/gemini-cli

# Verify installation
gemini --version

# Authenticate with your work Google account
gemini auth
# This opens a browser — sign in with your work account that has Gemini Enterprise
```

### Step 1.4 — Test Gemini CLI works
```bash
# Quick sanity check — should browse and return real data
gemini -p "Search the web and tell me Bangladesh's GDP in 2023 according to the World Bank. Return just the number."
```

If this works, you're ready. If it fails, check your Gemini Enterprise API access.

---

## Block 2 (45 min): GitHub Secrets

Go to your repo on GitHub → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these now (you'll fill in some values later today, placeholder is fine):

### Secret 1: GEMINI_API_KEY
- Get from: console.cloud.google.com → your company project → APIs & Services → Credentials → your Gemini API key
- OR from your IT team / internal docs
- Enter the key value

### Secret 2-3: Slack (set up Slack app first in Block 3, then come back)
- `SLACK_BOT_TOKEN` — placeholder: `xoxb-PLACEHOLDER`
- `SLACK_REVIEW_CHANNEL_ID` — placeholder: `CPLACEHOLDER`
- `SLACK_ERRORS_CHANNEL_ID` — placeholder: `CPLACEHOLDER`

### Secret 4-5: Instagram (set up in Block 4, then come back)
- `INSTAGRAM_ACCESS_TOKEN` — placeholder: `IGPLACEHOLDER`
- `INSTAGRAM_USER_ID` — placeholder: `IGPLACEHOLDER`

### Secret 6-8: Google Sheets (set up in Block 3, then come back)
- `GOOGLE_SHEETS_ID` — placeholder: `SHEETPLACEHOLDER`
- `GOOGLE_SERVICE_ACCOUNT_JSON` — placeholder: `{}`

---

## Block 3 (75 min): Google Sheets + Service Account

### Step 3.1 — Create the Spreadsheet
1. Go to sheets.google.com → **Blank spreadsheet**
2. Name it: **BD Content Platform**
3. Create 4 tabs (click `+` at bottom): `Content_Queue`, `Published_Log`, `Error_Log`, `Topic_Suggestions`

### Step 3.2 — Set up Content_Queue headers
Click the `Content_Queue` tab. Add these in Row 1, one per column:
```
A1: Topic_ID
B1: Topic_Bangla  
C1: Topic_English
D1: Priority
E1: Context_Notes
F1: Deadline
G1: Status
H1: Sensitivity
I1: Dry_Run
```

Bold Row 1, freeze it (View → Freeze → 1 row).

### Step 3.3 — Add your first test topic (Row 2)
```
A2: T001
B2: শিক্ষা খাতে বরাদ্দ তুলনা
C2: Education Budget Comparison
D2: High
E2: Compare 1996-2006 vs 2009-2024. Focus on education spending as % of GDP. Use UNESCO Institute for Statistics and Bangladesh Bureau of Statistics. Show primary enrollment rates alongside spending.
F2: 2026-03-01
G2: Approved
H2: FALSE
I2: TRUE
```

### Step 3.4 — Get the Sheet ID
Your Sheet URL looks like:
`https://docs.google.com/spreadsheets/d/`**`1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms`**`/edit`

The bold part is your Sheet ID. Copy it.

Update GitHub Secret `GOOGLE_SHEETS_ID` with this value.

### Step 3.5 — Create a service account for Sheets API access

> **Note:** You're NOT creating a new GCP project. You're adding a service account to your **existing** company project. This is a minor operation that most company GCP projects allow.

```
1. Go to: console.cloud.google.com
2. Select your existing company project from the dropdown
3. Go to: IAM & Admin → Service Accounts
4. Click: + CREATE SERVICE ACCOUNT
5. Name: bd-pipeline-sa
6. Description: BD Content Platform pipeline
7. Click Create and Continue
8. Skip "Grant this service account access to project" — click Continue
9. Skip "Grant users access" — click Done
```

If you don't have permission to create service accounts, ask your IT/GCP admin to create one for you and provide the JSON key. Alternatively, use the [OAuth Playground](https://developers.google.com/oauthplayground) to get user credentials temporarily.

### Step 3.6 — Download the JSON key
```
1. Click on the newly created bd-pipeline-sa service account
2. Go to Keys tab
3. Add Key → Create new key → JSON
4. Download the JSON file
```

### Step 3.7 — Share the Sheet with the service account
```
1. Open your BD Content Platform Sheet
2. Click Share
3. Paste the service account email (looks like: bd-pipeline-sa@YOUR-COMPANY-PROJECT.iam.gserviceaccount.com)
4. Set to Editor
5. Click Send
```

### Step 3.8 — Add the JSON to GitHub Secrets
```bash
# Base64 encode the JSON file
base64 -i ~/Downloads/bd-pipeline-sa-*.json | tr -d '\n'
# Copy the output
```

Go to GitHub Secrets → update `GOOGLE_SERVICE_ACCOUNT_JSON` with the base64 string.

---

## Block 4 (45 min): Slack Setup

### Step 4.1 — Create Slack App
1. Go to **api.slack.com/apps** → Create New App → From Scratch
2. App Name: `BD Pipeline Bot`
3. Select your Slack workspace
4. Click Create App

### Step 4.2 — Set permissions
1. Go to **OAuth & Permissions** (left sidebar)
2. Scroll to **Scopes** → **Bot Token Scopes** → Add:
   - `chat:write`
   - `files:upload`
3. Scroll up → Click **Install to Workspace** → Allow

### Step 4.3 — Get the bot token
After installing, you'll see **Bot User OAuth Token** (starts with `xoxb-`). Copy it.

Update GitHub Secret `SLACK_BOT_TOKEN` with this value.

### Step 4.4 — Create channels and get IDs
In Slack:
1. Create channel: `#bd-content-review`
2. Create channel: `#bd-pipeline-errors`
3. Invite the bot: in each channel, type `/invite @BD Pipeline Bot`

To get Channel IDs:
- Right-click on the channel name → View channel details → Scroll to bottom → Copy ID (starts with `C`)

Update GitHub Secrets `SLACK_REVIEW_CHANNEL_ID` and `SLACK_ERRORS_CHANNEL_ID`.

---

## Block 5 (30 min): Instagram API

### Step 5.1 — Prerequisites check
- You need a **Facebook Business account** (personal Facebook works if linked to a business)
- Your Instagram must be an **Instagram Business or Creator account** (not personal)
- To convert: Instagram app → Settings → Account → Switch to Professional Account

### Step 5.2 — Create Meta Developer App
1. Go to **developers.facebook.com** → My Apps → Create App
2. Select **Other** as use case, then **Business** as type
3. Name: `BD Content Platform`
4. Complete creation

### Step 5.3 — Add Instagram Graph API
1. In your app dashboard → Add Products → find **Instagram** → Set Up
2. Go to Instagram → API setup with Instagram Business Login

### Step 5.4 — Get your tokens
Use the [Graph API Explorer](https://developers.facebook.com/tools/explorer/):
1. Select your app
2. Request permissions: `instagram_basic`, `instagram_content_publish`
3. Generate Access Token
4. Exchange for long-lived token via: `https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-lived-token}`

Get your Instagram User ID:
```bash
curl "https://graph.facebook.com/v18.0/me?fields=id,name&access_token=YOUR_TOKEN"
# Returns your Facebook user ID
curl "https://graph.facebook.com/v18.0/YOUR_FB_ID/accounts?access_token=YOUR_TOKEN"
# Find the Instagram Business Account ID
```

Update GitHub Secrets: `INSTAGRAM_ACCESS_TOKEN` and `INSTAGRAM_USER_ID`.

---

## Block 6 (60 min): Begin Writing Style Profile

This is the highest-value work you'll do. Open your editor and start `config/writing_style_profile.md`.

Use this starter template — replace everything in `[brackets]` with your actual preferences:

```markdown
# Writing Style Profile

Last Updated: 2026-02-22
Author: [Your name]

---

## Core Voice

**Who am I writing as:**
[e.g., "A data analyst who grew up in Bangladesh and cares deeply about how government performance actually affected people's lives. Not a politician. Not an activist. Someone who reads BBS reports so their followers don't have to."]

**Tone:** [e.g., "Informative but conversational. Like explaining something interesting at a dhaba with friends. Smart but never condescending."]

**What I'm NOT:** [e.g., "Not a political commentator. Not cheerleading any party. Not writing academic papers."]

---

## Language Mix

| Content Element | Bangla | English | Rule |
|---|---|---|---|
| Post headline | 60% | 40% | Bangla first, English tech terms OK |
| Body narrative | 70% | 30% | Bangla for story, English for data terms |
| Numbers/statistics | — | 100% | Always Arabic numerals |
| Source attribution | 40% | 60% | "তথ্যসূত্র: World Bank" style |

---

## Vocabulary Rules

### Always use these Bangla words:
- "তথ্য" (not "ডেটা") for data
- "প্রবৃদ্ধি" (not "গ্রোথ") for growth  
- [Add 8 more terms you care about]

### Never use:
- Inflammatory political terms without data evidence
- "সেরা" or "worst" without comparative data
- Passive voice where active is clearer
- [Add 5 more banned patterns]

---

## Post Structure (always in this order)

1. **Headline** — question or surprising fact, <15 words
2. **Hook** — the most counterintuitive finding in the data
3. **Data comparison** — 3-5 bullet points, each with citation
4. **Context** — 1-2 sentences of historical framing
5. **Engagement question** — asks audience for their view
6. **Source line** — "তথ্যসূত্র: [Source 1], [Source 2]"
7. **Hashtags** — 3-5, last line

---

## Examples of Posts I Love (or have written)

### Example 1 — [Short description]
[PASTE FULL POST VERBATIM HERE — Bangla and English mix as it actually appears]

### Example 2 — [Short description]
[PASTE FULL POST VERBATIM HERE]

### Example 3 — [Short description]
[PASTE FULL POST VERBATIM HERE]
```

Save the file. Commit what you have, even if incomplete:
```bash
cd bd-content-platform
git add config/writing_style_profile.md
git commit -m "Add writing style profile (WIP)"
git push
```

---

## ✅ End-of-Day Verification

Run through this checklist before ending:

**GitHub:**
- [ ] Repo exists and is private: `github.com/YOUR-USERNAME/bd-content-platform`
- [ ] All folders exist: config/, prompts/, scripts/, topics/, pipeline/, .github/workflows/
- [ ] Gemini CLI installed locally: `gemini --version` works
- [ ] `gemini auth` authenticated with work account

**Secrets (go to repo Settings → Secrets → Actions):**
- [ ] `GEMINI_API_KEY` — real value ✅
- [ ] `GOOGLE_SHEETS_ID` — real value ✅
- [ ] `GOOGLE_SERVICE_ACCOUNT_JSON` — real value (base64 JSON) ✅
- [ ] `SLACK_BOT_TOKEN` — real value ✅
- [ ] `SLACK_REVIEW_CHANNEL_ID` — real value ✅
- [ ] `SLACK_ERRORS_CHANNEL_ID` — real value ✅
- [ ] `INSTAGRAM_ACCESS_TOKEN` — real value ✅ (or placeholder if still setting up)
- [ ] `INSTAGRAM_USER_ID` — real value ✅ (or placeholder)

**Google Sheets:**
- [ ] "BD Content Platform" sheet exists with 4 tabs
- [ ] Content_Queue has headers in Row 1
- [ ] T001 test topic in Row 2 with Status=Approved, Dry_Run=TRUE
- [ ] Shared with service account email (Editor access)

**Slack:**
- [ ] `#bd-content-review` and `#bd-pipeline-errors` channels exist
- [ ] BD Pipeline Bot is in both channels (test: type `/invite @BD Pipeline Bot`)

**Config files:**
- [ ] `config/writing_style_profile.md` exists (even if WIP)
- [ ] Committed and pushed to GitHub

**Quick Gemini CLI test:**
```bash
cd bd-content-platform
gemini -p "Read this file and tell me the top 3 vocabulary rules: $(cat config/writing_style_profile.md)"
```
If Gemini can read your file and respond — everything is working.

---

## 📅 Day 2 Preview

**Morning (2 hours):**
Complete the remaining 4 config files:
- `config/editorial_preferences.md`
- `config/visual_identity.md`
- `config/source_priority.md`
- `config/fact_check_protocols.md`

**Afternoon (2 hours):**
Write the 5 prompt files in `prompts/` directory — start with `prompts/01_research.md`.

**Evening (1 hour):**
Run your first local Gemini CLI research stage on T001 and review the output.

By end of Day 2: configs complete, research prompt working, first research output generated.