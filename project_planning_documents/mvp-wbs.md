# Bangladesh Content Platform — Simplified MVP v4.0
## Google Cloud-Centric Work Breakdown Structure

> **Version 4.0 Philosophy:** Maximum Google Cloud Services utilization · GCS bucket as primary storage · GitHub for version control only · No external service accounts · Immediate actionable steps
> **Target:** 1 verified post/day · <15 min human time · ~$0/month (using company GCP)

---

## 🎯 Architectural Simplification

### Key Changes from v3.0

| Component | v3.0 Approach | v4.0 Approach | Rationale |
|-----------|---------------|---------------|-----------|
| **Storage** | GitHub repo files | GCS bucket | Use company's GCP resources |
| **Orchestration** | GitHub Actions | Cloud Scheduler + Cloud Functions | Native GCP, no external service account risk |
| **AI Engine** | Gemini CLI | Gemini API (direct) | Already have enterprise access |
| **Config Management** | Markdown in GitHub | Markdown in GCS + GitHub sync | GCS as source of truth, GitHub for version control |
| **Secrets** | GitHub Secrets | No secrets needed (service account-free design) | Security requirement |

### What This Version Optimizes For

1. ✅ **Company GCP Resources:** Cloud Functions, Cloud Scheduler, GCS buckets (existing project)
2. ✅ **Zero Service Accounts:** No credentials for 3rd party services (except Instagram API, which is necessary)
3. ✅ **Simplified Storage:** Everything in one GCS bucket with clear folder structure
4. ✅ **GitHub as Backup:** Code and configs versioned, but execution happens in GCP
5. ✅ **Immediate Start:** No infrastructure provisioning needed (use existing project)

---

## 🏗️ Simplified Architecture

```
┌─────────────────────────────────────────────────────────┐
│  HUMAN LAYER                                             │
│  • Google Sheets: Topic queue, publication log          │
│  • Gmail: Review notifications (no Slack needed)         │
│  • GCS Console: View pipeline outputs                   │
│  • GitHub: Version control for configs/code             │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  ORCHESTRATION LAYER: Cloud Scheduler + Cloud Functions │
│  • Cloud Scheduler: Daily trigger (9am Bangladesh)      │
│  • Main Function: Reads Sheets, runs Gemini pipeline    │
│  • Publish Function: Posts to Instagram when approved   │
│  • All Python code in functions (no external servers)   │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  AI LAYER: Gemini 2.5 Pro API (Direct)                  │
│  • Research: Multi-turn conversation with web search    │
│  • Writing: Style-aware content generation              │
│  • Fact-check: Source verification                      │
│  • Visual: Code generation for charts                   │
│  • All prompts stored as .md files in GCS               │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  STORAGE LAYER: Single GCS Bucket                       │
│  gs://[company-bucket]/bd-content/                      │
│  ├── config/           # Your preference files (.md)    │
│  ├── prompts/          # Gemini instruction files       │
│  ├── topics/           # Active topic briefs            │
│  ├── pipeline/         # Work-in-progress outputs       │
│  ├── published/        # Approved content archive       │
│  └── assets/           # Generated images (.png)        │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 GCS Bucket Structure

```
gs://[your-company-bucket]/bd-content/
│
├── config/                           # Configuration files (YOU write, sync from GitHub)
│   ├── writing_style_profile.md      # 1-2 pages, your voice examples
│   ├── editorial_preferences.md      # Topics to cover/avoid
│   ├── visual_identity.md            # Colors, fonts (markdown table format)
│   ├── source_priority.md            # BBS, World Bank, etc. with URLs
│   └── fact_check_protocols.md       # Verification rules
│
├── prompts/                          # Gemini API system prompts (YOU write once)
│   ├── research_prompt.md            # Instructions for data gathering
│   ├── writer_prompt.md              # Bilingual content generation rules
│   ├── factcheck_prompt.md           # Claim verification instructions
│   ├── stylecheck_prompt.md          # Style scoring criteria
│   └── visual_prompt.md              # Chart generation specifications
│
├── topics/                           # One file per topic (auto-generated from Sheets)
│   ├── T001_education_spending.md    # Topic: brief, context, deadline
│   ├── T002_gdp_growth.md
│   └── ...
│
├── pipeline/                         # Pipeline execution outputs (auto-generated)
│   ├── T001/
│   │   ├── 01_research.json          # Structured data + sources
│   │   ├── 02_draft.md               # Bangla-English content
│   │   ├── 03_factcheck_report.json  # Verification results
│   │   ├── 04_style_report.json      # Style score + issues
│   │   ├── 05_chart_code.py          # Matplotlib code
│   │   └── 06_final_package.json     # Ready for review
│   └── T002/
│       └── ...
│
├── assets/                           # Generated visual content
│   ├── T001_chart.png                # Instagram-ready 1080x1080
│   ├── T002_chart.png
│   └── ...
│
└── published/                        # Approved content archive
    ├── T001/
    │   ├── caption.md
    │   ├── image.png
    │   └── metadata.json             # Post URL, date, engagement
    └── T002/
        └── ...
```

---

## 🛠️ Technology Stack (Simplified)

| Component | Technology | Cost | Why This Choice |
|-----------|-----------|------|-----------------|
| **Storage** | GCS Bucket | $0 (existing) | Company resource, no setup needed |
| **Compute** | Cloud Functions (2nd gen) | ~$0 (free tier: 2M invocations/month) | Serverless, no VM management |
| **Scheduling** | Cloud Scheduler | ~$0 (free tier: 3 jobs) | Native GCP integration |
| **AI** | Gemini 2.5 Pro API | $0 (enterprise via work) | Already available |
| **Database** | Google Sheets API | $0 | Already using Workspace |
| **Publishing** | Instagram Graph API | $0 | Only external API needed |
| **Version Control** | GitHub (private repo) | $0 | Code backup only, not execution |
| **Notifications** | Gmail API | $0 | No Slack needed, Workspace integration |

**Total Monthly Cost:** ~$0 (staying within free tiers)

---

## 📋 DETAILED WORK BREAKDOWN STRUCTURE

---

## ⏱️ TODAY'S IMMEDIATE ACTIONS (4-6 hours)

### PHASE 0: Environment Setup (1.5 hours)

#### 0.1 GCS Bucket Setup (20 min)

**Task:** Create folder structure in company's GCS bucket

**Steps:**
1. Open Google Cloud Console → Storage → Buckets
2. Navigate to your accessible bucket (e.g., `gs://your-company-bucket`)
3. Create folder: `bd-content/`
4. Inside `bd-content/`, create these folders:
   ```
   bd-content/config/
   bd-content/prompts/
   bd-content/topics/
   bd-content/pipeline/
   bd-content/published/
   bd-content/assets/
   ```
