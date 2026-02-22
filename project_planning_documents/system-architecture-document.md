# Bangladesh Political Content Platform
## Comprehensive System Architecture Design v2.0

> **Document Type:** System Architecture Design  
> **Supersedes:** Architecture v1.0 (DOCX, Feb 22 2026)  
> **PRD Reference:** `bangladesh-content-platform-PRD.md` v1.0  
> **Last Updated:** February 22, 2026  
> **Status:** Revised — Incorporating Claude AI Toolchain & Markdown-First Stack



## Table of Contents

1. [Complete Tool Inventory](#1-complete-tool-inventory)
2. [Architectural Philosophy](#2-architectural-philosophy)
3. [Macro Architecture](#3-macro-architecture)
4. [Micro Architecture — Agent Layer](#4-micro-architecture--agent-layer)
5. [Micro Architecture — Workflow Layer](#5-micro-architecture--workflow-layer)
6. [Micro Architecture — Human Layer](#6-micro-architecture--human-layer)
7. [Markdown-First Configuration System](#7-markdown-first-configuration-system)
8. [Claude AI Toolchain Integration](#8-claude-ai-toolchain-integration)
9. [API & Integration Architecture](#9-api--integration-architecture)
10. [Alternative Options Analysis](#10-alternative-options-analysis)
11. [Security, Reliability & Scalability](#11-security-reliability--scalability)
12. [MVP Plan — 6-Week Sprint](#12-mvp-plan--6-week-sprint)

---

## 1. Complete Tool Inventory

This section lists every tool in the stack with purpose, tier, cost, and justification. This is the definitive reference before any implementation decision.

---

### 1.1 Primary AI / Reasoning Tools

| Tool | Version / Tier | Cost | Role in System | Why This Tool |
|---|---|---|---|---|
| **Claude API** | claude-sonnet-4-6 (primary), claude-haiku-4-5 (fast tasks) | Pay-per-token via Anthropic | Primary reasoning LLM for all agents: research synthesis, content writing, fact-checking, style scoring | Superior reasoning quality; native MCP support; better instruction-following for structured outputs; Markdown-native responses |
| **Claude Code** | CLI tool, free | $0 (uses Claude API quota) | Generate, test, and run Python scripts for data processing, chart generation, pipeline orchestration code, and ad-hoc automation | Agentic coding without manual scripting; can write and execute Matplotlib chart code; ideal for analytics scripts |
| **Claude MCP Servers** | Open-source, self-hosted | $0 | Extend Claude agents with real tools: web fetch, file system, Google Drive, browser automation | Turns Claude from a text generator into an agent that can actually read web pages, verify URLs, write files, and interact with external systems |
| **Claude Cowork** | Desktop app (beta) | Included with Anthropic subscription | Human-AI collaboration interface on desktop for file review, batch approval workflows, and document management | Reduces human review time; Claude can pre-annotate content packages for faster human sign-off; desktop access = no browser switching |
| **Google Gemini 2.5 Pro** | Enterprise API via work | $0 (via work allocation) | Fallback LLM; Gemini Code Execution for chart/visual generation; used when Gemini-specific tools are advantageous | Free via work; Gemini Code Execution is excellent for sandboxed Python execution without local setup |
| **Google Gemini 2.5 Flash** | Enterprise API via work | $0 (via work allocation) | Backup for high-volume, low-complexity tasks (formatting, templating) when Anthropic rate limits are hit | Cost-effective fallback; same work API key |

---

### 1.2 Agentic Orchestration Framework

| Tool | Version | Cost | Role | Why |
|---|---|---|---|---|
| **CrewAI** | Latest stable (0.x) | $0 (open-source) | Multi-agent orchestration framework; defines agent roles, tools, task sequences, and crew execution | Role-based model maps directly to content workflow (Researcher, Writer, Fact-Checker, etc.); lower learning curve than LangGraph; native support for Claude API via LiteLLM |
| **LiteLLM** | Latest | $0 (open-source) | Universal LLM proxy layer; allows CrewAI to call Claude, Gemini, or any other LLM through a single standardized interface | Critical for multi-LLM strategy; swap between Claude and Gemini without changing agent code; handles rate limit routing automatically |

---

### 1.3 MCP Servers (Claude Tool Extensions)

MCP (Model Context Protocol) servers are the mechanism by which Claude agents interact with the real world. Each MCP server adds a category of capabilities to Claude without custom code.

| MCP Server | Hosted Where | Cost | Capabilities Added | Used By |
|---|---|---|---|---|
| **`@modelcontextprotocol/server-fetch`** | n8n server (npm) | $0 | Fetch live web URLs; extract text content; follow redirects | Fact-Checker agent — verifies source URLs are live and extracts data |
| **`@modelcontextprotocol/server-filesystem`** | n8n server (npm) | $0 | Read/write files in configured directories; list directory contents | All agents — read config `.md` files; write research data, draft content, audit logs |
| **`@modelcontextprotocol/server-google-drive`** | n8n server (npm) | $0 | List, read, and write Google Drive files and folders | Visual Designer — save PNG assets; Config Backup workflow |
| **`mcp-server-playwright`** | n8n server (npm) | $0 | Headless browser automation; screenshot capture; JavaScript-rendered page scraping | Research Agent — scrape BBS and Bangladesh Bank portals that require JS rendering |
| **`@modelcontextprotocol/server-brave-search`** | n8n server (npm) | $3/mo (Brave API) | Web search with factual, privacy-focused results | Content Strategist — find trending Bangladesh topics; Research Agent — discover new sources |
| **`mcp-server-github`** | n8n server (npm) | $0 | Read/write GitHub repos; create commits; read file history | Config update workflow — commits approved config changes with human approval message |
| **`mcp-server-slack`** | n8n server (npm) | $0 | Send messages, create interactive blocks, listen for responses | Human Review Notifier — send content packages with approval buttons |
| **`mcp-server-google-sheets`** | n8n server (npm) | $0 | Read and write Google Sheets data programmatically | All workflow agents — read topic queue; log publication data; write analytics |

---

### 1.4 Workflow Orchestration

| Tool | Version | Cost | Role | Why |
|---|---|---|---|---|
| **n8n** | Self-hosted (Docker) | $6/mo (DO droplet) | Visual workflow automation; triggers, scheduling, API calls, conditional logic, webhook handling | Open-source; 400+ integrations; visual debugging; can spawn Python subprocesses (CrewAI crews) |
| **Docker + Docker Compose** | Latest | $0 | Container runtime for n8n, MCP servers, and CrewAI processes on Digital Ocean droplet | Reproducible environments; easy updates; isolates services |
| **Digital Ocean Droplet** | 2 vCPU / 4GB RAM (Basic) | $18/mo (upgraded from $6 to handle MCP servers) | Cloud VPS hosting all self-hosted components | Cost-effective; reliable; simple setup; SSH access |

> **Note on hosting cost:** The original PRD budgeted $6/mo for a 1 vCPU / 1GB droplet. Running n8n + Docker + multiple MCP servers + CrewAI requires at least 2 vCPU / 4GB RAM. Budget updated to $18/mo.

---

### 1.5 Data Storage & Management

| Tool | Role | Cost | Format Preference | Notes |
|---|---|---|---|---|
| **Google Sheets** | Content queue, publication log, analytics, error log | $0 | Tabular (unavoidable) | Primary human-editable data store; 4 tabs |
| **Google Drive** | Visual asset storage; document archive | $0 | PNG, MD, PDF | Free 15GB; use Drive folders organized by date |
| **GitHub (private repo)** | Version control for all config files and code | $0 | **Markdown** (`.md`) | All configs live here; Git history = change audit |
| **Local Filesystem (on droplet)** | Temp files during pipeline execution | $0 | Markdown, PNG | Cleaned up after each successful pipeline run |

---

### 1.6 Visual Content Generation

| Tool | Cost | Quality | Use Case |
|---|---|---|---|
| **Claude Code + Matplotlib** | $0 (uses Claude API) | ⭐⭐⭐ Good | MVP visual generation — Claude Code writes and executes Python chart scripts |
| **Gemini Code Execution** | $0 (via work) | ⭐⭐⭐ Good | Alternative/fallback for visual generation; sandboxed Python environment |
| **Templated.io API** | $29/mo | ⭐⭐⭐⭐⭐ Professional | Phase 3+ upgrade for branded infographic templates |
| **Canva API** | $13/mo (Pro) | ⭐⭐⭐⭐ Very Good | Alternative to Templated.io; better design ecosystem |

---

### 1.7 Publication & Distribution

| Tool | Cost | Authentication | Rate Limits | Notes |
|---|---|---|---|---|
| **Instagram Graph API** | $0 | OAuth 2.0 (60-day token) | 200 calls/hour | Requires Facebook Business account; images must be hosted URL |
| **Facebook Pages API** | $0 | Same OAuth app as Instagram | 200 calls/hour | Same Meta Developer App handles both |
| **WordPress REST API** | $0 | Application Password | No practical limit | Optional; post-MVP |
| **Substack API** | $0 | API key | No public limit | Alternative blog platform; simpler than WordPress |

---

### 1.8 Human Interface & Review Tools

| Tool | Cost | Role | Integration |
|---|---|---|---|
| **Slack** | Free tier | Human review notifications; error alerts; approval action buttons | n8n Slack node + MCP Slack server |
| **Claude Cowork** | Included with Anthropic plan | Desktop review interface for batch content approval; file management | Reads from Google Drive / local filesystem |
| **Google Sheets** | $0 | Topic queue management; weekly review UI for human | n8n reads/writes; human edits directly |
| **GitHub Web UI** | $0 | Config file review and approval; monthly optimization review | Human approves PRs for config changes |

---

### 1.9 Development & Debugging Tools

| Tool | Cost | Role |
|---|---|---|
| **Claude Code (CLI)** | $0 | Write pipeline scripts, debug agent outputs, generate test data, create Matplotlib templates |
| **Python 3.11+ / venv** | $0 | Runtime for CrewAI and all agent scripts |
| **Git CLI** | $0 | Version control; commit config changes |
| **n8n Execution Logs** | $0 | Visual pipeline debugging |
| **Brave Search API** | $3/mo | Topic discovery and news research |

---

### 1.10 Cost Summary (Updated)

| Component | Monthly Cost | Notes |
|---|---|---|
| Digital Ocean Droplet (2vCPU/4GB) | $18 | Upgraded from $6 to support full stack |
| Brave Search API | $3 | MCP web search for Research Agent |
| Templated.io (Phase 3+) | $29 | Deferred to Month 3; $0 in MVP |
| Anthropic Claude API | ~$15-25 | Estimated for 60 posts/month at Sonnet pricing |
| Gemini API | $0 | Via work enterprise access |
| All other tools | $0 | Open-source or free tiers |
| **MVP Total (first 2 months)** | **~$36–46/mo** | Without Templated.io |
| **Full Stack Total** | **~$65–75/mo** | With Templated.io from Month 3 |

> The PRD's "$6/month minimum" target is not achievable with a robust MCP + Claude setup. The realistic minimum for a reliable system is ~$36/month. The $42.60/month Gemini API estimate from the PRD is replaced by ~$20/month Claude API cost, which is comparable.

---

## 2. Architectural Philosophy

### 2.1 Three-Layer Model

The platform is organized into three vertically integrated layers:

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: HUMAN LAYER                                       │
│  Google Sheets (topics) · Slack (review) · Cowork (files)  │
│  GitHub Web (config approval) · 3 touchpoints/week          │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: WORKFLOW LAYER (n8n)                              │
│  Scheduling · API calls · Formatting · Publishing · Logging │
│  9 deterministic workflows · No reasoning decisions         │
├─────────────────────────────────────────────────────────────┤
│  LAYER 1: AGENT LAYER (CrewAI + Claude API + MCP)          │
│  Research · Write · Fact-check · Style · Visual · Reflect  │
│  6 specialized agents · All reasoning happens here          │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Core Design Principles

**Trust Pipeline First.** No content is published without clearing four automated quality gates AND one human approval. These gates are structural — not optional — and cannot be bypassed even via manual override (only via explicit human rejection of a gate outcome, which is logged).

**Markdown as the Universal Language.** All configuration, all agent outputs, all audit logs, all reports, and all inter-agent communication use Markdown. This makes every artifact human-readable, Git-diffable, and editable without special tools. JSON is only used where a third-party API explicitly requires it (and is always generated from a Markdown source at runtime).

**Claude as the Primary Reasoning Engine.** Claude (via Anthropic API) handles all tasks requiring judgment: evaluating source quality, writing bilingual content, scoring style compliance, and synthesizing analytics insights. Gemini is retained as a fallback and for Gemini Code Execution (visual generation), which is a uniquely strong capability.

**MCP as the Nervous System.** MCP servers give Claude agents the ability to interact with the real world — reading live web pages, writing files, searching the web, and committing to Git. Without MCP, Claude is text-in/text-out. With MCP, it becomes a true autonomous agent.

**Separation of Concerns.** Agents reason. Workflows execute. Humans decide strategy. These responsibilities never cross.

---

## 3. Macro Architecture

### 3.1 System Context

```
EXTERNAL DATA SOURCES                DISTRIBUTION CHANNELS
┌──────────────┐                     ┌──────────────────┐
│ BBS.gov.bd   │                     │ Instagram        │
│ Bangladesh   │◄── Research ──┐     │ Facebook Pages   │
│ Bank         │               │     │ Blog (optional)  │
│ World Bank   │               │     └──────────────────┘
│ UNESCO UIS   │               │              ▲
└──────────────┘               │              │
                               │    ┌─────────────────────────┐
AI SERVICES                    │    │   PLATFORM CORE         │
┌──────────────┐               │    │                         │
│ Claude API   │◄─── Agents ───┤    │  Layer 1: Agent Crew    │
│ (Anthropic)  │               │    │  Layer 2: n8n Workflows │
│ Gemini API   │◄─── Fallback ─┘    │  Layer 3: Human HITL   │
│ (Google Work)│                    └─────────────────────────┘
└──────────────┘                              ▲
                                              │
HUMAN INTERFACES                   CONFIG & VERSION CONTROL
┌──────────────┐                   ┌──────────────────┐
│ Slack        │◄── Review ────────│ GitHub (private) │
│ Google Sheets│◄── Topic Queue ───│ Markdown configs │
│ Claude Cowork│◄── File Review ───│ Audit logs (.md) │
└──────────────┘                   └──────────────────┘
```

### 3.2 Master Data Flow

```
[HUMAN] Add topic to Google Sheets
           │
           ▼
[WF-01] Topic Queue Sync (Monday 6am cron)
  → Reads "Approved" topics from Sheets
  → Passes topic_id to Pipeline Orchestrator
           │
           ▼
[WF-02] Pipeline Orchestrator
  → Spawns CrewAI crew as Python subprocess
           │
    ┌──────┴──────────────────────────────────────────┐
    │              CREWAI CREW                         │
    │                                                  │
    │  [Agent 1: Content Strategist]                   │
    │    ↓ Approved topic + MCP web search             │
    │  [Agent 2: Research Agent]                       │
    │    ↓ Structured research data (.md)              │
    │  ──── GATE 1: Research Quality Check ────        │
    │  [Agent 3: Content Writer]                       │
    │    ↓ Draft content (.md)                         │
    │  [Agent 4: Fact-Checker]                         │
    │    ↓ Fact-check report (.md)                     │
    │  ──── GATE 2: Fact-Check Validation ────         │
    │  [Agent 5: Style Checker]                        │
    │    ↓ Style compliance report (.md)               │
    │  ──── GATE 3: Style Compliance Check ────        │
    │  [Agent 6: Visual Designer]                      │
    │    ↓ PNG assets + visual report (.md)            │
    │  ──── GATE 4: Brand Compliance Check ────        │
    │                                                  │
    └──────────────────────────────────────────────────┘
           │
           ▼
[WF-03] Human Review Notifier
  → Compiles content package
  → Sends Slack message with action buttons
           │
    ┌──────┴────────────────────────────────┐
    │         [HUMAN TOUCHPOINT 2]          │
    │  Approve │ Request Changes │ Reject   │
    └──────┬───────────────┬───────────────┘
           │ Approve        │ Request Changes
           ▼                ▼
[WF-04] Publisher    [Return to specific agent]
  → Instagram API      → Re-enter crew at
  → Facebook API         correct stage
  → Log to Sheets
           │
           ▼
[WF-05] Analytics Fetcher (daily cron)
  → Fetch engagement metrics
  → Write to Sheets
           │
[Monthly] Reflection Agent
  → Generate insights .md report
  → Human approves config changes via GitHub PR
```

### 3.3 Quality Gate Summary

| Gate | Triggered After | Pass Criterion | Failure Action | Max Retries |
|---|---|---|---|---|
| Gate 1: Research Quality | Research Agent | 100% citations, confidence ≥ medium | Flag to human with issue report | N/A — escalate |
| Gate 2: Fact-Check | Fact-Checker Agent | ≥95% pass rate, 0 discrepancies | Return to Writer with corrections | 2 retries → human |
| Gate 3: Style Compliance | Style Checker Agent | ≥85% style score | Auto-correct if 80-84; retry Writer if <80 | 2 retries → human |
| Gate 4: Brand Compliance | Visual Designer Agent | All brand elements present | Retry visual agent | 1 retry → human |

---

## 4. Micro Architecture — Agent Layer

### 4.1 CrewAI Setup Overview

```python
# High-level crew structure (pseudocode)
crew = Crew(
    agents=[strategist, researcher, writer, fact_checker, style_checker, visual_designer],
    tasks=[
        ideation_task,
        research_task,
        writing_task,
        fact_check_task,
        style_check_task,
        visual_task
    ],
    process=Process.sequential,
    memory=True,
    verbose=True,  # All reasoning steps logged to audit .md file
    output_log_file="audit/pipeline_run_{topic_id}_{timestamp}.md"
)
```

All agents use Claude API via LiteLLM as their primary LLM:

```python
from litellm import completion

# Claude Sonnet for reasoning-heavy agents
llm_primary = "anthropic/claude-sonnet-4-6"

# Claude Haiku for fast, cheap tasks
llm_fast = "anthropic/claude-haiku-4-5-20251001"

# Gemini fallback
llm_fallback = "gemini/gemini-2.5-flash"
```

---

### 4.2 Agent 1: Content Strategist

**Purpose:** Weekly editorial planning and automated topic suggestion generation.

| Property | Value |
|---|---|
| **LLM** | claude-haiku-4-5 (light reasoning task) |
| **Execution** | Weekly cron (Monday 6am) + on-demand for urgent topics |
| **MCP Tools** | `brave-search` (trending BD topics), `filesystem` (read editorial_preferences.md), `google-sheets` (read last 30 days published topics) |
| **Memory** | Last 30 days of published topic IDs (prevents duplication) |
| **Output Format** | `content/topic_suggestions_{week}.md` |

**Behavior:**
- Searches Brave for recent Bangladesh news, economic releases, political anniversaries
- Cross-references against published topics (via MCP Google Sheets) to avoid repetition
- Reads `config/editorial_preferences.md` to filter out banned topic categories
- Generates exactly 10 suggestions with research hints per suggestion
- Writes output as a Markdown file to Google Drive for human review

**Output Markdown format:**

```markdown
# Topic Suggestions — Week {N}, {Year}

Generated: {timestamp}
Brave Search queries used: {list}

---

## Suggestion 1 — {Title in English}

**বাংলা শিরোনাম:** {Title in Bangla}
**Priority Signal:** High | GDP data release this week
**Suggested Sources:**
- BBS: https://...
- World Bank: https://...
**Research Hints:** Focus on 2015-2024 trend; compare pre/post 2018 policy shift
**Sensitivity:** Low
**Estimated Research Difficulty:** Medium

---

## Suggestion 2 ...
```

---

### 4.3 Agent 2: Research Agent

**Purpose:** Autonomous, multi-source data collection with full provenance tracking.

| Property | Value |
|---|---|
| **LLM** | claude-sonnet-4-6 (complex source evaluation, data interpretation) |
| **MCP Tools** | `fetch` (live URL retrieval), `playwright` (JS-rendered portals), `filesystem` (write research output), `brave-search` (discover alternative sources) |
| **PRA Loop** | Perceive → Reason → Act → Reflect → Adapt |
| **Output Format** | `research/{topic_id}_research.md` |

**Source Priority Hierarchy:**

```
Tier 1 (Authoritative):  BBS.gov.bd · Bangladesh Bank · Ministry of Finance
Tier 2 (International):  World Bank · IMF · UNESCO UIS · UNDP · ADB
Tier 3 (Secondary):      Academic papers · Daily Star data journalism
Tier 4 (Never cite):     Social media · Unverified blogs · Wikipedia
```

**Output Markdown format:**

```markdown
# Research Data — {Topic Title}

**Topic ID:** {id}
**Research Agent Run:** {timestamp}
**Research Duration:** {X} minutes
**Overall Confidence:** High | Medium | Low

---

## Data Points

### Data Point 1: GDP Growth Rate 2023
- **Value:** 5.78%
- **Unit:** Percentage (annual growth)
- **Year:** 2023
- **Source Name:** World Bank Open Data
- **Source URL:** https://data.worldbank.org/...
- **Verification:** Cross-referenced with Bangladesh Bank Annual Report 2023 ✓
- **Confidence:** High
- **Notes:** BBS preliminary estimate was 5.82%; World Bank revised figure used

### Data Point 2: ...

---

## Methodology Notes

- BBS portal required Playwright (JS-rendered table) for data extraction
- 2019 data point unavailable from Tier 1 sources; interpolated using linear regression between 2018 (5.2%) and 2020 (3.5%); flagged as interpolated
- All PDFs processed via MCP fetch + Claude PDF understanding

---

## Quality Self-Assessment

- [ ] All data points have source URLs: YES
- [ ] Minimum 2 sources cross-referenced for key stats: YES
- [ ] Outliers investigated: YES (see note on 2019)
- [ ] Confidence ≥ medium for all points: YES
- **Gate 1 Result: PASS**
```

---

### 4.4 Agent 3: Content Writer

**Purpose:** Generate bilingual (Bangla-English) content matching the user's style profile.

| Property | Value |
|---|---|
| **LLM** | claude-sonnet-4-6 (creative writing + bilingual generation) |
| **MCP Tools** | `filesystem` (read research .md, read style guide .md, read example posts) |
| **Style Profile Input** | `config/writing_style_profile.md` (loaded fresh each run) |
| **Output Formats** | Instagram caption · Facebook post · Blog draft (all in `.md`) |
| **Language Target** | 70% Bangla body · 30% English technical terms · Headlines 60/40 |

**Output Markdown format:**

```markdown
# Content Draft — {Topic Title}

**Topic ID:** {id}
**Writer Agent Run:** {timestamp}
**Language Ratio (self-assessed):** Bangla 71% / English 29%
**Style Match Score (self-assessed):** 87/100

---

## Instagram Caption

{Full bilingual caption in Bangla/English mix}

**Engagement Question:** {question at end}
**Hashtags:** #বাংলাদেশ #Bangladesh #DataDriven ...
**Source Line:** তথ্যসূত্র: World Bank (2023), BBS Annual Report (2022)
**Character Count:** 1,847 / 2,200

---

## Facebook Post

{Slightly longer version with additional context}

---

## Blog Draft Outline

### Introduction
...
### Section 1: {Title}
**Data Point Reference:** [DP-1] GDP Growth Rate 2023 — 5.78% (World Bank)
...

---

## Writing Notes

- Used "তথ্য" (not "ডেটা") per style guide vocabulary rules
- Avoided passive voice constructions per style guide
- Engagement question placed as final line per format rules
- 3 surprising/counterintuitive facts included per style guide engagement pattern
```

---

### 4.5 Agent 4: Fact-Checker

**Purpose:** Verify every numerical claim in the draft against live source documents.

| Property | Value |
|---|---|
| **LLM** | claude-sonnet-4-6 (document comprehension, numerical comparison) |
| **MCP Tools** | `fetch` (retrieve source URLs live), `playwright` (JS-heavy sources), `filesystem` (read draft .md, write fact-check report .md) |
| **Verification Method** | Fetches each cited source URL; extracts figures; compares with draft claims |
| **Confidence Levels** | `exact_match` · `within_rounding` · `plausible_interpolated` · `unverifiable` · `mismatch` |
| **Output Format** | `reports/factcheck_{topic_id}.md` |

**Output Markdown format:**

```markdown
# Fact-Check Report — {Topic Title}

**Topic ID:** {id}
**Fact-Checker Run:** {timestamp}
**Overall Result:** PASS | FAIL
**Pass Rate:** 97% (29/30 claims verified)

---

## Claim Verification Results

### Claim 1 ✅
- **Claim in Draft:** "২০২৩ সালে বাংলাদেশের GDP প্রবৃদ্ধি ছিল ৫.৭৮%"
- **Source URL Checked:** https://data.worldbank.org/...
- **Extracted Value:** 5.78%
- **Status:** `exact_match`
- **Confidence:** High

### Claim 2 ⚠️
- **Claim in Draft:** "শিক্ষা খাতে বরাদ্দ ছিল জিডিপির ২.১%"
- **Source URL Checked:** https://mof.gov.bd/...
- **Extracted Value:** 2.09%
- **Status:** `within_rounding` — draft says 2.1%, source says 2.09%
- **Correction Applied:** Changed to "প্রায় ২.১%" (approximately) to be accurate
- **Confidence:** High

### Claim 3 ❌
- **Claim in Draft:** "১৯৯৬ সালে বাজেট ঘাটতি ছিল ৪.৩%"
- **Source URL Checked:** https://... (404 error)
- **Alternative Checked:** Bangladesh Bank archive PDF
- **Status:** `unverifiable` — source link broken, alternative incomplete
- **Action:** Flagged for human review; do not publish this specific claim without verification
- **Confidence:** Low

---

## Corrections Applied Automatically: 1
## Claims Requiring Human Review: 1
## Gate 2 Result: CONDITIONAL PASS — human review required for Claim 3
```

---

### 4.6 Agent 5: Style Checker

**Purpose:** Score the draft against the writing style profile on 10 dimensions.

| Property | Value |
|---|---|
| **LLM** | claude-haiku-4-5 (scoring task; cheaper) |
| **MCP Tools** | `filesystem` (read draft .md, style guide .md, example posts) |
| **Scoring Dimensions** | Tone (20%), B-E Ratio (20%), Engagement Hook (15%), Vocab Rules (10%), Structure (10%), Formality (10%), Source Format (10%), Headline (5%) |
| **Thresholds** | ≥85 = Pass · 80-84 = Auto-correct · 75-79 = Retry Writer · <75 = Human |
| **Output Format** | `reports/stylecheck_{topic_id}.md` |

**Output Markdown format:**

```markdown
# Style Compliance Report — {Topic Title}

**Topic ID:** {id}
**Style Checker Run:** {timestamp}
**Overall Score:** 88/100
**Gate 3 Result:** PASS

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Notes |
|---|---|---|---|---|
| Tone (informative, not preachy) | 20% | 90 | 18.0 | Good — neutral throughout |
| Bangla-English Ratio | 20% | 85 | 17.0 | 71%/29% — within 70±5% target |
| Engagement Hook | 15% | 95 | 14.25 | Strong question at end |
| Vocabulary Rules | 10% | 80 | 8.0 | Used "ডেটা" once; corrected to "তথ্য" |
| Structure | 10% | 85 | 8.5 | Good flow |
| Formality Level | 10% | 90 | 9.0 | Semi-formal, appropriate |
| Source Citation Format | 10% | 90 | 9.0 | All stats cited correctly |
| Headline Style | 5% | 80 | 4.0 | Minor — headline slightly long |
| **TOTAL** | **100%** | — | **87.75** | **PASS** |

---

## Deviations Found

1. **Line 12:** Used "ডেটা" — corrected to "তথ্য" per vocabulary rules ✅ (auto-fixed)
2. **Headline:** 18 words (guideline: <15) — rewritten ✅ (auto-fixed)

## Auto-Corrections Applied: 2
```

---

### 4.7 Agent 6: Visual Designer

**Purpose:** Generate branded infographic assets using Claude Code + Matplotlib.

| Property | Value |
|---|---|
| **LLM** | claude-sonnet-4-6 (decides chart type, layout strategy, writes Matplotlib code) |
| **Execution Method** | Claude Code generates Python script → Python subprocess executes it → PNG saved |
| **Fallback** | Gemini Code Execution (if Claude Code unavailable) |
| **MCP Tools** | `filesystem` (read research .md, visual identity .md, write PNG path), `google-drive` (upload PNG) |
| **Output Formats** | Instagram 1080×1080px · Facebook 1200×630px |
| **Output Format** | `reports/visual_{topic_id}.md` + PNG files |

**Visual Decision Logic (Claude reasoning):**

```
If data_points > 5 AND temporal:       → Line chart
If data_points <= 3 AND comparative:   → Bar chart  
If single_key_stat AND high_impact:    → Data Card (large number)
If sequential events:                   → Timeline
If two groups compared:                → Side-by-side comparison
```

**Claude Code generates scripts like:**

```python
# Generated by Claude Code for topic: GDP Growth 2024
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Brand colors from visual_identity.md
GREEN = "#006A4E"    # Bangladesh Green
RED = "#F42A41"      # Liberation Red
BG = "#FAFAFA"

fig, ax = plt.subplots(figsize=(10.8, 10.8), dpi=100)
fig.patch.set_facecolor(BG)
# ... chart code ...
# Watermark / source citation
ax.text(0.5, 0.02, "তথ্যসূত্র: World Bank (2023) | @BDDataStory",
        ha="center", fontsize=9, color="#888888", transform=fig.transFigure)
plt.savefig("output/instagram_{topic_id}.png", bbox_inches="tight", dpi=100)
```

**Visual Report Markdown format:**

```markdown
# Visual Asset Report — {Topic Title}

**Topic ID:** {id}
**Visual Designer Run:** {timestamp}
**Chart Type Selected:** Line Chart (temporal, 8 data points)
**Reasoning:** GDP growth trend 2015-2023; temporal data suits line chart; highlights peak 2017 and COVID dip 2020

---

## Generated Assets

| Platform | File | Dimensions | File Size |
|---|---|---|---|
| Instagram | `visuals/{id}_ig.png` | 1080×1080px | 312KB |
| Facebook | `visuals/{id}_fb.png` | 1200×630px | 287KB |

## Brand Compliance Check

- [x] Primary color #006A4E used for main line: YES
- [x] Source watermark present: YES
- [x] Noto Sans Bengali font for Bangla text: YES
- [x] File size < 1MB: YES (312KB, 287KB)
- [x] Brand logo/handle included: YES

**Gate 4 Result: PASS**
```

---

### 4.8 Agent 7: Reflection Agent (Monthly)

**Purpose:** Analyze 30 days of performance data and propose system optimizations.

| Property | Value |
|---|---|
| **LLM** | claude-sonnet-4-6 |
| **Execution** | First Monday of each month |
| **MCP Tools** | `google-sheets` (read analytics tab), `filesystem` (read all config .md files, write optimization report) |
| **Output Format** | `reports/monthly_reflection_{month}_{year}.md` |
| **Human Action** | Review report; approve config changes via GitHub PR |

---

## 5. Micro Architecture — Workflow Layer

### 5.1 Workflow Inventory

| ID | Workflow Name | Trigger | Layer Interaction | Runtime |
|---|---|---|---|---|
| WF-01 | Topic Queue Sync | Cron: Mon 6am | Reads Sheets → Invokes Strategist Agent → Writes back | ~5 min |
| WF-02 | Pipeline Orchestrator | Webhook from WF-01 | Spawns CrewAI subprocess → Monitors completion | ~30-45 min |
| WF-03 | Human Review Notifier | Webhook from WF-02 (on success) | Packages MD files → Sends Slack with buttons | ~2 min |
| WF-04 | Multi-Platform Publisher | Webhook (Slack approval button) | Formats for each platform → Posts via APIs → Logs to Sheets | ~60 sec |
| WF-05 | Analytics Fetcher | Cron: Daily 11pm | IG Insights API → FB Insights API → Write to Sheets | ~5 min |
| WF-06 | Error Alert Handler | Webhook (any agent error) | Parse error → Route to Slack channel → Log to Sheets | ~30 sec |
| WF-07 | Monthly Report Trigger | Cron: 1st Mon of month | Invokes Reflection Agent → Sends report to human | ~15 min |
| WF-08 | Config Backup | Cron: Daily midnight | Git pull → Copy configs → Drive backup | ~2 min |
| WF-09 | Health Monitor | Cron: Every 6 hours | Ping Claude API · Gemini API · n8n · Sheets · GitHub | ~30 sec |

---

### 5.2 WF-02 Pipeline Orchestrator — Step Detail

```
WF-02: PIPELINE ORCHESTRATOR
─────────────────────────────────────────────────────────────────
Step 1:  Receive {topic_id} via webhook from WF-01
Step 2:  Read topic metadata from Google Sheets
Step 3:  Initialize pipeline context (topic_id, timestamp, status=running)
Step 4:  Spawn CrewAI crew as Python subprocess
         └── Pass: topic_id, config paths, output directory
Step 5:  Monitor subprocess (poll every 60 seconds)
         └── On success: Read output MD files from filesystem
         └── On timeout (>60 min): Kill subprocess, trigger WF-06
Step 6:  Parse Gate results from agent MD reports
         └── Gate 1 FAIL → Trigger WF-06 (research issue)
         └── Gate 2 FAIL after 2 retries → Trigger WF-06
         └── Gate 3 FAIL after 2 retries → Trigger WF-06
         └── Gate 4 FAIL after 1 retry → Trigger WF-06
Step 7:  All gates PASS → Package content for review
         └── Collect: draft.md, factcheck.md, stylecheck.md, visual.md, PNG files
Step 8:  Trigger WF-03 with content package path
Step 9:  Update Google Sheets status to "In Review"
─────────────────────────────────────────────────────────────────
```

---

### 5.3 Dry-Run Mode

Every workflow supports a `dry_run=true` parameter that:
- Runs the full pipeline including all agents
- Does NOT post to Instagram or Facebook
- Does NOT log to the production Published sheet (logs to test tab)
- Delivers content package to Slack with `[DRY RUN]` label
- Allows full QA testing without audience-facing side effects

Activated by setting `DRY_RUN=true` in n8n workflow variables, or by adding `[TEST]` prefix to topic title in Google Sheets.

---

## 6. Micro Architecture — Human Layer

### 6.1 Touchpoint 1: Weekly Topic Queue (Monday, ~30 min)

**Interface:** Google Sheets `Content_Queue` tab + Claude Cowork (optional)

The Content Strategist agent pre-populates a `topic_suggestions_{week}.md` file in Google Drive each Monday. Claude Cowork can be used to review this file on desktop — Claude can highlight which suggestions are most data-rich and flag any that may be politically sensitive before the human reviews the Sheets queue.

**Google Sheets Schema:**

| Column | Type | Who Fills | Description |
|---|---|---|---|
| Topic_ID | Auto (T001...) | System | Unique identifier |
| Topic_Bangla | Text | Human / AI | Title in Bangla |
| Topic_English | Text | Human / AI | Title in English |
| Priority | High / Med / Low | Human | Processing order |
| Context_Notes | Free text | Human | Passed verbatim to Research Agent |
| Suggested_Sources | URL list | AI | Pre-identified by Strategist |
| Deadline | Date | Human | Target publish date |
| Status | Dropdown | Both | Queue / Approved / In-Progress / Review / Published / Rejected |
| Sensitivity | Checkbox | Human | Triggers 99% fact-check threshold |
| Dry_Run | Checkbox | Human | Runs pipeline without publishing |
| Week | Auto | System | Week number |

---

### 6.2 Touchpoint 2: Content Review (Daily, ~5 min/post)

**Interface:** Slack notification (primary) + Claude Cowork (file review)

**Slack Review Package Contents:**

```
🇧🇩 Content Ready for Review — {Topic Title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📸 Preview: [thumbnail image attached]
📝 Caption Preview: {first 200 chars of caption}
📊 Quality Scores:
   Fact-Check:  ✅ 97% pass (29/30 claims)
   Style Score: ✅ 88/100
   Brand Check: ✅ PASS
   
📌 Sources Used: 3 sources (World Bank, BBS, BD Bank)
⚠️  Notes: 1 claim marked unverifiable — check Claim 3 in fact-check report

📁 Full Package: [Google Drive link]

[✅ Approve & Publish]  [✏️ Request Changes]  [❌ Reject]
```

When "Request Changes" is selected, a text input appears for specific feedback. This feedback is passed directly to the relevant agent's prompt as additional context.

**Claude Cowork Integration:** The full content package (all `.md` files + PNG) is accessible in Cowork. Claude can answer questions like "summarize what the fact-checker flagged" or "does this caption match the style guide?" without the human reading raw files.

---

### 6.3 Touchpoint 3: Monthly Optimization (1st Monday, ~1-2 hrs)

**Interface:** GitHub Pull Request + Claude Cowork

The Reflection Agent writes a `monthly_reflection_{month}.md` report and opens a GitHub Pull Request that modifies config files (e.g., updates vocabulary rules, adjusts source priority list). The human reviews the PR diff in GitHub, approves or rejects individual changes inline using GitHub review comments, and merges or closes the PR.

This pattern means:
- Every config change is reviewed by a human before it takes effect
- Git history provides a full audit trail of every system optimization decision
- Reverting a bad change is a simple `git revert`

---

## 7. Markdown-First Configuration System

All system configuration lives as Markdown files in the private GitHub repository. No JSON config files. Agents read these files via MCP `filesystem` tool on every execution.

### 7.1 Config File Map

```
/config/
├── writing_style_profile.md      # Agent 3: Content Writer + Agent 5: Style Checker
├── visual_identity.md             # Agent 6: Visual Designer
├── editorial_preferences.md       # Agent 1: Strategist + Agent 2: Research
├── source_priority.md             # Agent 2: Research Agent
├── fact_check_protocols.md        # Agent 4: Fact-Checker
└── platform_formatting.md         # WF-04: Publisher formatting rules
```

### 7.2 Example: `writing_style_profile.md`

```markdown
# Writing Style Profile

Last Updated: {date}
Updated By: {human name} via monthly optimization review

---

## Voice Characteristics

- **Tone:** Informative yet conversational — like a knowledgeable friend explaining data
- **Formality:** Semi-formal (not academic, not casual)  
- **Persona:** Curious data researcher, never political commentator
- **Core Promise:** Every claim is backed by a cited source

---

## Language Mix Rules

| Content Element | Bangla % | English % | Notes |
|---|---|---|---|
| Headlines | 60% | 40% | English technical terms allowed |
| Body text | 70% | 30% | Bangla preferred for narrative |
| Numbers/stats | — | 100% | Always Arabic numerals |
| Source citations | 30% | 70% | Format: [Source: URL] |

---

## Vocabulary Rules

### Always Use
- "তথ্য" (not "ডেটা") for "data"
- "প্রবৃদ্ধি" (not "গ্রোথ") for "growth"

### Never Use
- Inflammatory or partisan language
- Superlatives without data support ("best", "worst" unless data-backed)
- Passive voice where active is clearer

---

## Structure Rules

1. Lead with the most surprising/counterintuitive data point
2. Provide 3-5 supporting data points with inline citations
3. Add 1 sentence of historical context per major claim
4. End with an engagement question to audience
5. Source citation line always last (before hashtags)

---

## Engagement Hooks

Always include one of:
- A counterintuitive finding ("এই তথ্যটি আপনাকে অবাক করবে...")
- A direct question to the audience
- A comparison to a familiar reference point

---

## Example Posts I Love

### Example 1
{paste actual example post here — verbatim}

### Example 2
{paste actual example post here — verbatim}
```

### 7.3 Example: `visual_identity.md`

```markdown
# Visual Identity Guide

Last Updated: {date}

---

## Color Palette

| Color Name | Hex | Usage |
|---|---|---|
| Bangladesh Green | `#006A4E` | Primary — headers, key stats, chart lines |
| Liberation Red | `#F42A41` | Accent — important dates, alerts, highlights |
| Off-White Background | `#FAFAFA` | Card backgrounds |
| Dark Text | `#1A1A2E` | Body text |
| Medium Gray | `#666666` | Labels, secondary text |

---

## Typography

| Use Case | Font | Weight | Size |
|---|---|---|---|
| Bangla text | Noto Sans Bengali | Regular / Bold | 16-24px |
| English text | Inter | Regular / SemiBold | 14-20px |
| Data callout numbers | Inter | Bold | 48-72px |
| Source attribution | Inter | Regular | 10px |

---

## Template Types

| Template | Use When | Dimensions |
|---|---|---|
| Data Card | Single key statistic | 1080×1080 (IG), 1200×630 (FB) |
| Line Chart | Trend over time (≥4 data points) | Same |
| Bar Chart | Category comparison (≤6 categories) | Same |
| Timeline | Sequence of events | Same |
| Side-by-Side | Two-group comparison | Same |

---

## Mandatory Elements

Every visual must include:
- Handle watermark: `@BDDataStory` (bottom right, 50% opacity)
- Source attribution line (bottom center)
- Bangladesh Green (`#006A4E`) as primary or accent color

---

## Brand Compliance Checklist

Agent runs this before passing Gate 4:
- [ ] Primary color used: `#006A4E` present in chart
- [ ] Source watermark present and legible
- [ ] Correct font (Noto Sans Bengali for Bangla text)
- [ ] File size <1MB
- [ ] Dimensions correct for platform
- [ ] No copyright-restricted images used
```

### 7.4 Example: `source_priority.md`

```markdown
# Source Priority Guide

Last Updated: {date}

---

## Tier 1 — Primary (Official Bangladesh Government)

Use these first. Highest trust. Cite directly.

| Source | URL | Data Types | Notes |
|---|---|---|---|
| Bangladesh Bureau of Statistics | https://bbs.gov.bd | GDP, population, education, health | JS-rendered; requires Playwright |
| Bangladesh Bank | https://www.bb.org.bd | Monetary, trade, financial | PDFs available |
| Ministry of Finance | https://mof.gov.bd | Budget, fiscal data | Annual Economic Reviews |
| Bangladesh Economic Review | https://mof.gov.bd/site/page/ber | Comprehensive annual review | Best single-source document |

---

## Tier 2 — International (Cross-reference mandatory for Tier 1 claims)

| Source | URL | Data Types | API Available |
|---|---|---|---|
| World Bank Open Data | https://data.worldbank.org | GDP, development indicators | Yes — use API |
| IMF DataMapper | https://www.imf.org/en/Publications/WEO | GDP, inflation, fiscal | Yes |
| UNESCO UIS | https://uis.unesco.org | Education statistics | Yes |
| UNDP Bangladesh | https://www.undp.org/bangladesh | HDI, human development | Web only |
| ADB Statistics | https://data.adb.org | Regional comparison | API available |

---

## Tier 3 — Secondary (Context only; always cross-reference with Tier 1/2)

| Source | URL | Use For |
|---|---|---|
| The Daily Star data journalism | https://www.thedailystar.net | Historical context, event dates |
| Prothom Alo | https://www.prothomalo.com | Bangla primary source quotes |
| CPD Bangladesh | https://cpd.org.bd | Policy analysis and commentary |

---

## Tier 4 — Never Cite

- Wikipedia (use for orientation only — never as citation)
- Social media posts
- Unverified personal blogs
- News headlines without linked data
```

---

## 8. Claude AI Toolchain Integration

This section documents specifically how Anthropic's Claude products integrate into the platform, beyond just using the Claude API.

### 8.1 Claude Code — Role in the Platform

**Claude Code** (the CLI agentic coding tool) plays three distinct roles:

**Role 1: Visual Generation Engine**

Claude Code writes and executes Matplotlib/Seaborn Python scripts for infographic generation. The Visual Designer agent (running Claude API) writes code in its response, which Claude Code then executes in an isolated subprocess. This avoids Gemini Code Execution dependency and keeps all visual generation within the Claude ecosystem.

```bash
# Visual Designer agent calls Claude Code
claude -p "Write a Python Matplotlib script to visualize this data:
$(cat research/{topic_id}_research.md)
Use brand colors from visual_identity.md.
Output PNG to visuals/{topic_id}_ig.png (1080x1080px)."
```

**Role 2: Pipeline Scaffolding & Maintenance**

When new CrewAI agent code needs to be written, updated, or debugged, Claude Code handles the implementation. The operator (the user as Analytics Engineer) uses Claude Code to:
- Write new n8n JavaScript function nodes
- Debug CrewAI agent tools when they malfunction
- Generate test data for pipeline dry-runs
- Write one-off data transformation scripts

```bash
# Example: Debug a broken fact-checker tool
claude -p "The MCP fetch tool is returning truncated content for BBS PDFs.
Read the current agent code in agents/fact_checker.py and
propose a fix that handles large PDF responses." --allow-read --allow-write
```

**Role 3: Config Migration & Refactoring**

When monthly optimization review approves changes to multiple config files, Claude Code can implement all changes atomically:

```bash
# Claude Code implements approved config changes
claude -p "The monthly optimization review approved these changes:
$(cat reports/monthly_reflection_feb_2026.md | grep 'APPROVED')
Update the relevant config .md files in /config/ accordingly." \
--allow-write
```

---

### 8.2 Claude API — Primary LLM for All Agents

All six CrewAI agents use the Anthropic Claude API as their primary LLM via LiteLLM. The two models used:

| Model | Use Case | Why |
|---|---|---|
| `claude-sonnet-4-6` | Research, Writing, Fact-Checking, Visual Design | Best reasoning + instruction following; writes high-quality Bangla |
| `claude-haiku-4-5-20251001` | Content Strategist, Style Checker | Cheaper for lighter tasks; still excellent quality |

**LiteLLM configuration (`litellm_config.yaml` → stored as `litellm_config.md` in repo, converted at runtime):**

```markdown
# LiteLLM Config

## Model Routing

| Task | Primary Model | Fallback Model | Max Tokens |
|---|---|---|---|
| Research synthesis | claude-sonnet-4-6 | gemini/gemini-2.5-pro | 8,000 |
| Content writing | claude-sonnet-4-6 | gemini/gemini-2.5-pro | 4,000 |
| Fact-checking | claude-sonnet-4-6 | gemini/gemini-2.5-pro | 6,000 |
| Style checking | claude-haiku-4-5-20251001 | gemini/gemini-2.5-flash | 2,000 |
| Idea generation | claude-haiku-4-5-20251001 | gemini/gemini-2.5-flash | 3,000 |

## Rate Limit Strategy

- Primary: Claude API (Anthropic) — Tier 1 limits
- On 429 from Claude: Route to Gemini fallback automatically
- On 429 from both: Queue request with 5-minute delay; alert via Slack
```

---

### 8.3 MCP Servers — Claude's Real-World Interface

MCP servers are the mechanism by which Claude agents transcend pure text generation and interact with the actual world. Each MCP server is installed on the Digital Ocean droplet and made available to Claude agents running via CrewAI.

**MCP Server Deployment (`docker-compose.mcp.yml` — abbreviated):**

```yaml
services:
  mcp-fetch:
    image: node:18
    command: npx @modelcontextprotocol/server-fetch
    
  mcp-filesystem:
    image: node:18
    command: npx @modelcontextprotocol/server-filesystem
    volumes:
      - ./pipeline-data:/data  # agents read/write here
      
  mcp-playwright:
    image: mcr.microsoft.com/playwright/python
    command: python -m mcp_server_playwright
    
  mcp-brave-search:
    image: node:18
    command: npx @modelcontextprotocol/server-brave-search
    environment:
      BRAVE_API_KEY: ${BRAVE_API_KEY}
      
  mcp-github:
    image: node:18
    command: npx @modelcontextprotocol/server-github
    environment:
      GITHUB_PERSONAL_ACCESS_TOKEN: ${GITHUB_TOKEN}
      
  mcp-slack:
    image: node:18
    command: npx mcp-server-slack
    environment:
      SLACK_BOT_TOKEN: ${SLACK_BOT_TOKEN}
```

**CrewAI + MCP Integration Pattern:**

```python
from crewai import Agent, Tool
from mcp import MCPClient

# Connect to MCP servers
fetch_client = MCPClient("http://localhost:3001")  # mcp-fetch
fs_client = MCPClient("http://localhost:3002")     # mcp-filesystem
playwright_client = MCPClient("http://localhost:3003")

# Wrap MCP tools as CrewAI tools
fetch_tool = Tool(name="fetch_url", func=fetch_client.fetch, description="Fetch live web page content")
write_file = Tool(name="write_file", func=fs_client.write, description="Write content to a file")
read_file = Tool(name="read_file", func=fs_client.read, description="Read file content")
search_web = Tool(name="brave_search", func=brave_client.search, description="Search the web")

# Assign tools to agents
research_agent = Agent(
    role="Bangladesh Data Research Specialist",
    llm="anthropic/claude-sonnet-4-6",
    tools=[fetch_tool, playwright_tool, search_web, write_file, read_file],
    verbose=True
)
```

---

### 8.4 Claude Cowork — Human Review Enhancement

**Claude Cowork** is used at two points in the human layer:

**Weekly Topic Review (Touchpoint 1):**
The `topic_suggestions_{week}.md` file generated by the Content Strategist is accessible via Cowork. The operator can ask Claude (inside Cowork's desktop context) questions like:
- "Which of these 10 topic suggestions has the richest data available?"
- "Flag any suggestions that might be politically sensitive this week"
- "Rank these by estimated audience engagement based on our analytics history"

This reduces the weekly review from 30 minutes to approximately 10-15 minutes.

**Daily Content Review (Touchpoint 2):**
When the Slack notification arrives, the operator can open the full content package in Cowork instead of navigating raw files in Google Drive. Claude Cowork provides:
- Side-by-side view of draft caption and fact-check report
- Instant answers: "Does Claim 3 actually need fixing or is it close enough?"
- Batch approval if multiple posts are ready simultaneously
- Desktop notifications so the operator doesn't need to monitor Slack

---

### 8.5 Claude API for Analytics & Reflection

The Reflection Agent uses Claude Sonnet to synthesize monthly analytics data into actionable recommendations. The agent:

1. Reads the full 30-day analytics tab from Google Sheets (via MCP)
2. Reads all published content `.md` files (via MCP filesystem)
3. Identifies patterns: which topic categories, chart types, and writing styles correlate with high engagement
4. Generates a structured Markdown optimization report
5. Uses MCP GitHub tool to open a Pull Request with proposed config file changes

This closes the feedback loop: Claude writes the content, Claude analyzes how it performs, and Claude proposes improvements — all human-reviewed before taking effect.

---

## 9. API & Integration Architecture

### 9.1 External API Summary

| API | Direction | Auth | Rate Limit | Retry Strategy |
|---|---|---|---|---|
| Anthropic Claude API | Outbound | API Key (env var) | Tier 1: ~40K tokens/min | Exponential backoff; route to Gemini on 429 |
| Google Gemini API | Outbound (fallback) | API Key (env var) | Enterprise limits | Fallback when Claude 429; not primary |
| Brave Search API | Outbound | API Key (env var) | 2,000 calls/month free; $3/mo for more | Cache search results for 24 hours |
| Instagram Graph API | Outbound | OAuth 2.0 (60-day) | 200 calls/hour | Retry after 1 hour on rate limit |
| Facebook Pages API | Outbound | Same OAuth app | 200 calls/hour | Same as Instagram |
| Google Sheets API | Bidirectional | Service Account | 100 req/100s | Batch writes; exponential backoff |
| Google Drive API | Outbound | Service Account | 10 req/sec | Resumable upload for files >5MB |
| GitHub API | Outbound | PAT | 5,000 req/hour | No practical limit for this use case |
| Slack API | Outbound | Bot Token | Tier 1: 1+ msg/sec | Queue messages; don't burst |
| WordPress/Substack API | Outbound | App Password/API Key | None practical | Post-MVP; no retry needed initially |

---

### 9.2 Token Budget (Claude API)

| Task | Agent | Model | Est. Input Tokens | Est. Output Tokens | Est. Cost/Post |
|---|---|---|---|---|---|
| Research synthesis | Research Agent | Sonnet | 30K | 5K | ~$0.12 |
| Content writing | Writer Agent | Sonnet | 20K | 4K | ~$0.09 |
| Fact-checking | Fact-Checker | Sonnet | 35K | 3K | ~$0.14 |
| Style checking | Style Checker | Haiku | 8K | 2K | ~$0.003 |
| Visual design + code | Visual Designer | Sonnet | 15K | 3K | ~$0.07 |
| **Per post total** | — | — | — | — | **~$0.42** |
| **60 posts/month** | — | — | — | — | **~$25/month** |

> At claude-sonnet-4-6 pricing ($3/MTok input, $15/MTok output) and claude-haiku-4-5 pricing ($0.25/$1.25 per MTok). Estimate; actual depends on research depth.

---

## 10. Alternative Options Analysis

### 10.1 Agentic Framework: CrewAI vs LangGraph vs AutoGen

| Dimension | CrewAI ✅ Recommended | LangGraph | AutoGen |
|---|---|---|---|
| Learning curve | Low — role-based, declarative | High — graph state machines | Medium |
| Claude integration | Via LiteLLM — excellent | Via LangChain — good | Native — good |
| MCP support | Via custom tool wrappers | Via LangChain MCP | Limited |
| Best for | Sequential pipelines with defined roles | Complex branching, dynamic graphs | Conversational multi-agent |
| Debugging | Good — verbose logging | Hard — graph traversal complex | Medium |
| Migrate when? | At 100+ posts/week or complex branching | When workflow branches dynamically | Not recommended for this use case |

### 10.2 LLM Strategy: Claude-Primary vs Gemini-Primary

| Consideration | Claude-Primary ✅ | Gemini-Primary (original v1.0) |
|---|---|---|
| Bangla text quality | Excellent | Good |
| Instruction following | Superior for structured MD output | Good |
| MCP native support | ✅ Native (Claude was designed for MCP) | Via third-party adapters |
| Cost | ~$25/month for 60 posts | $0 (via work), but limited |
| Reliability | 99.9% Anthropic SLA | Dependent on work enterprise access |
| Risk | Low — commercial API, no work dependency | Medium — work access could be revoked |
| Fallback | Gemini (free via work) | Claude API |
| **Verdict** | **Primary LLM** | **Fallback LLM** |

### 10.3 Visual Generation Options

| Option | Cost | Quality | Automation Level | MVP Recommendation |
|---|---|---|---|---|
| Claude Code + Matplotlib | ~$0 (API usage) | ⭐⭐⭐ | ✅ Fully automated | ✅ **Use for MVP** |
| Gemini Code Execution | $0 | ⭐⭐⭐ | ✅ Fully automated | ✅ Fallback |
| Templated.io API | $29/mo | ⭐⭐⭐⭐⭐ | ✅ Fully automated | Phase 3+ |
| Canva API | $13/mo | ⭐⭐⭐⭐ | ✅ Fully automated | Phase 3 alternative |
| Manual Canva | $0 | ⭐⭐⭐⭐⭐ | ❌ Manual | Defeats automation goal |

### 10.4 Workflow Engine Options

| Option | Cost | Visual Debug | Integrations | Claude Code/MCP compatible | Verdict |
|---|---|---|---|---|---|
| n8n self-hosted | $18/mo (droplet) | ✅ Excellent | 400+ | ✅ Via subprocess | ✅ **Recommended** |
| Make.com | $16/mo | ✅ Good | 1,000+ | ⚠️ Via HTTP | ❌ Costly long-term |
| Zapier | $49/mo | ✅ Good | 5,000+ | ⚠️ Via HTTP | ❌ Too expensive |
| Pure Python scripts | $0 (compute) | ❌ None | Manual | ✅ Native | ⚠️ Good fallback |
| GitHub Actions | $0 (free tier) | ⚠️ Basic | Via actions | ✅ Yes | ⚠️ Good for simple triggers |

### 10.5 Human Review Interface Options

| Option | Speed | Mobile-Friendly | Cowork Integration | Verdict |
|---|---|---|---|---|
| Slack + action buttons | ⭐⭐⭐⭐⭐ | ✅ Excellent | ✅ Complementary | ✅ **Primary** |
| Email | ⭐⭐⭐ | ✅ Good | ❌ None | Fallback only |
| Custom dashboard | ⭐⭐ | Depends | Partial | Post-MVP |
| Claude Cowork | ⭐⭐⭐⭐ | Desktop only | ✅ Native | ✅ **Supplement** |
| Google Sheets directly | ⭐⭐ | ✅ OK | ❌ None | For topic queue only |

---

## 11. Security, Reliability & Scalability

### 11.1 Security Architecture

| Concern | Risk Level | Mitigation |
|---|---|---|
| API key exposure | High | Environment variables only; `.env` never committed; GitHub secrets for CI |
| OAuth token expiry | Medium | WF-09 checks token validity; alerts 7 days before expiry |
| Config integrity | Medium | JSON schema validation (config .md → validated before agent use); Git history for rollback |
| Content policy violation | Medium | Banned vocabulary list; human review gate; no auto-publish |
| Audit trail gaps | Low | All agent reasoning logged to `audit/pipeline_{id}_{timestamp}.md` |
| Source code privacy | Medium | Private GitHub repo; no public forks |
| PII collection | Low | System never collects audience personal data; only aggregate metrics fetched |

### 11.2 Error Recovery Matrix

| Error | Detection | Auto-Recovery | Human Alert |
|---|---|---|---|
| Claude API 429 | HTTP 429 response | Route to Gemini fallback via LiteLLM | If Gemini also 429 |
| Claude API 500 | HTTP 5xx | 3 retries exponential backoff | After 3rd failure |
| Fact-check failure | Gate 2 result = FAIL | Retry writer agent with corrections (max 2x) | After 2nd failure |
| Source URL 404 | MCP fetch returns 404 | Research agent tries Tier 2 alternatives | If all alternatives fail |
| Style score <75 | Gate 3 score | Return to writer (max 2x) | After 2nd retry |
| Instagram API rejection | HTTP 4xx from IG | Rate limit → retry 1hr; Auth → immediate alert | On auth/policy failure |
| n8n crash | Execution error | n8n built-in retry (max 3) | After 1st crash in production |
| Playwright timeout | Timeout exception | Retry with extended timeout; fallback to raw fetch | After 2nd timeout |

### 11.3 Scalability Path

| Phase | Volume | Architecture State | Key Bottleneck |
|---|---|---|---|
| MVP (Weeks 1-6) | 5-10 posts/week | Single droplet, sequential pipeline | Human review time |
| Growth (Months 2-4) | 15-30 posts/week | Add parallel pipeline execution for non-dependent topics | Claude API rate limits |
| Scale (Months 5-9) | 50-75 posts/week | Add second n8n worker; implement Redis job queue | Google Sheets row accumulation |
| Mature (Month 10+) | 100+ posts/week | Migrate Sheets → PostgreSQL; containerize with K3s; CDN for visuals | Infrastructure management |