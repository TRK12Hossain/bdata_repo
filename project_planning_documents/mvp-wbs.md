# Bangladesh Content Platform — Revised MVP v3.0
## Work Breakdown Structure

> **Version 3.0 changes:** Gemini CLI as agent engine · GitHub Actions as orchestration · Zero GCP infrastructure · GitHub personal repo for version control
> **Target:** 1 verified post/day · <15 min human time · ~$0/month

---

## 🔄 Architecture Reset: What This Version Changes

### The Three Constraints and Their Implications

| Constraint | Old Approach | New Approach | Impact |
|---|---|---|---|
| Maximize Gemini CLI | Write Python agent code manually | Write **prompt files** — Gemini CLI does everything else | Eliminates ~14hrs of Python coding |
| GitHub personal repo | GCS bucket versioning | GitHub = version control + storage + CI/CD | One ecosystem, free, familiar |
| Cannot create GCP project | Cloud Run + Cloud Scheduler + Cloud Functions | **GitHub Actions** (free compute, no GCP needed) | Zero infrastructure to provision |

### What Just Disappeared from the Stack

- ❌ Digital Ocean / Cloud Run / any VM
- ❌ Cloud Scheduler
- ❌ Cloud Functions
- ❌ GCS buckets (custom)
- ❌ Secret Manager
- ❌ Docker / containerization
- ❌ Writing Python agent code yourself
- ❌ MCP servers
- ❌ CrewAI / LiteLLM / Python orchestration framework

### What Remains

- ✅ Gemini CLI (agent engine — does research, writes content, generates chart code)
- ✅ GitHub Actions (scheduler + compute — runs the pipeline)
- ✅ GitHub personal repo (version control + pipeline file storage)
- ✅ GitHub Secrets (API key management)
- ✅ Google Sheets (topic queue, publication log — Workspace, no new project)
- ✅ Google Drive (visual asset archive — Workspace, no new project)
- ✅ Slack (human review interface)
- ✅ Gemini 2.5 Pro API via work (AI engine — free)
- ✅ Instagram Graph API (publishing)

---

## 🧠 How Gemini CLI Changes Your Role

**Before (v1 & v2):** You are a developer writing Python classes, configuring Docker, managing servers.

**After (v3):** You are an **editorial director** writing prompt files in plain English/Markdown. Gemini CLI is your employee that reads those files and does the work.

```
YOU WRITE:                          GEMINI CLI DOES:
─────────────────                   ──────────────────────────────────
prompts/01_research.md    →         Browses BBS, World Bank, UNESCO
prompts/02_write.md       →         Writes bilingual Bangla-English content
prompts/03_factcheck.md   →         Fetches source URLs, verifies claims
prompts/04_stylecheck.md  →         Scores draft against your style guide
prompts/05_visual.md      →         Writes Python code, generates PNG chart
scripts/setup.md          →         Writes all the glue scripts (notify Slack, post to IG, etc.)
```

You write Markdown. Gemini CLI writes code.

---

## 🏗️ Complete Architecture