5. Test upload: Create a file `bd-content/README.md`:
   ```markdown
   # Bangladesh Content Platform
   Created: [Today's Date]
   Purpose: Automated political content generation
   ```
6. Upload via console to verify write permissions

**Validation:**
- [ ] Can navigate to `gs://[bucket]/bd-content/` in console
- [ ] Can upload/view README.md
- [ ] All 6 folders visible

---

#### 0.2 GitHub Repository (Version Control) (15 min)

**Task:** Create private repo for code versioning (not execution)

**Steps:**
1. Go to github.com → New Repository
2. Name: `bd-content-platform`
3. Privacy: **Private**
4. Initialize with README
5. Clone locally:
   ```bash
   cd ~/projects  # or your preferred location
   git clone https://github.com/[YOUR-USERNAME]/bd-content-platform
   cd bd-content-platform
   ```
6. Create local folder structure matching GCS:
   ```bash
   mkdir -p config prompts functions
   touch .gitignore
   ```
7. Add to `.gitignore`:
   ```
   # Secrets
   .env
   service-account-key.json
   
   # Local testing
   __pycache__/
   *.pyc
   .pytest_cache/
   venv/
   
   # Pipeline outputs (these stay in GCS only)
   pipeline/
   published/
   assets/
   ```

**Validation:**
- [ ] Repo is private
- [ ] Can push commits
- [ ] .gitignore excludes sensitive files

---

#### 0.3 Google Sheets Setup (30 min)

**Task:** Create content management spreadsheet

**Steps:**
1. Create new Google Sheet: "BD Content Platform"
2. Share with your work email (edit access)
3. Create 3 sheets (tabs):

**Sheet 1: "Content_Queue"**
| Column A | Column B | Column C | Column D | Column E | Column F | Column G |
|----------|----------|----------|----------|----------|----------|----------|
| Topic_ID | Topic_Bangla | Topic_English | Priority | Context_Notes | Inspiration_URLs | Status |
| T001 | শিক্ষা খরচ তুলনা | Education Spending Comparison | High | Compare 1996-2001 vs 2009-2024 primary education | https://example.com/similar | Approved |

**Sheet 2: "Published_Log"**
| Column A | Column B | Column C | Column D | Column E | Column F |
|----------|----------|----------|----------|----------|----------|
| Topic_ID | Published_Date | Instagram_URL | Likes | Comments | Status |

**Sheet 3: "Pipeline_Status"**
| Column A | Column B | Column C | Column D | Column E |
|----------|----------|----------|----------|----------|
| Topic_ID | Stage | Status | Last_Updated | Notes |

4. Note the Sheet ID from URL: `https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit`

**Validation:**
- [ ] 3 sheets created with correct headers
- [ ] Can manually edit cells
- [ ] Sheet ID copied for later use

---

#### 0.4 Enable Required Google APIs (15 min)

**Task:** Enable APIs in existing GCP project

**Steps:**
1. Go to GCP Console → APIs & Services → Library
2. Search and Enable these APIs:
   - **Cloud Functions API**
   - **Cloud Scheduler API**
   - **Cloud Build API** (needed for function deployment)
   - **Google Sheets API**
   - **Gmail API** (for notifications)
   - **Gemini API** (if not already enabled)
3. Wait 2-3 minutes for propagation

**Validation:**
- [ ] All 6 APIs show "Enabled" status
- [ ] No error messages in notifications

---

#### 0.5 Instagram API Setup (10 min)

**Task:** Get Instagram access token for publishing

**Steps:**
1. Go to developers.facebook.com
2. My Apps → Create App → Business
3. Add Instagram Graph API product
4. Connect your Instagram Business/Creator account
5. Generate Long-Lived Access Token (60-day validity)
6. Save token to a secure note (we'll store it in Cloud Function environment later)

**Validation:**
- [ ] Long-lived token generated (starts with `EAA...`)
- [ ] Token stored securely (NOT in GitHub)
- [ ] Instagram account connected

---

### PHASE 1: Configuration Files (2 hours)

#### 1.1 Writing Style Profile (30 min)

**Task:** Document YOUR unique voice

**Location:** Create `config/writing_style_profile.md`

**Template:**
```markdown
# Writing Style Profile

## Voice Characteristics
- **Tone:** [e.g., Informative yet conversational, like a knowledgeable friend]
- **Formality:** [e.g., Semi-formal, accessible to 18-35 year olds]
- **Perspective:** [e.g., First-person plural "আমরা দেখছি", "We observe"]

## Language Mix Rules
- **Headlines:** 60% Bangla, 40% English (numbers in English)
- **Body Text:** 70% Bangla, 30% English (technical terms)
- **Statistics:** Always English numerals with Bangla context
- **Sources:** English (international standards)

## Vocabulary Rules

### ALWAYS USE (Bangla):
- "তথ্য" (data) not "ডেটা"  
- "সরকার" (government) not "গভর্নমেন্ট"
- "অর্থনীতি" (economy) not "ইকোনমি"

### NEVER USE:
- Inflammatory words without verification ("দুর্নীতি" needs proof)
- Partisan labels ("ভালো"/"খারাপ" for governments without data)
- Absolute claims ("সবচেয়ে বেশি" without citation)

## Example Post (Reference for Gemini):

```
শিক্ষা খাতে কত টাকা খরচ হচ্ছে? 🎓

একটা interesting comparison:

**Period A (1996-2001):**
• Education budget: GDP-র ২.১%
• প্রাথমিক enrollment: ৮৭%

**Period B (2009-2024):**
• Education budget: GDP-র ২.৫%
• প্রাথমিক enrollment: ৯৮%

অগ্রগতি আছে, তবে UNESCO recommendation: 4-6% of GDP
আমরা এখনও সেখানে পৌঁছাইনি।

আপনার মতামত?

📚 Source: UNESCO Institute for Statistics  
[Link: https://...]
```

## Structural Templates

### Comparison Post:
1. Question headline (Bangla)
2. Context (1-2 lines)
3. Data comparison (bullet points)
4. Analysis (what changed?)
5. Source citation
6. Engagement question

### Timeline Post:
1. Event/Topic + time span
2. Hook (why it matters)
3. Chronological data points
4. Visual indicator for each milestone
5. Source link
```

**Action:**
1. Copy template to local file: `config/writing_style_profile.md`
2. Replace bracketed placeholders with YOUR preferences
3. Add 2-3 of your actual example posts (if you have any)
4. Upload to GCS: `gs://[bucket]/bd-content/config/writing_style_profile.md`
5. Commit to GitHub:
   ```bash
   git add config/writing_style_profile.md
   git commit -m "Add writing style profile"
   git push
   ```

**Validation:**
- [ ] File exists in both GCS and GitHub
- [ ] At least 1 complete example post included
- [ ] All vocabulary rules defined

---

#### 1.2 Editorial Preferences (20 min)

**Location:** Create `config/editorial_preferences.md`

**Template:**
```markdown
# Editorial Preferences

## Content Philosophy
- Strictly objective, data-driven storytelling
- No partisan language or subjective judgments
- Focus on verifiable facts from official sources
- Let numbers tell the story

## Priority Topics (Rank these in research)
1. Economic indicators (GDP, inflation, unemployment)
2. Education system metrics (budget, enrollment, outcomes)
3. Infrastructure development (roads, bridges, digital)
4. Public health data (life expectancy, hospital access)
5. International comparisons (BD vs neighbors)

## Topics to AVOID
- Religious controversies (no data-based discussion possible)
- Active legal cases (sub judice)
- Personal scandals without official records
- Speculation about future events
- Unverified social media claims

## Audience Profile
- **Age:** 18-35 years old
- **Location:** Primarily urban Bangladesh, some diaspora
- **Education:** College-educated or students
- **Preferences:** Quick facts, visual data, comparative analysis
- **Dislikes:** Long text, partisan rhetoric, clickbait

## Source Tier System

### Tier 1 (Always Prefer):
- Bangladesh Bureau of Statistics (BBS)
- Bangladesh Bank
- World Bank Open Data
- UNESCO Institute for Statistics
- IMF Country Reports

### Tier 2 (Use if Tier 1 unavailable):
- UN agencies (UNDP, UNICEF)
- Asian Development Bank
- Credible local research institutes

### Tier 3 (Use with caution + cross-check):
- News media reports (verify original source)
- Academic papers (check methodology)
- NGO reports (check funding bias)

## Tone Guidelines
- Informative without being preachy
- Curious without being accusatory
- Respectful of all political periods
- Educational, not entertainment
```

**Action:**
1. Create file locally, fill template
2. Upload to GCS: `gs://[bucket]/bd-content/config/editorial_preferences.md`
3. Commit to GitHub
4. **Important:** Review and customize the "Priority Topics" section to match YOUR interests

**Validation:**
- [ ] File in GCS and GitHub
- [ ] Source tier system defined with specific URLs
- [ ] At least 5 topics to avoid listed

---

#### 1.3 Visual Identity (30 min)

**Location:** Create `config/visual_identity.md`

**Template:**
```markdown
# Visual Identity Guide

## Brand Colors (Markdown-Friendly Format)

| Purpose | Color Name | Hex Code | Usage |
|---------|------------|----------|-------|
| Primary | Bangladesh Green | `#006A4E` | Headers, key statistics, CTAs |
| Secondary | Liberation Red | `#F42A41` | Highlights, important dates, negative trends |
| Neutral Dark | Charcoal | `#1A1A1A` | Body text, chart labels |
| Neutral Light | Off-White | `#F5F5F5` | Backgrounds, subtle contrast |
| Data - Positive | Growth Green | `#10B981` | Upward trends, improvements |
| Data - Negative | Alert Red | `#EF4444` | Downward trends, concerns |
| Data - Neutral | Gray | `#6B7280` | Comparisons, benchmarks |

## Typography

| Element | Bangla Font | English Font | Size | Weight |
|---------|-------------|--------------|------|--------|
| Headlines | Noto Sans Bengali | Inter | 32px | Bold |
| Subheadlines | Noto Sans Bengali | Inter | 24px | SemiBold |
| Body Text | Noto Sans Bengali | Inter | 18px | Regular |
| Captions | Noto Sans Bengali | Inter | 14px | Regular |
| Source Citations | — | Inter | 12px | Regular |

## Layout Specifications

### Instagram Square (1080x1080px)
- Margins: 80px all sides
- Content area: 920x920px
- Logo placement: Top-right, 60px from edges
- Source citation: Bottom-left corner
- Watermark: Bottom-right, 60% opacity

### Facebook Landscape (1200x630px)
- Margins: 60px all sides
- Title area: Top 200px
- Chart area: Center 370px
- Source bar: Bottom 60px

## Chart Style Guidelines

### General Rules
- Line width: 4px for primary data
- Grid lines: Subtle (#E5E7EB), optional
- Axis labels: 14px, dark gray
- Data point markers: 8px circles
- Legend: Top-right or bottom, 12px

### Specific Chart Types

**Line Charts:**
- Use for: Time series, trends
- Max lines: 3 (more = confusing)
- Colors: Primary for main trend, others from data palette

**Bar Charts:**
- Use for: Comparisons, rankings
- Bar width: 60px
- Spacing: 20px between bars
- Rounded corners: 8px

**Pie Charts:**
- Avoid if possible (hard to read exact values)
- If needed: Max 5 segments, label percentages

## Source Citation Format

```
📊 Source: [Organization Name]
   [Short URL or "See link in bio"]
```

Position: Bottom-left, 12px, 70% opacity

## Watermark

```
@BangladeshDataStories
```

Position: Bottom-right, 14px, 60% opacity
```

**Action:**
1. Create file locally
2. Choose YOUR color palette (use Bangladesh flag colors or your preference)
3. Upload to GCS and commit to GitHub

**Validation:**
- [ ] At least 7 colors defined with hex codes
- [ ] Font specifications for Bangla and English
- [ ] Instagram and Facebook layouts specified

---

#### 1.4 Source Priority (20 min)

**Location:** Create `config/source_priority.md`

**Template:**
```markdown
# Data Source Priority & URLs

## Tier 1: Government & International Official Sources

### Bangladesh Bureau of Statistics (BBS)
- **Homepage:** http://bbs.gov.bd/
- **Statistical Yearbook:** http://bbs.portal.gov.bd/sites/default/files/files/bbs.portal.gov.bd/page/[year]/
- **Data Portal:** http://data.bbs.gov.bd/
- **Use for:** GDP, population, education, employment, poverty

### Bangladesh Bank
- **Homepage:** https://www.bb.org.bd/
- **Economic Data:** https://www.bb.org.bd/en/index.php/econdata/index
- **Use for:** Inflation, exchange rates, reserves, monetary policy

### World Bank Open Data
- **Bangladesh Page:** https://data.worldbank.org/country/bangladesh
- **API:** https://api.worldbank.org/v2/country/bgd/indicator/[INDICATOR]
- **Use for:** Cross-country comparisons, historical trends

### UNESCO Institute for Statistics
- **Country Profile:** http://uis.unesco.org/en/country/bd
- **Use for:** Education spending, literacy rates, enrollment

### IMF Bangladesh
- **Country Page:** https://www.imf.org/en/Countries/BGD
- **Use for:** Fiscal data, debt statistics, projections

## Tier 2: Credible International Organizations

### Asian Development Bank
- **URL:** https://www.adb.org/countries/bangladesh/main
- **Use for:** Infrastructure, development indicators

### UNDP Bangladesh
- **URL:** https://www.undp.org/bangladesh
- **Use for:** Human development index, poverty

### UNICEF Bangladesh
- **URL:** https://www.unicef.org/bangladesh/
- **Use for:** Child health, education, nutrition

## Tier 3: News & Research (Verify Before Use)

### The Daily Star
- **URL:** https://www.thedailystar.net/
- **Use:** Only for referencing official announcements (find original source)

### Centre for Policy Dialogue (CPD)
- **URL:** https://cpd.org.bd/
- **Use:** Economic analysis (cite as "CPD analysis of [source]")

## Verification Rules

1. **Always prefer Tier 1** sources
2. If Tier 1 unavailable, use Tier 2 and note in output
3. If using Tier 3, MUST cross-reference with Tier 1 or 2
4. Never use: Wikipedia, blogs, social media as primary sources
5. For controversial data: Require 2+ sources agreement
```

**Action:**
1. Create file with all source URLs
2. Test 3-4 URLs to ensure they work
3. Upload to GCS and commit to GitHub

**Validation:**
- [ ] At least 5 Tier 1 sources with working URLs
- [ ] Each source has clear "Use for:" descriptions
- [ ] Verification rules defined

---

#### 1.5 Fact-Check Protocols (20 min)

**Location:** Create `config/fact_check_protocols.md`

**Template:**
```markdown
# Fact-Checking Protocol

## Mandatory Checks for Every Draft

### 1. Numerical Claims
**Rule:** Every number must have a source URL.

**Process:**
1. Extract all numerical claims from draft
2. For each number, verify:
   - Source document accessible?
   - Number appears in source? (exact match)
   - Context correct? (not cherry-picked)
3. Flag if: Source not accessible, number doesn't match, context misleading

**Pass threshold:** 100% of numbers verified

### 2. Date Accuracy
**Rule:** All dates must be verifiable from sources.

**Check:**
- Government period dates (e.g., "1996-2001" → verify election dates)
- Data release dates (e.g., "BBS published in 2023" → check actual date)
- Historical events (e.g., "Liberation in 1971" → correct)

**Pass threshold:** 100% of dates correct

### 3. Attribution Accuracy
**Rule:** Claims about "X government did Y" must have official source.

**Process:**
1. Identify policy attribution claims
2. Find official government document/announcement
3. Verify timing (did this government implement this?)
4. Note if policy started under previous government (common error)

**Pass threshold:** No false attributions

### 4. Comparative Claims
**Rule:** "Higher than" / "Lower than" statements must use same measurement unit and time period.

**Check:**
- Same currency? (BDT vs USD)
- Same methodology? (CPI vs GDP deflator for inflation)
- Same geographic scope? (National vs regional)
- Same time granularity? (Annual vs quarterly)

**Pass threshold:** All comparisons apples-to-apples

### 5. Omission Check
**Rule:** Are we cherry-picking data?

**Check:**
- If showing positive trend, is there a recent downturn not mentioned?
- If showing increase, is it due to inflation adjustment?
- If showing improvement, what's the absolute level? (80% → 85% sounds good, but if baseline should be 95%, it's actually bad)

**Pass threshold:** No misleading omissions flagged

## Confidence Scoring

For each claim, assign:
- **HIGH:** Direct source, recent, from Tier 1, exact number match
- **MEDIUM:** Tier 2 source, or number requires calculation from source
- **LOW:** Tier 3 source, or indirect inference

**Overall Draft Pass Criteria:**
- 90%+ claims are HIGH confidence
- 0 LOW confidence claims on critical facts
- All flags resolved before human review

## Handling Discrepancies

If two sources disagree:
1. Note both values in fact-check report
2. Check publication dates (use more recent)
3. Check methodology notes (which is more rigorous?)
4. Default to Tier 1 > Tier 2 > Tier 3
5. If still unclear, flag for human review
```

**Action:**
1. Create file locally
2. Review each protocol section - does it make sense for YOUR use case?
3. Upload to GCS and commit to GitHub

**Validation:**
- [ ] 5 check types defined
- [ ] Pass thresholds specified
- [ ] Confidence scoring system clear

---

### PHASE 2: Prompt Engineering (2 hours)

#### 2.1 Research Prompt (30 min)

**Location:** Create `prompts/research_prompt.md`

**Template:**
```markdown
# Research Agent System Prompt

You are a research specialist for a Bangladesh political content platform. Your job is to gather objective, verifiable data from authoritative sources.

## Your Mission
Given a topic brief, find the specific data points needed, cite sources meticulously, and present findings in structured JSON format.

## Source Priority
ALWAYS prefer sources in this order:
1. Bangladesh Bureau of Statistics (BBS)
2. Bangladesh Bank
3. World Bank, UNESCO, IMF
4. Other UN agencies
5. Only use news sources if no official data exists

Read the source priority file for full details.

## Research Process

### Step 1: Understand the Topic
- Read the topic brief carefully
- Identify: What data is needed? What time period? Any comparisons requested?
- Check context notes for user's specific focus

### Step 2: Search Strategy
- Start with Tier 1 sources
- Use specific search terms (e.g., "Bangladesh GDP 1990-2020 BBS" not just "Bangladesh economy")
- Look for official reports, statistical yearbooks, databases
- If a source is paywalled or broken, note it and try alternatives

### Step 3: Data Extraction
- Record exact numbers as they appear (don't round)
- Note units (billion BDT vs USD, percentage points vs percent)
- Capture year/date of data
- Copy the exact URL where you found it

### Step 4: Cross-Verification
- If possible, check the same statistic in a second source
- Flag discrepancies (e.g., "BBS says 5.2%, World Bank says 5.4%")
- Prefer official Bangladesh sources over international estimates when available

### Step 5: Context Gathering
- Look for methodology notes (how was this measured?)
- Check if there are known data issues (e.g., "BBS revised this figure in 2023")
- Note any important caveats (e.g., "excluding informal sector")

## Output Format

Respond ONLY with valid JSON. No markdown, no explanations outside JSON.

```json
{
  "topic_id": "T001",
  "research_date": "2026-02-22",
  "data_points": [
    {
      "metric": "Education Budget (% of GDP)",
      "value": 2.1,
      "unit": "percent",
      "year": "1996-2001",
      "period_type": "average",
      "source": {
        "organization": "UNESCO Institute for Statistics",
        "title": "Education Finance in Bangladesh, 1990-2010",
        "url": "https://exact-url-here.pdf",
        "accessed": "2026-02-22",
        "tier": 1
      },
      "confidence": "high",
      "notes": "Simple average across 6 years (1996-2001)"
    },
    {
      "metric": "Primary School Enrollment Rate",
      "value": 87,
      "unit": "percent",
      "year": "2000",
      "period_type": "annual",
      "source": {
        "organization": "Bangladesh Bureau of Statistics",
        "title": "Statistical Yearbook 2001",
        "url": "http://bbs.portal.gov.bd/.../yearbook_2001.pdf",
        "accessed": "2026-02-22",
        "tier": 1
      },
      "confidence": "high",
      "notes": "Net enrollment rate for ages 6-10"
    }
  ],
  "methodology_notes": "BBS data for 1998 unavailable; used World Bank estimate for that year",
  "data_gaps": ["Government spending breakdown by education level not available for 1996-2001 period"],
  "cross_references": [
    {
      "metric": "Primary enrollment",
      "source1": "BBS: 87%",
      "source2": "World Bank: 86%",
      "resolution": "Used BBS (Tier 1 source)"
    }
  ],
  "human_review_flags": []
}
```

## Quality Standards

- **Minimum:** 3 data points per topic
- **Citation:** 100% of data points have working source URLs
- **Confidence:** 80%+ of data points marked "high" confidence
- **Gaps:** Explicitly note any data you couldn't find

## When to Flag for Human Review

Flag if:
- Cannot find ANY official data on the topic (might need topic change)
- Major discrepancies between sources (>10% difference in numbers)
- Data is outdated (>5 years old and no recent update available)
- Source is only available in Bangla and contains complex statistical tables (you might misread)

## Remember
You are NOT writing content. You are gathering raw materials. Be thorough, be accurate, cite everything.
```

**Action:**
1. Create file locally
2. Review the JSON output format - does it capture what you need?
3. Upload to GCS and commit to GitHub

**Validation:**
- [ ] File uploaded to `gs://[bucket]/bd-content/prompts/research_prompt.md`
- [ ] JSON output format is valid (test with a JSON validator)
- [ ] Committed to GitHub

---

#### 2.2 Writer Prompt (30 min)

**Location:** Create `prompts/writer_prompt.md`

**Template:**
```markdown
# Content Writer System Prompt

You are a bilingual content writer for a Bangladesh political content platform. Your voice must match the creator's style exactly.

## Your Mission
Transform research data into engaging, objective Bangla-English mixed content that educates young Bangladeshis without partisan bias.

## Input
You receive:
1. Research JSON (data points + sources)
2. Writing style profile (the creator's voice)
3. Visual identity guide (for understanding brand tone)
4. Topic context notes (user's specific angle)

## Core Writing Rules

### Language Mix (70% Bangla, 30% English)
- **Headlines:** Start in Bangla for emotional connection
  - Good: "শিক্ষা খাতে কত টাকা খরচ হচ্ছে?"
  - Bad: "How Much is Education Budget?"
- **Body:** Mix naturally, like young Bangladeshis speak
  - Good: "১৯৯৬ সালে education budget ছিল GDP-র ২.১%"
  - Bad: "১৯৯৬ সালে শিক্ষা বাজেট ছিল জিডিপি এর ২.১ শতাংশ" (too formal)
- **Numbers:** ALWAYS use English numerals: "২.১%" → "2.1%"
- **Sources:** English only (international standard)

### Tone Matching
Read the writing style profile carefully. Match:
- Formality level (conversational? academic?)
- Sentence length (short punchy? or longer explanatory?)
- Emoji usage (how many? which types?)
- Question style (rhetorical? direct?)

### Structural Template
Use one of these structures (check style profile for preference):

**Comparison Structure:**
```
[Question headline in Bangla]

[1-2 sentences context]

**Period A:**
• Data point 1
• Data point 2

**Period B:**
• Data point 1
• Data point 2

[Analysis: what changed?]

[Benchmark or context: where should we be?]

[Source citation]

[Engagement question]
```

**Timeline Structure:**
```
[Event + time span in Bangla]

[Hook: why this matters now]

📅 [Year]: [Milestone]
📅 [Year]: [Milestone]
📅 [Year]: [Milestone]

[Trend observation]

[Source citation]

[Forward-looking question]
```

### Citation Rules
- EVERY statistic must reference a source
- Format: "📊 Source: [Organization Name]" at the end
- Include URL if it fits (Instagram allows 1 link in bio, so say "Link in bio")
- For multiple sources, list all

### Objectivity Safeguards
**NEVER:**
- Use value judgments ("good", "bad", "terrible", "excellent") without data support
- Attribute intent ("government wanted to...", "aimed to...")
- Make causal claims without evidence ("due to X, Y happened")
- Cherry-pick data (if trend reversed recently, mention it)

**ALWAYS:**
- Use neutral language ("increased", "decreased", "changed")
- Present both sides of comparisons fairly
- Note data limitations (e.g., "BBS data for 1998 unavailable")
- Include benchmarks (e.g., "UNESCO recommends 4-6%")

## Output Format

Respond with valid JSON:

```json
{
  "topic_id": "T001",
  "draft_date": "2026-02-22",
  "platform": "instagram",
  "content": {
    "caption": "শিক্ষা খাতে কত টাকা খরচ হচ্ছে? 🎓\n\nএকটা interesting comparison:\n\n**Period A (1996-2001):**\n• Education budget: GDP-র 2.1%\n• প্রাথমিক enrollment: 87%\n\n**Period B (2009-2024):**\n• Education budget: GDP-র 2.5%\n• প্রাথমিক enrollment: 98%\n\nঅগ্রগতি আছে, তবে UNESCO recommendation: at least 4% (ideally 6%)\nআমরা এখনও সেখানে পৌঁছাইনি।\n\nআপনার মতামত?\n\n📚 Source: UNESCO Institute for Statistics\n[Link in bio]\n\n#BangladeshEducation #DataDrivenBD",
    "hashtags": ["#BangladeshEducation", "#DataDrivenBD", "#শিক্ষা", "#তথ্যভিত্তিক"],
    "character_count": 487,
    "bangla_percentage": 68,
    "english_percentage": 32
  },
  "metadata": {
    "structure_used": "comparison",
    "emojis_count": 2,
    "questions_count": 2,
    "sources_cited": 1,
    "data_points_used": 4
  },
  "self_review": {
    "style_match_confidence": "high",
    "potential_issues": [],
    "notes": "Used comparison structure as per style guide example. Maintained neutral tone throughout."
  }
}
```

## Quality Checklist (Before Submitting)

- [ ] Bangla-English ratio is 65-75% Bangla, 25-35% English
- [ ] All numerals in English (2.1%, not ২.১%)
- [ ] Every statistic has source attribution
- [ ] No partisan language or value judgments
- [ ] Character count < 2200 (Instagram limit)
- [ ] At least 1 engagement question
- [ ] Hashtags relevant and mix Bangla/English

## Remember
Your job is to make data storytelling accessible, not to make arguments or push agendas. Let the numbers speak.
```

**Action:**
1. Create file locally
2. Review the JSON output format
3. Upload to GCS and commit to GitHub

**Validation:**
- [ ] File in GCS and GitHub
- [ ] Language mix percentages match your preference
- [ ] Example JSON is complete and valid

---

#### 2.3 Fact-Check Prompt (30 min)

**Location:** Create `prompts/factcheck_prompt.md`

**Template:**
```markdown
# Fact-Checker System Prompt

You are a meticulous fact-verification specialist. Your job is to validate every claim in a draft against original sources.

## Your Mission
Verify that every number, date, and claim in the draft content matches the research data and original sources. Catch errors before they reach the audience.

## Input
You receive:
1. Draft content JSON (from writer)
2. Research JSON (original data with source URLs)
3. Fact-check protocols (verification rules)

## Verification Process

### Step 1: Extract Claims
Parse the draft and list all factual claims:
- Numerical claims (GDP was 2.1%)
- Date claims (period 1996-2001)
- Attribution claims (government X implemented Y)
- Comparative claims (higher than, increased from X to Y)
- Trend claims (improved, declined, remained stable)

### Step 2: Match to Research Data
For each claim:
1. Find corresponding data point in research JSON
2. Check: Does number match exactly?
3. Check: Is context correct? (not cherry-picked or misleading)
4. Check: Is source accurately cited?

### Step 3: Fetch Original Sources (If Possible)
If you have web search capability:
- Visit the source URL from research JSON
- Verify the number appears in the source document
- Check if there's additional context that changes meaning

### Step 4: Apply Fact-Check Protocols
Follow the rules from `config/fact_check_protocols.md`:
- 100% of numbers must have sources
- Dates must be verifiable
- Comparisons must use same units
- No false attributions

### Step 5: Assign Confidence Scores
For each claim:
- **VERIFIED:** Number matches source exactly, context accurate
- **MINOR_ISSUE:** Number correct but context could be clearer
- **MAJOR_ISSUE:** Number wrong, misleading context, or no source
- **CANNOT_VERIFY:** Source not accessible (need human review)

## Output Format

```json
{
  "topic_id": "T001",
  "factcheck_date": "2026-02-22",
  "draft_analyzed": "draft.json",
  "claims_extracted": 6,
  "verification_results": [
    {
      "claim_id": 1,
      "claim_text": "Education budget ছিল GDP-র 2.1%",
      "claim_type": "numerical",
      "extracted_value": 2.1,
      "extracted_unit": "percent of GDP",
      "extracted_period": "1996-2001",
      "research_match": {
        "value": 2.1,
        "unit": "percent",
        "period": "1996-2001",
        "source_url": "https://unesco.org/...",
        "matches": true
      },
      "verification_status": "VERIFIED",
      "confidence": "high",
      "notes": "Exact match with UNESCO data, period correct"
    },
    {
      "claim_id": 2,
      "claim_text": "Primary enrollment: 87%",
      "claim_type": "numerical",
      "extracted_value": 87,
      "extracted_unit": "percent",
      "extracted_period": "Period A (implied 1996-2001)",
      "research_match": {
        "value": 87,
        "unit": "percent",
        "year": "2000",
        "source_url": "http://bbs.gov.bd/...",
        "matches": true
      },
      "verification_status": "MINOR_ISSUE",
      "confidence": "medium",
      "notes": "Number correct but draft says 'Period A average' when source only has 2000 data. Should say 'as of 2000'"
    }
  ],
  "overall_assessment": {
    "total_claims": 6,
    "verified": 4,
    "minor_issues": 2,
    "major_issues": 0,
    "cannot_verify": 0,
    "pass_rate": 66.7,
    "passed_threshold": false,
    "threshold_required": 95.0
  },
  "corrections_needed": [
    {
      "claim_id": 2,
      "current_text": "প্রাথমিক enrollment: 87%",
      "suggested_fix": "প্রাথমিক enrollment: 87% (as of 2000)",
      "reason": "Clarify data is point-in-time, not period average"
    }
  ],
  "human_review_flags": [],
  "recommendation": "RETURN_TO_WRITER",
  "reasoning": "Pass rate 66.7% is below 95% threshold. Two minor issues need correction before proceeding."
}
```

## Quality Gates

### GATE 2: Fact-Check Pass Criteria
- ✅ 95%+ of claims verified
- ✅ 0 major issues
- ✅ All corrections applied
- ✅ Source URLs accessible

**If passed:** Draft proceeds to style check
**If failed:** Return to writer with corrections

### Special Cases

**Discrepancy Between Sources:**
If research JSON shows conflicting data from multiple sources:
- Note both values in verification
- Check which source was used in draft
- Verify it's the higher-tier source
- If draft used lower-tier source incorrectly, flag for correction

**Missing Context:**
If a number is technically correct but misleading without context:
- Flag as MINOR_ISSUE
- Suggest adding context (e.g., "but population grew 15%")

**Rounding:**
If draft rounds numbers (2.14% → 2.1%):
- Allow if: reasonable rounding (1 decimal place)
- Flag if: misleading (2.9% → 3% when 3% is a symbolic threshold)

## Remember
Your job is to be the last line of defense against misinformation. Be strict but fair.
```

**Action:**
1. Create file
2. Review verification process
3. Upload to GCS and commit to GitHub

**Validation:**
- [ ] File in GCS and GitHub
- [ ] Pass criteria clearly defined (95% threshold)
- [ ] JSON format valid

---

[Due to length constraints, I'll provide the remaining prompts in a condensed format]

#### 2.4 Style Check Prompt (15 min)

**Location:** `prompts/stylecheck_prompt.md`

**Key Sections:**
- Compare draft against writing_style_profile.md
- Score on 10 dimensions (tone, ratio, structure, etc.)
- Return JSON with score + specific issues
- Pass if score ≥ 85%

**Action:** Create, upload to GCS, commit to GitHub

---

#### 2.5 Visual Designer Prompt (15 min)

**Location:** `prompts/visual_prompt.md`

**Key Sections:**
- Generate Python/Matplotlib code for charts
- Follow visual_identity.md (colors, fonts)
- Output executable .py file
- Add source watermark automatically

**Action:** Create, upload to GCS, commit to GitHub

---

### PHASE 3: Cloud Functions (2-3 hours)

#### 3.1 Main Pipeline Function (90 min)

**Location:** Create `functions/main_pipeline/main.py`

**Function Purpose:** Orchestrate the entire content pipeline when triggered by Cloud Scheduler

**Key Steps:**
1. Read next approved topic from Google Sheets
2. Load config files from GCS
3. Call Gemini API 5 times (research, write, factcheck, stylecheck, visual)
4. Save all outputs to GCS
5. Send Gmail notification when ready for review

**Code Template:**
```python
import functions_framework
from google.cloud import storage
from googleapiclient.discovery import build
import google.generativeai as genai
import json
import os

# Initialize clients
storage_client = storage.Client()
BUCKET_NAME = os.environ.get('GCS_BUCKET')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

@functions_framework.http
def run_pipeline(request):
    """Main pipeline orchestrator"""
    
    # Step 1: Get next topic from Sheets
    topic = get_next_topic_from_sheets()
    if not topic:
        return {"status": "no_topics", "message": "No approved topics found"}
    
    topic_id = topic['Topic_ID']
    
    # Step 2: Load config files from GCS
    configs = load_configs_from_gcs()
    
    # Step 3: Run Gemini stages
    try:
        # Stage 1: Research
        research_result = run_research_stage(topic, configs)
        save_to_gcs(f'pipeline/{topic_id}/01_research.json', research_result)
        
        # Stage 2: Write
        draft = run_write_stage(research_result, configs)
        save_to_gcs(f'pipeline/{topic_id}/02_draft.json', draft)
        
        # Stage 3: Fact-check
        factcheck = run_factcheck_stage(draft, research_result, configs)
        save_to_gcs(f'pipeline/{topic_id}/03_factcheck.json', factcheck)
        
        # Check Gate 2
        if factcheck['overall_assessment']['pass_rate'] < 95:
            # Failed fact-check, notify and stop
            send_notification(topic_id, "failed", "Fact-check failed")
            update_sheets_status(topic_id, "Failed_FactCheck")
            return {"status": "failed", "gate": "factcheck"}
        
        # Stage 4: Style check
        stylecheck = run_stylecheck_stage(draft, configs)
        save_to_gcs(f'pipeline/{topic_id}/04_stylecheck.json', stylecheck)
        
        # Check Gate 3
        if stylecheck['overall_score'] < 85:
            send_notification(topic_id, "failed", "Style check failed")
            update_sheets_status(topic_id, "Failed_StyleCheck")
            return {"status": "failed", "gate": "stylecheck"}
        
        # Stage 5: Visual
        visual_code = run_visual_stage(research_result, configs)
        save_to_gcs(f'pipeline/{topic_id}/05_chart_code.py', visual_code)
        
        # Execute chart code (generates PNG)
        execute_chart_code(topic_id, visual_code)
        
        # All gates passed, notify human
        send_review_notification(topic_id)
        update_sheets_status(topic_id, "Ready_For_Review")
        
        return {"status": "success", "topic_id": topic_id}
        
    except Exception as e:
        send_notification(topic_id, "error", str(e))
        update_sheets_status(topic_id, "Pipeline_Error")
        return {"status": "error", "message": str(e)}, 500

def get_next_topic_from_sheets():
    """Read Content_Queue sheet, return first Approved topic"""
    sheets_service = build('sheets', 'v4')
    sheet_id = os.environ.get('SHEET_ID')
    
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range='Content_Queue!A2:G100'
    ).execute()
    
    rows = result.get('values', [])
    for row in rows:
        if len(row) >= 7 and row[6] == 'Approved':
            return {
                'Topic_ID': row[0],
                'Topic_Bangla': row[1],
                'Topic_English': row[2],
                'Priority': row[3],
                'Context_Notes': row[4],
                'Inspiration_URLs': row[5]
            }
    return None

def load_configs_from_gcs():
    """Load all config .md files from GCS"""
    bucket = storage_client.bucket(BUCKET_NAME)
    configs = {}
    
    config_files = [
        'writing_style_profile.md',
        'editorial_preferences.md',
        'visual_identity.md',
        'source_priority.md',
        'fact_check_protocols.md'
    ]
    
    for filename in config_files:
        blob = bucket.blob(f'bd-content/config/{filename}')
        configs[filename] = blob.download_as_text()
    
    return configs

def run_research_stage(topic, configs):
    """Call Gemini API with research prompt"""
    bucket = storage_client.bucket(BUCKET_NAME)
    research_prompt_blob = bucket.blob('bd-content/prompts/research_prompt.md')
    research_prompt = research_prompt_blob.download_as_text()
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    full_prompt = f"""{research_prompt}

## TOPIC BRIEF
{json.dumps(topic, indent=2)}

## SOURCE PRIORITY
{configs['source_priority.md']}

## EDITORIAL PREFERENCES
{configs['editorial_preferences.md']}

Now research this topic and output JSON only.
"""
    
    response = model.generate_content(full_prompt)
    return response.text

def run_write_stage(research_result, configs):
    """Call Gemini with writer prompt"""
    # Similar structure to run_research_stage
    # Load writer_prompt.md, combine with configs, call Gemini
    pass  # Implementation similar to above

def run_factcheck_stage(draft, research_result, configs):
    """Call Gemini with factcheck prompt"""
    pass  # Implementation similar

def run_stylecheck_stage(draft, configs):
    """Call Gemini with stylecheck prompt"""
    pass

def run_visual_stage(research_result, configs):
    """Call Gemini to generate Matplotlib code"""
    pass

def execute_chart_code(topic_id, python_code):
    """Execute Gemini-generated Python code to create PNG"""
    # Save code to temp file, execute, capture output PNG
    # Upload PNG to GCS at assets/[topic_id]_chart.png
    pass

def save_to_gcs(path, content):
    """Save string content to GCS"""
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f'bd-content/{path}')
    
    if isinstance(content, dict):
        content = json.dumps(content, indent=2)
    
    blob.upload_from_string(content)

def send_review_notification(topic_id):
    """Send Gmail with review package"""
    gmail_service = build('gmail', 'v1')
    
    message = f"""
Subject: [BD Content] Topic {topic_id} Ready for Review

Topic {topic_id} has passed all quality gates and is ready for your review.

View outputs:
https://console.cloud.google.com/storage/browser/[BUCKET]/bd-content/pipeline/{topic_id}

Reply with:
- APPROVE: Will publish to Instagram
- REJECT: Will archive without publishing
- REVISE [notes]: Will flag for manual editing

Pipeline Bot
"""
    
    # Send via Gmail API
    pass

def update_sheets_status(topic_id, status):
    """Update Content_Queue status column"""
    sheets_service = build('sheets', 'v4')
    # Find row with topic_id, update column G
    pass

# Add more helper functions as needed
```

**Action:**
1. Create `functions/main_pipeline/main.py` locally
2. Create `functions/main_pipeline/requirements.txt`:
   ```
   functions-framework==3.*
   google-cloud-storage
   google-api-python-client
   google-generativeai
   ```
3. Test locally (optional):
   ```bash
   cd functions/main_pipeline
   pip install -r requirements.txt
   functions-framework --target=run_pipeline --debug
   ```
4. Deploy to Cloud Functions:
   ```bash
   gcloud functions deploy content-pipeline \
     --gen2 \
     --runtime=python311 \
     --region=asia-southeast1 \
     --source=functions/main_pipeline \
     --entry-point=run_pipeline \
     --trigger-http \
     --allow-unauthenticated \
     --set-env-vars GCS_BUCKET=[YOUR_BUCKET],GEMINI_API_KEY=[YOUR_KEY],SHEET_ID=[YOUR_SHEET_ID]
   ```

**Validation:**
- [ ] Function deploys successfully
- [ ] Can trigger via Cloud Console
- [ ] Logs show execution steps

---

#### 3.2 Publish Function (30 min)

**Location:** Create `functions/publish/main.py`

**Purpose:** Post approved content to Instagram

**Action:**
1. Create function that reads final package from GCS
2. Posts to Instagram Graph API
3. Updates Published_Log in Sheets
4. Archives content to `published/` folder in GCS

---

### PHASE 4: Cloud Scheduler (30 min)

**Task:** Set up daily trigger for pipeline

**Steps:**
1. Go to Cloud Console → Cloud Scheduler
2. Create job:
   - Name: `daily-content-pipeline`
   - Frequency: `0 9 * * 1-6` (9am Mon-Sat, Bangladesh time)
   - Target: HTTP
   - URL: [Your Cloud Function URL from step 3.1]
   - Method: POST
3. Test: Click "Run Now"

**Validation:**
- [ ] Job created
- [ ] Test run triggers function
- [ ] Logs show execution

---

### PHASE 5: Testing (2-3 hours)

#### 5.1 End-to-End Test (90 min)

**Steps:**
1. Add test topic to Google Sheets (Status: Approved)
2. Manually trigger Cloud Scheduler job
3. Monitor Cloud Function logs in real-time
4. Check GCS bucket for outputs at each stage
5. Review quality of generated content
6. Check if Gmail notification received

#### 5.2 Quality Review (60 min)

For the test topic, evaluate:
- Research: Correct sources? Data accurate?
- Content: Matches your style? Bangla-English ratio correct?
- Fact-check: All claims verified?
- Visual: Chart looks good? On-brand?

#### 5.3 Prompt Tuning (Variable)

Based on test results:
- Edit prompt .md files in GCS
- Commit updated versions to GitHub
- Re-run pipeline
- Iterate until quality is acceptable (target: 70%+ approvable as-is)

---

## ✅ Definition of Done

You'll know the MVP is complete when:

- [ ] **Day 1 (Today):** GCS bucket structured, configs created, GitHub repo set up
- [ ] **Day 2:** All 5 prompt files written, Cloud Functions code written
- [ ] **Day 3:** Functions deployed, Cloud Scheduler configured, first test run
- [ ] **Day 4:** Quality tuning, prompt iteration, second test run
- [ ] **Day 5:** Third test run, approval workflow tested
- [ ] **Day 6:** First real post published to Instagram 🎉

---

## 💰 Actual Cost Estimate

| Service | Usage | Cost |
|---------|-------|------|
| Cloud Functions | 30 invocations/month × 2 min avg | $0 (within 2M free tier) |
| Cloud Scheduler | 1 job, 30 triggers/month | $0 (within 3 jobs free) |
| GCS Storage | ~5GB (pipeline outputs + assets) | $0.10/month |
| Gemini API | 30 requests × ~100K tokens | $0 (via work) |
| **TOTAL** | | **~$0.10/month** |

---

## 🚨 Security Considerations

### What We're NOT Doing (Per Your Requirements)
- ❌ No service account for 3rd party tools
- ❌ No external workflow orchestrators (Zapier, n8n)
- ❌ No credentials stored in GitHub
- ❌ No SSH keys or API keys in code

### What We ARE Doing
- ✅ Instagram token in Cloud Function environment variables (encrypted)
- ✅ Gemini API key in Cloud Function environment variables
- ✅ Cloud Functions run in your company's GCP project (already secured)
- ✅ GCS bucket access via default service account (no new credentials)
- ✅ GitHub repo is private, only contains code (no secrets)

---

## 📊 Next Steps After MVP

**Month 2 Improvements:**
1. Add approval buttons via Cloud Functions webhook (instead of Gmail reply)
2. Implement retry logic for failed stages
3. Add weekly idea generator (separate Cloud Function)
4. Create simple web dashboard (Cloud Run + Streamlit)

**Month 3 Scaling:**
1. Increase from 1 post/day to 3-5 posts/day
2. Add Facebook, LinkedIn publishing
3. Implement A/B testing for headlines
4. Add engagement analytics tracking

---

## 🎯 Success Metrics (First 30 Days)

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Content Volume | 20-25 posts published | Count rows in Published_Log sheet |
| Human Time | <15 min/day average | Track time spent reviewing |
| Quality Pass Rate | 70%+ approved as-is | Approval rate from Published_Log |
| Fact-Check Accuracy | 95%+ claims verified | Spot-check 10 random posts |
| System Uptime | 95%+ (no missed days) | Count successful vs failed runs |
| Cost | <$5 total | GCP billing |

---

**START NOW:** Begin with Phase 0, Task 0.1 (GCS Bucket Setup) - should take 20 minutes. You can complete the entire setup in 4-6 hours today if you work through it systematically.

Good luck! 🚀