```
┌─────────────────────────────────────────────────────┐
│  HUMAN LAYER                                         │
│  Google Sheets → add topics, review published log   │
│  Slack → receive review package, click Approve       │
│  GitHub → edit config/prompt files, view pipeline   │
└──────────────────────────┬──────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────┐
│  ORCHESTRATION LAYER: GitHub Actions                 │
│  • Cron scheduler (Mon 9am Bangladesh time)          │
│  • Manual trigger (workflow_dispatch)                │
│  • Reads topic from Google Sheets                    │
│  • Runs each Gemini CLI stage in sequence            │
│  • Commits pipeline outputs to repo                  │
│  • Sends Slack notifications                         │
│  • Handles errors and retries                        │
└──────────────────────────┬──────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────┐
│  AI LAYER: Gemini CLI + Gemini 2.5 Pro              │
│  Stage 1: Research Agent (browses web, reads PDFs)   │
│  Stage 2: Content Writer (bilingual, style-aware)    │
│  Stage 3: Fact-Checker (verifies every claim)        │
│  Stage 4: Style Checker (scores vs style guide)      │
│  Stage 5: Visual Designer (writes + runs Python)     │
└──────────────────────────┬──────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────┐
│  STORAGE LAYER: GitHub repo                          │
│  config/     → your Markdown config files           │
│  prompts/    → Gemini CLI instruction files         │
│  scripts/    → Gemini-generated helper scripts      │
│  pipeline/   → per-topic MD outputs + PNG           │
│  published/  → archive of approved content          │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
bd-content-platform/  (private GitHub personal repo)
│
├── .github/
│   └── workflows/
│       ├── content-pipeline.yml      # Main pipeline (daily trigger)
│       ├── topic-suggester.yml       # Weekly idea generation (Mon)
│       └── health-check.yml         # Daily API health ping
│
├── config/                           # YOU write these — Gemini CLI reads them
│   ├── writing_style_profile.md      # Your voice, tone, examples
│   ├── editorial_preferences.md      # Topic rules, banned topics
│   ├── visual_identity.md            # Colors, fonts, templates
│   ├── source_priority.md            # Tier 1/2/3 sources with URLs
│   └── fact_check_protocols.md       # Verification rules
│
├── prompts/                          # YOU write these — Gemini CLI executes them
│   ├── 01_research.md               # Research agent instructions
│   ├── 02_write.md                  # Content writer instructions
│   ├── 03_factcheck.md              # Fact-checker instructions
│   ├── 04_stylecheck.md             # Style checker instructions
│   └── 05_visual.md                 # Visual designer instructions
│
├── scripts/                          # GEMINI CLI writes these (you prompt it once)
│   ├── get_next_topic.py             # Reads Google Sheets, gets next approved topic
│   ├── gate_check.py                 # Evaluates quality gate pass/fail
│   ├── notify_slack.py               # Sends review package to Slack
│   ├── publish_instagram.py          # Posts approved content to Instagram
│   ├── run_visual.py                 # Executes Gemini-generated chart code
│   └── update_sheets.py              # Updates topic status + logs publication
│
├── topics/                           # One file per approved topic
│   └── T001.md                      # Topic brief (created from Sheets data)
│
├── pipeline/                         # Pipeline outputs (auto-committed per run)
│   └── T001/
│       ├── research.md
│       ├── draft.md
│       ├── factcheck.md
│       ├── stylecheck.md
│       ├── visual_report.md
│       ├── chart_code.py             # Gemini-generated Matplotlib code
│       └── instagram.png             # Generated chart (committed to repo)
│
└── published/                        # Approved + published content archive
    └── T001/
        ├── final_caption.md
        └── metadata.md
```

---

## 📋 WORK BREAKDOWN STRUCTURE

---

## PHASE 0 — Accounts & Foundations (2.5 hours)

### 0.1 GitHub Repository
- [ ] **0.1.1** Create private GitHub repo: `bd-content-platform`
- [ ] **0.1.2** Clone locally: `git clone https://github.com/YOUR-USERNAME/bd-content-platform`
- [ ] **0.1.3** Create folder structure:
  ```bash
  mkdir -p .github/workflows config prompts scripts topics pipeline published
  touch .github/workflows/.keep config/.keep prompts/.keep scripts/.keep
  git add . && git commit -m "Initial structure" && git push
  ```
- [ ] **0.1.4** Enable branch protection on `main` (Settings → Branches → Add rule → require PR for pushes) — optional but good practice

### 0.2 GitHub Secrets
Go to repo → Settings → Secrets and variables → Actions → New repository secret

- [ ] **0.2.1** `GEMINI_API_KEY` — your work Gemini Enterprise API key
- [ ] **0.2.2** `SLACK_BOT_TOKEN` — from Slack app (set up in 0.4)
- [ ] **0.2.3** `SLACK_REVIEW_CHANNEL_ID` — Slack channel for review notifications
- [ ] **0.2.4** `SLACK_ERRORS_CHANNEL_ID` — Slack channel for errors
- [ ] **0.2.5** `INSTAGRAM_ACCESS_TOKEN` — long-lived token (set up in 0.5)
- [ ] **0.2.6** `INSTAGRAM_USER_ID` — your Instagram Business account ID
- [ ] **0.2.7** `GOOGLE_SHEETS_ID` — the ID from your Sheets URL
- [ ] **0.2.8** `GOOGLE_SERVICE_ACCOUNT_JSON` — service account credentials for Sheets API access (see 0.3)

### 0.3 Google Sheets + Service Account
- [ ] **0.3.1** Create Google Sheets file: **"BD Content Platform"**
- [ ] **0.3.2** Create 4 tabs: `Content_Queue`, `Published_Log`, `Error_Log`, `Topic_Suggestions`
- [ ] **0.3.3** Set up `Content_Queue` headers (Row 1):
  ```
  A: Topic_ID | B: Topic_Bangla | C: Topic_English | D: Priority | 
  E: Context_Notes | F: Deadline | G: Status | H: Sensitivity | I: Dry_Run
  ```
- [ ] **0.3.4** Add your first test topic in Row 2 with `Status = Approved`, `Dry_Run = TRUE`
- [ ] **0.3.5** To access Sheets from GitHub Actions, you need a service account. Use your **existing company GCP project** — just create a service account within it (this doesn't require creating a new project):
  ```
  GCP Console → existing project → IAM & Admin → Service Accounts → Create
  Name: bd-pipeline-sa
  Role: none needed at project level
  ```
- [ ] **0.3.6** Download the service account JSON key
- [ ] **0.3.7** Share the Google Sheet with the service account email (Editor access)
- [ ] **0.3.8** Base64-encode the JSON and store in GitHub Secrets as `GOOGLE_SERVICE_ACCOUNT_JSON`

### 0.4 Slack Setup
- [ ] **0.4.1** Go to **api.slack.com/apps** → Create App → From Scratch → name: `BD Pipeline Bot`
- [ ] **0.4.2** OAuth & Permissions → Bot Token Scopes: `chat:write`, `files:upload`
- [ ] **0.4.3** Interactivity & Shortcuts → Enable → set Request URL to: (GitHub Actions webhook URL — fill in Phase 3)
- [ ] **0.4.4** Install to Workspace → copy Bot User OAuth Token
- [ ] **0.4.5** Create channels: `#bd-content-review` and `#bd-pipeline-errors`, invite bot to both

### 0.5 Instagram API
- [ ] **0.5.1** Ensure you have a Facebook Business account linked to your Instagram
- [ ] **0.5.2** Go to **developers.facebook.com** → My Apps → Create App → Business type
- [ ] **0.5.3** Add product: Instagram Graph API
- [ ] **0.5.4** Generate a long-lived access token (valid 60 days)
- [ ] **0.5.5** Note your Instagram User ID (from Graph API Explorer: `me?fields=id,name`)
- [ ] **0.5.6** Set a calendar reminder for day 50 to refresh the token

### 0.6 Gemini CLI Local Setup
*(For local development and writing/testing prompt files)*
- [ ] **0.6.1** Install Node.js if not installed: `https://nodejs.org`
- [ ] **0.6.2** Install Gemini CLI: `npm install -g @google/gemini-cli`
- [ ] **0.6.3** Authenticate: `gemini auth` (use your work Google account with Gemini Enterprise)
- [ ] **0.6.4** Test it works: `gemini -p "What is the GDP of Bangladesh in 2023? Search the web."` — it should browse and respond

**Phase 0 Total: ~2.5 hours**

---

## PHASE 1 — Config Files: Your Brand's DNA (4 hours)
*These are Markdown files you write. Gemini CLI reads them as context for every task.*

### 1.1 `config/writing_style_profile.md`
This is the most important file. Spend real time on it.

- [ ] **1.1.1** Voice section: Describe your tone in concrete terms. Don't say "professional" — say "like a knowledgeable friend who reads BBS reports so you don't have to"
- [ ] **1.1.2** Language rules table: specify Bangla/English % per element (headline, body, numbers, source lines)
- [ ] **1.1.3** Vocabulary rules: 10+ "always use" terms in Bangla, 10+ "never use" terms. Be specific.
- [ ] **1.1.4** Post structure rules: exact order of elements (hook → data → context → question → source)
- [ ] **1.1.5** Paste **at least 3 full example posts verbatim** that represent your ideal style. This is how Gemini calibrates.
- [ ] **1.1.6** Commit: `git add config/writing_style_profile.md && git commit -m "Add writing style profile"`

### 1.2 `config/editorial_preferences.md`
- [ ] **1.2.1** Content philosophy statement (objective, data-first, neutral)
- [ ] **1.2.2** Priority topic list ranked (economic → education → infrastructure → healthcare)
- [ ] **1.2.3** Banned topics and sensitivity flags (active court cases, religious controversies, etc.)
- [ ] **1.2.4** Government period comparison rules (which eras, how to frame comparisons neutrally)
- [ ] **1.2.5** International comparison lens (which peer countries to reference for context)
- [ ] **1.2.6** Commit: `git add config/editorial_preferences.md && git commit -m "Add editorial preferences"`

### 1.3 `config/visual_identity.md`
- [ ] **1.3.1** Color palette: name, hex, and explicit usage rule per color (minimum 3 colors)
- [ ] **1.3.2** Typography: Bangla font name + English font name + sizes per use case
- [ ] **1.3.3** Template decision table: "if data is X type → use Y chart type"
- [ ] **1.3.4** Mandatory elements for every visual: watermark handle, source line, dimensions
- [ ] **1.3.5** Things to NEVER do visually: cherry-picked Y-axis, misleading scales, etc.
- [ ] **1.3.6** Commit: `git add config/visual_identity.md && git commit -m "Add visual identity"`

### 1.4 `config/source_priority.md`
- [ ] **1.4.1** Tier 1: BBS, Bangladesh Bank, Ministry of Finance — include exact URL patterns for data portals
- [ ] **1.4.2** Tier 2: World Bank, IMF, UNESCO, ADB — include API endpoints where they exist
- [ ] **1.4.3** Tier 3: Daily Star, Prothom Alo data journalism — context only, never primary citation
- [ ] **1.4.4** Tier 4 blacklist with explicit reasoning
- [ ] **1.4.5** Fallback chain: "If BBS unavailable → try World Bank → if both fail → flag for human"
- [ ] **1.4.6** Commit: `git add config/source_priority.md && git commit -m "Add source priority"`

### 1.5 `config/fact_check_protocols.md`
- [ ] **1.5.1** Confidence levels: `exact_match`, `within_rounding`, `plausible_interpolated`, `unverifiable`, `mismatch`
- [ ] **1.5.2** Rounding tolerance: define when rounding is OK (2.09% → "approximately 2.1%")
- [ ] **1.5.3** Broken URL protocol: try Wayback Machine → try Tier 2 alternative → flag if all fail
- [ ] **1.5.4** Interpolation rules: when is historical data interpolation acceptable and how to label it
- [ ] **1.5.5** Auto-correction rules: what can be fixed without human review vs. what must escalate
- [ ] **1.5.6** Commit: `git add config/fact_check_protocols.md && git commit -m "Add fact check protocols"`

**Phase 1 Total: ~4 hours**

---

## PHASE 2 — Prompt Files: Gemini CLI's Instructions (3 hours)
*You write these in Markdown. GitHub Actions passes them to Gemini CLI as its task. Think of these as job descriptions for an AI employee.*

### 2.1 `prompts/01_research.md`

This prompt tells Gemini CLI how to research any Bangladesh data topic. It should include:

- [ ] **2.1.1** Role and goal statement
- [ ] **2.1.2** Instruction to read: `config/source_priority.md`, `config/editorial_preferences.md`, and the topic brief at `topics/{TOPIC_ID}.md`
- [ ] **2.1.3** Step-by-step research process (search → Tier 1 sources → cross-reference → extract data points)
- [ ] **2.1.4** Exact output format: every data point needs value, unit, year, source name, source URL, confidence level, methodology note
- [ ] **2.1.5** Self-assessment checklist Gemini CLI must complete before finishing
- [ ] **2.1.6** Gate 1 declaration: "End your output with GATE_1: PASS or GATE_1: FAIL with reason"

### 2.2 `prompts/02_write.md`

- [ ] **2.2.1** Role: bilingual content writer for Bangladesh political data
- [ ] **2.2.2** Instruction to read: `pipeline/{TOPIC_ID}/research.md`, `config/writing_style_profile.md`
- [ ] **2.2.3** Output format specification: Instagram caption section (with character count), then Facebook post section, then Bangla-English ratio self-assessment
- [ ] **2.2.4** Hard rules from style guide restated inline (Gemini must follow these non-negotiably)
- [ ] **2.2.5** Self-review step: after writing, check against each vocabulary rule

### 2.3 `prompts/03_factcheck.md`

- [ ] **2.3.1** Role: skeptical fact verifier — trust nothing, verify everything
- [ ] **2.3.2** Instruction to read: `pipeline/{TOPIC_ID}/draft.md`, `pipeline/{TOPIC_ID}/research.md`, `config/fact_check_protocols.md`
- [ ] **2.3.3** Process: extract all numerical claims → fetch each source URL → compare → classify
- [ ] **2.3.4** Output format: per-claim results table, then overall pass rate, then Gate 2 declaration
- [ ] **2.3.5** Auto-correction section: for `within_rounding` cases, write the corrected version

### 2.4 `prompts/04_stylecheck.md`

- [ ] **2.4.1** Role: quality control editor who knows the platform voice cold
- [ ] **2.4.2** Instruction to read: `pipeline/{TOPIC_ID}/draft.md`, `config/writing_style_profile.md`
- [ ] **2.4.3** Scoring rubric: 8 dimensions with weights (total = 100)
- [ ] **2.4.4** Output format: dimension scores table, deviations list with line references, overall score, Gate 3 declaration
- [ ] **2.4.5** If score 80-84: also output a corrected version of the draft with deviations fixed

### 2.5 `prompts/05_visual.md`

- [ ] **2.5.1** Role: data visualization designer — honest, on-brand, accessible
- [ ] **2.5.2** Instruction to read: `pipeline/{TOPIC_ID}/research.md`, `config/visual_identity.md`
- [ ] **2.5.3** Chart type decision logic: temporal data → line chart, comparison → bar, single stat → data card
- [ ] **2.5.4** **Critical instruction:** "Write a complete, self-contained Python script using only `matplotlib`, `PIL`, and `requests` (standard libraries available in GitHub Actions). The script must save its output to `pipeline/{TOPIC_ID}/instagram.png` (1080x1080px, 100dpi) and `pipeline/{TOPIC_ID}/facebook.png` (1200x630px). Include all brand colors and fonts from the visual identity config inline in the script."
- [ ] **2.5.5** Mandatory elements checklist: source watermark, handle watermark, Bangla labels
- [ ] **2.5.6** Gate 4 declaration after script

**Phase 2 Total: ~3 hours**

---

## PHASE 3 — Scripts via Gemini CLI (2 hours)
*You DON'T write these. You ask Gemini CLI to write them. Do this locally in your repo folder.*

### 3.1 Generate Helper Scripts
Run these Gemini CLI commands locally from your repo root. Review each output before committing.

- [ ] **3.1.1** Generate `scripts/get_next_topic.py`:
  ```bash
  gemini -p "Write a Python script called get_next_topic.py that:
  1. Reads Google Sheets using the google-auth and gspread libraries
  2. Credentials come from env var GOOGLE_SERVICE_ACCOUNT_JSON (base64 encoded JSON)
  3. Sheet ID comes from env var GOOGLE_SHEETS_ID
  4. Finds the first row in Content_Queue tab where Status='Approved'
  5. Prints the topic data as JSON to stdout
  6. Updates that row's Status to 'In Progress'
  Use error handling. Add a --dry-run flag that doesn't update status."
  > scripts/get_next_topic.py
  ```

- [ ] **3.1.2** Generate `scripts/gate_check.py`:
  ```bash
  gemini -p "Write a Python script called gate_check.py that:
  1. Takes --file path/to/file.md and --gate GATE_1 (or GATE_2, GATE_3, GATE_4) as args
  2. Reads the file and looks for the line 'GATE_X: PASS' or 'GATE_X: FAIL'
  3. Exits with code 0 for PASS, code 1 for FAIL
  4. Also extracts and prints the score if present (e.g. 'Style Score: 87/100')
  Simple, robust, no external dependencies beyond standard library."
  > scripts/gate_check.py
  ```

- [ ] **3.1.3** Generate `scripts/notify_slack.py`:
  ```bash
  gemini -p "Write a Python script called notify_slack.py that:
  1. Takes --topic-id, --dry-run (bool), --fact-score, --style-score, --flags as args
  2. Reads pipeline/{topic_id}/draft.md to get first 400 chars of Instagram caption
  3. Sends a Slack Block Kit message to SLACK_REVIEW_CHANNEL_ID (env var)
  4. Message includes: topic title, caption preview, quality scores, any flags, and 3 buttons: Approve / Request Changes / Reject
  5. Each button's value includes the topic_id and dry_run status
  6. Uses SLACK_BOT_TOKEN env var
  7. Also attaches the instagram.png file from pipeline/{topic_id}/
  Use requests library only. No Slack SDK."
  > scripts/notify_slack.py
  ```

- [ ] **3.1.4** Generate `scripts/publish_instagram.py`:
  ```bash
  gemini -p "Write a Python script called publish_instagram.py that:
  1. Takes --topic-id as argument
  2. Reads pipeline/{topic_id}/draft.md and extracts the Instagram caption section
  3. The PNG file is at pipeline/{topic_id}/instagram.png
  4. Uploads the image to Instagram using Instagram Graph API (2-step: create media container, then publish)
  5. Uses env vars: INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_USER_ID
  6. Logs the published post URL to stdout
  7. If --dry-run flag is set, skips the API call and prints DRY_RUN instead
  Use requests library only."
  > scripts/publish_instagram.py
  ```

- [ ] **3.1.5** Generate `scripts/update_sheets.py`:
  ```bash
  gemini -p "Write a Python script called update_sheets.py that:
  1. Takes --topic-id, --status (Published/Failed/Rejected), --post-url (optional) as args
  2. Updates Content_Queue tab: sets Status column for the matching Topic_ID row
  3. If status=Published: also appends a row to Published_Log with topic_id, date, post_url, fact_score, style_score
  4. Same Google Sheets auth as get_next_topic.py (GOOGLE_SERVICE_ACCOUNT_JSON env var)
  Uses gspread. Add error handling."
  > scripts/update_sheets.py
  ```

- [ ] **3.1.6** Review all generated scripts, test locally with `--dry-run` flags
- [ ] **3.1.7** Commit: `git add scripts/ && git commit -m "Add Gemini-generated helper scripts"`

**Phase 3 Total: ~2 hours**

---

## PHASE 4 — GitHub Actions Workflows (3 hours)

### 4.1 Main Pipeline: `.github/workflows/content-pipeline.yml`

- [ ] **4.1.1** Create the workflow file with:

```yaml
name: Content Pipeline

on:
  schedule:
    - cron: '0 3 * * 1-5'  # Mon-Fri 9am Bangladesh (UTC+6 → UTC 3am)
  workflow_dispatch:
    inputs:
      topic_id:
        description: 'Force a specific Topic ID (leave blank for auto)'
        required: false
      dry_run:
        description: 'Dry run (no Instagram publish)'
        type: boolean
        default: true

jobs:
  pipeline:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    
    env:
      GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
      GOOGLE_SERVICE_ACCOUNT_JSON: ${{ secrets.GOOGLE_SERVICE_ACCOUNT_JSON }}
      GOOGLE_SHEETS_ID: ${{ secrets.GOOGLE_SHEETS_ID }}
      SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
      SLACK_REVIEW_CHANNEL_ID: ${{ secrets.SLACK_REVIEW_CHANNEL_ID }}
      SLACK_ERRORS_CHANNEL_ID: ${{ secrets.SLACK_ERRORS_CHANNEL_ID }}
      INSTAGRAM_ACCESS_TOKEN: ${{ secrets.INSTAGRAM_ACCESS_TOKEN }}
      INSTAGRAM_USER_ID: ${{ secrets.INSTAGRAM_USER_ID }}
      DRY_RUN: ${{ inputs.dry_run || 'true' }}

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Python dependencies
        run: pip install gspread google-auth requests matplotlib pillow

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Gemini CLI
        run: npm install -g @google/gemini-cli

      # ─── Get next topic ────────────────────────────────────
      - name: Get next topic from Sheets
        id: topic
        run: |
          TOPIC_JSON=$(python scripts/get_next_topic.py \
            --force-id "${{ inputs.topic_id }}" \
            ${{ env.DRY_RUN == 'true' && '--dry-run' || '' }})
          echo "topic_id=$(echo $TOPIC_JSON | python -c 'import sys,json; print(json.load(sys.stdin)[\"Topic_ID\"])')" >> $GITHUB_OUTPUT
          echo "topic_english=$(echo $TOPIC_JSON | python -c 'import sys,json; print(json.load(sys.stdin)[\"Topic_English\"])')" >> $GITHUB_OUTPUT
          echo $TOPIC_JSON > topics/${{ steps.topic.outputs.topic_id }}.md
          mkdir -p pipeline/${{ steps.topic.outputs.topic_id }}

      - name: Set TOPIC_ID env var
        run: echo "TOPIC_ID=${{ steps.topic.outputs.topic_id }}" >> $GITHUB_ENV

      # ─── Stage 1: Research ─────────────────────────────────
      - name: Stage 1 - Research
        run: |
          gemini \
            --model gemini-2.5-pro \
            --prompt "$(cat prompts/01_research.md)" \
            --file "config/source_priority.md" \
            --file "config/editorial_preferences.md" \
            --file "topics/${TOPIC_ID}.md" \
            > pipeline/${TOPIC_ID}/research.md

      - name: Gate 1 Check
        run: python scripts/gate_check.py --file pipeline/${TOPIC_ID}/research.md --gate GATE_1

      # ─── Stage 2: Write ────────────────────────────────────
      - name: Stage 2 - Write Content
        run: |
          gemini \
            --model gemini-2.5-pro \
            --prompt "$(cat prompts/02_write.md)" \
            --file "config/writing_style_profile.md" \
            --file "pipeline/${TOPIC_ID}/research.md" \
            > pipeline/${TOPIC_ID}/draft.md

      # ─── Stage 3: Fact-Check ───────────────────────────────
      - name: Stage 3 - Fact Check
        run: |
          gemini \
            --model gemini-2.5-pro \
            --prompt "$(cat prompts/03_factcheck.md)" \
            --file "config/fact_check_protocols.md" \
            --file "pipeline/${TOPIC_ID}/research.md" \
            --file "pipeline/${TOPIC_ID}/draft.md" \
            > pipeline/${TOPIC_ID}/factcheck.md

      - name: Gate 2 Check
        id: gate2
        run: python scripts/gate_check.py --file pipeline/${TOPIC_ID}/factcheck.md --gate GATE_2

      # ─── Stage 4: Style Check ──────────────────────────────
      - name: Stage 4 - Style Check
        run: |
          gemini \
            --model gemini-2.5-flash \
            --prompt "$(cat prompts/04_stylecheck.md)" \
            --file "config/writing_style_profile.md" \
            --file "pipeline/${TOPIC_ID}/draft.md" \
            > pipeline/${TOPIC_ID}/stylecheck.md

      - name: Gate 3 Check
        id: gate3
        run: python scripts/gate_check.py --file pipeline/${TOPIC_ID}/stylecheck.md --gate GATE_3

      # ─── Stage 5: Visual ───────────────────────────────────
      - name: Stage 5 - Generate Chart Code
        run: |
          gemini \
            --model gemini-2.5-pro \
            --prompt "$(cat prompts/05_visual.md)" \
            --file "config/visual_identity.md" \
            --file "pipeline/${TOPIC_ID}/research.md" \
            > pipeline/${TOPIC_ID}/visual_report.md
          # Extract Python code block from visual_report.md
          python scripts/run_visual.py --topic-id ${TOPIC_ID}

      - name: Gate 4 Check
        run: |
          [ -f "pipeline/${TOPIC_ID}/instagram.png" ] || (echo "Instagram PNG not found" && exit 1)
          python scripts/gate_check.py --file pipeline/${TOPIC_ID}/visual_report.md --gate GATE_4

      # ─── Commit pipeline outputs ───────────────────────────
      - name: Commit pipeline outputs to repo
        run: |
          git config user.email "pipeline-bot@bd-content"
          git config user.name "BD Pipeline Bot"
          git add pipeline/${TOPIC_ID}/
          git add topics/${TOPIC_ID}.md
          git diff --staged --quiet || git commit -m "Pipeline run: ${TOPIC_ID} $(date +%Y-%m-%d)"
          git push

      # ─── Notify human ──────────────────────────────────────
      - name: Send Slack review notification
        run: |
          python scripts/notify_slack.py \
            --topic-id ${TOPIC_ID} \
            ${{ env.DRY_RUN == 'true' && '--dry-run' || '' }}

      # ─── Error handling ────────────────────────────────────
      - name: Handle pipeline failure
        if: failure()
        run: |
          python scripts/update_sheets.py --topic-id ${TOPIC_ID} --status Failed
          curl -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
            -H "Content-type: application/json" \
            --data "{\"channel\":\"$SLACK_ERRORS_CHANNEL_ID\",\"text\":\"❌ Pipeline failed for ${TOPIC_ID}. Check Actions: $GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID\"}" \
            https://slack.com/api/chat.postMessage
```

- [ ] **4.1.2** Commit workflow file

### 4.2 Topic Suggester: `.github/workflows/topic-suggester.yml`

- [ ] **4.2.1** Create a simpler workflow that runs every Monday morning:
  - Runs Gemini CLI with a topic-generation prompt
  - Reads `config/editorial_preferences.md` + recent Bangladesh news (Gemini CLI browses web)
  - Outputs `Topic_Suggestions` sheet rows
  - Commits the suggestion file to `pipeline/suggestions/week-{N}.md`
  - Posts suggestions to Slack for your review

### 4.3 Approval Webhook Handler
The Slack approval buttons need a URL to send to. Options (pick one):

- [ ] **4.3.1** **Option A (Simpler):** Use a GitHub Actions `workflow_dispatch` as the approval mechanism. Instead of Slack buttons, the Slack message contains a link to manually trigger the publish workflow in GitHub. You click the link → GitHub shows a form → you click Run. No webhook server needed.

- [ ] **4.3.2** **Option B (Smoother UX):** Use a free Cloudflare Worker (free tier: 100k req/day) as the webhook receiver. The worker receives the Slack button click and triggers the GitHub Actions API to run the publish workflow. Write the worker code by asking Gemini CLI: `gemini -p "Write a Cloudflare Worker that receives a Slack interactive component webhook, validates the token, and triggers a GitHub Actions workflow_dispatch via the GitHub API"`

**Recommendation for MVP:** Start with Option A (GitHub Actions manual trigger). Upgrade to Option B in Month 2.

### 4.4 Health Check: `.github/workflows/health-check.yml`

- [ ] **4.4.1** Simple daily workflow:
  - Pings Gemini API with a 1-token request
  - Pings Instagram API to check token validity
  - Checks Google Sheets is accessible
  - Posts summary to Slack errors channel if anything fails

**Phase 4 Total: ~3 hours**

---

## PHASE 5 — End-to-End Testing (6 hours)

### 5.1 Local Testing First
- [ ] **5.1.1** Create a test topic file: `topics/T001.md` with your education budget topic
- [ ] **5.1.2** Run Stage 1 locally:
  ```bash
  gemini --model gemini-2.5-pro \
    --prompt "$(cat prompts/01_research.md)" \
    --file config/source_priority.md \
    --file config/editorial_preferences.md \
    --file topics/T001.md \
    > pipeline/T001/research.md
  ```
- [ ] **5.1.3** Review `pipeline/T001/research.md` — are sources correct? Data points cited?
- [ ] **5.1.4** Repeat for Stages 2-5 locally, reviewing output at each stage
- [ ] **5.1.5** Fix prompt files based on what's wrong before touching GitHub Actions

### 5.2 GitHub Actions Dry Run
- [ ] **5.2.1** Push all files to GitHub
- [ ] **5.2.2** Go to Actions → Content Pipeline → Run workflow → enter T001, dry_run = true
- [ ] **5.2.3** Watch each step in real time — identify failures
- [ ] **5.2.4** Check that Slack notification arrives with content package
- [ ] **5.2.5** Click "Approve" (or the GitHub link equivalent) → verify no Instagram post goes out (dry run)

### 5.3 Quality Assessment Checklist
For each test topic, evaluate:
- [ ] **5.3.1** Research: Are all data points from Tier 1/2 sources? Do URLs actually exist?
- [ ] **5.3.2** Content: Does the draft sound like your writing style? Is the Bangla natural?
- [ ] **5.3.3** Fact-check: Are the verifications making sense, or is Gemini hallucinating?
- [ ] **5.3.4** Visual: Is the chart readable? On-brand? Honest (no misleading axes)?
- [ ] **5.3.5** Overall: Would you publish this without changes?

### 5.4 Prompt Iteration
- [ ] **5.4.1** Edit prompt files based on issues found (not code — just the `.md` prompts)
- [ ] **5.4.2** Re-run locally for fast iteration
- [ ] **5.4.3** Target: 3 topics with ≥70% of content approvable as-is
- [ ] **5.4.4** Run 3 full topics through GitHub Actions dry-run

### 5.5 First Live Posts
- [ ] **5.5.1** Run workflow with `dry_run = false` for 1 topic
- [ ] **5.5.2** Review Slack package → click Approve
- [ ] **5.5.3** Verify post on Instagram
- [ ] **5.5.4** Verify Published_Log updated in Sheets
- [ ] **5.5.5** Celebrate 🎉

**Phase 5 Total: ~6 hours**

---

## 📊 Phase Summary

| Phase | What You Do | What Gemini Does | Hours |
|---|---|---|---|
| 0 | Set up GitHub, Slack, Sheets, Instagram API accounts | — | 2.5 hrs |
| 1 | Write 5 config Markdown files (your brand's DNA) | — | 4 hrs |
| 2 | Write 5 prompt Markdown files (agent instructions) | — | 3 hrs |
| 3 | Write 5 Gemini CLI prompts asking for scripts | Writes all 5 Python helper scripts | 2 hrs |
| 4 | Write GitHub Actions YAML workflows | — | 3 hrs |
| 5 | Test, review output quality, tune prompts, first post | Researches, writes, fact-checks, makes charts | 6 hrs |
| **TOTAL** | | | **~20.5 hours** |

> **Reduction from v2 (39 hrs) → v3 (20.5 hrs).** The ~18.5 hours saved comes from eliminating Docker, Cloud Run, Cloud Scheduler, manual Python agent code, and MCP server setup.

---

## 💰 Cost Breakdown

| Service | Monthly Cost | Notes |
|---|---|---|
| Gemini API (work) | **$0** | Enterprise access via work |
| GitHub (personal repo) | **$0** | Private repos free; Actions 2,000 min/month free |
| Slack | **$0** | Free tier (10k message history limit) |
| Google Sheets/Drive | **$0** | Existing Workspace |
| Instagram API | **$0** | Free |
| Cloudflare Workers (optional) | **$0** | 100k requests/day free tier |
| **TOTAL** | **$0/month** | |

> If you add Claude API for writing quality upgrade: ~$15-20/month. Optional, not required for MVP.

---

## ⚠️ Known Constraints & Workarounds

| Constraint | Impact | Workaround |
|---|---|---|
| Gemini CLI cannot scrape JS-heavy pages (BBS portal uses JS tables) | Research agent may miss some BBS data | Prompt Gemini to try multiple URL patterns + fallback to World Bank mirror data |
| GitHub Actions free tier: 2,000 min/month | Each pipeline run ≈ 20-30 min → ~66 runs/month before limits | Well within limits for 1/day target; upgrade to Pro ($4/mo) if scaling past 5/day |
| Instagram token expires every 60 days | Pipeline breaks if not refreshed | Health check workflow alerts 10 days before expiry |
| No GCP Secret Manager | Secrets in GitHub Secrets only | GitHub Secrets is fine; cannot be read from Actions logs; encrypted at rest |
| Slack approval = GitHub link (not button) in MVP | Slightly less smooth UX | Acceptable for MVP; add Cloudflare Worker in Month 2 for true button approval |

---

## 📅 Execution Schedule

| Day | Morning (2 hrs) | Afternoon (2 hrs) | Evening (1 hr) |
|---|---|---|---|
| 1 | Phase 0: GitHub repo + Secrets setup | Phase 0: Slack + Sheets + Instagram API | Phase 1: Start writing_style_profile.md |
| 2 | Phase 1: Complete all 5 config files | Phase 2: Write prompts 01 + 02 | Phase 2: Write prompts 03 + 04 |
| 3 | Phase 2: Write prompt 05 | Phase 3: Generate all scripts via Gemini CLI | Review + commit scripts |
| 4 | Phase 4: Write content-pipeline.yml | Phase 4: Write topic-suggester + health-check | First commit + test trigger |
| 5 | Phase 5: Local Gemini CLI tests (3 topics) | Phase 5: Fix prompt files based on output | Phase 5: GitHub Actions dry run |
| 6 | Phase 5: Quality review + prompt tuning | Phase 5: GitHub Actions dry run (2 more) | First live post 🎉 |

**Goal: First real post live on Instagram within 6 days.**