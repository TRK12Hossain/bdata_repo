# Product Requirements Document (PRD)
## Bangladesh Political Content Automation Platform

**Document Version:** 1.0  
**Last Updated:** February 22, 2026  
**Document Owner:** Analytics Engineer / Content Creator  
**Status:** Requirements Definition Phase

---

## Executive Summary

This document defines the requirements for an AI-powered content creation platform focused on **data-driven storytelling** about Bangladesh's political and economic history for a **mass audience**. The platform transforms complex government data and historical statistics into accessible, engaging narratives that help young Bangladeshis (18-35) understand their country's trajectory through objective facts and visual storytelling.

The platform uses a hybrid architecture combining agentic AI reasoning with deterministic workflows to maximize automation while maintaining editorial control and trust.

---

## 1. PROJECT OVERVIEW & GOALS

### 1.1 The "Why" - Problem Statement

**Primary Problem:**
As a full-time Analytics Engineer with limited availability (<10 hours/week), creating high-volume, trustworthy political content about Bangladesh manually is unsustainable. The target is 15-30 posts per week, which would require 30-40 hours of manual work.

**Core Challenges:**
1. **Speed vs Quality Trade-off:** Manual content is high-quality but slow (3-5 posts/week maximum)
2. **Trust & Credibility:** Political content requires rigorous fact-checking and source citation
3. **Consistency:** Maintaining consistent voice, style, and visual brand across high volume
4. **Sustainability:** Cannot dedicate full-time hours while working as Analytics Engineer
5. **Resource Constraints:** Building an efficient but **customizable and modular semi-automated workflow within limited resources**, capitalizing on **open-source and free-tier services**

**Success Definition:**
- Produce 15-30 pieces of content per week
- Maintain 95%+ factual accuracy with full source attribution
- Require <10 hours/week of human time (mostly review/approval)
- Build audience trust through transparent, objective, data-driven content

---

### 1.2 User Context & Decisions

**User Profile:**
- **Role:** Analytics Engineer (full-time)
- **Availability:** Very limited weekly time investment
- **Technical Skills:** Decent (knows basic Python and development environments, comfortable with data/analytics)
- **Content Experience:** Aspiring content creator, politically aware
- **Resources Available:** Google Gemini Enterprise API (via work), Google Workspace, NotebookLM, Sourcegraph Cody, open-source tools, possibly Claude individual plan

**User's Explicit Decisions:**
1. ✅ **Platform Focus:** Social media (Instagram, Facebook) + potential blog
2. ✅ **Content Type:** Historical government data, economic trends, policy comparisons (both **local and international comparative lens**)
3. ✅ **Language:** Mixed Bangla-English (target young Bangladeshi audience, 18-35)
4. ✅ **Content Volume:** High volume objective content with easy-to-digest visuals
5. ✅ **Trust Priority:** Source citation and data transparency are highest priority
6. ✅ **Automation Level:** "As automated as possible" from research to publication
7. ✅ **Budget Constraint:** Maximize free/open-source tools
8. ✅ **API Access:** Has Google Gemini Enterprise API available
9. ✅ **Philosophical Stance:** Strictly objective, politically neutral, data-first

**What "Hybrid" Means in This Context:**
1. **Agentic AI Layer:** Handles research, content strategy, creative writing, fact-checking, **idea generation**, **similar content scanning and taking inspiration**, **static or semi-static design generation implementing user creative preferences** (tasks requiring reasoning and judgment)
2. **Workflow Layer:** Handles data formatting, scheduling, publishing, mechanical transformations (deterministic tasks)
3. **Human Layer:** Editorial direction (topic selection), final approval (trust validation), strategic oversight, **provides training data for agents to learn about creator's own writing and visual preferences**

---

## 2. TECH STACK

### 2.1 Current Available Resources (User Decisions)

| Component | Technology | Status | Justification |
|-----------|------------|--------|---------------|
| **LLM API** | Google Gemini Enterprise | ✅ Available via work | Free for user, includes Gemini 2.5 Pro and Flash |
| **AI Assistant** | Claude (individual plan) | ✅ Possibly available | User considering personal subscription |
| **Google Workspace** | Sheets, Drive, Docs | ✅ Available | Full Google Workspace access |
| **AI Research Tool** | NotebookLM | ✅ Available | Google's AI-powered research tool |
| **Code Assistant** | Sourcegraph Cody | ✅ Available | AI coding assistant |
| **Technical Capability** | Python, data analysis | ✅ User's professional skill | Decent skills: basic Python, development environments |
| **Time Availability** | <10 hours/week | ✅ Constraint | Must be highly automated |
| **Philosophy** | Open-source tools | ✅ Priority | Maximize free/open-source solutions |

### 2.2 Recommended Tech Stack (Pending User Approval)

> **⚠️ IMPORTANT NOTE:** None of the tools or architectural approaches have been finalized yet. The recommendations below reflect the overall requirements and constraints, but alternatives are actively being considered. User should evaluate these recommendations against their specific needs and available resources before making final decisions.

#### 2.2.1 Agentic AI Layer

| Component | Recommended Technology | Alternative Options | Decision Status |
|-----------|----------------------|---------------------|-----------------|
| **Agentic Framework** | CrewAI | LangGraph, AutoGen | 🟡 Recommended (not decided) |
| **Primary LLM (Reasoning)** | Gemini 2.5 Pro | N/A (already available) | ✅ Available |
| **Fast LLM (Execution)** | Gemini 2.5 Flash | N/A (already available) | ✅ Available |
| **Code Execution** | Gemini Code Execution | Python + Matplotlib locally | 🟡 Recommended |

**Rationale for CrewAI:**
- Role-based agent design (matches content production workflow)
- Easier learning curve than LangGraph (important given limited time)
- Built-in memory and inter-agent communication
- Free and open-source
- Good integration with Google's Gemini API

**Alternative Considered: LangGraph**
- More powerful but steeper learning curve
- Better for complex multi-agent orchestration
- User can migrate later if needed

#### 2.2.2 Workflow Orchestration Layer

| Component | Recommended Technology | Alternative Options | Decision Status |
|-----------|----------------------|---------------------|-----------------|
| **Workflow Automation** | claude tools, n8n (self-hosted) | Make.com, Zapier | 🟡 Recommended (Searching for similar alternatives) |
| **Hosting** | Digital Ocean Droplet ($6/mo) | Railway.app (free tier), Local Docker | 🟡 Recommended |

**Rationale for n8n:**
- Free and open-source (self-hosted)
- Visual workflow builder (faster development)
- 400+ integrations (Google Sheets, social media, etc.)
- More cost-effective than Zapier/Make for long-term
- Can trigger Python scripts (CrewAI agents)

**Alternative Considered: Pure Python Orchestration**
- More control but requires more coding
- Harder to debug visually
- Better if user wants everything in code

#### 2.2.3 Data Storage & Management

| Component | Recommended Technology | Alternative Options | Decision Status |
|-----------|----------------------|---------------------|-----------------|
| **Content Database** | Google Sheets | Airtable, PostgreSQL | 🟡 Recommended |
| **File Storage** | Google Drive | GCS Bucket (Google Cloud Storage) | 🟡 Recommended |
| **Config Files** | Local JSON/TXT files | Database, Git-based | 🟡 Recommended |
| **Version Control** | Git + GitHub | GitLab, Bitbucket | 🟡 Recommended |

**Rationale for Google Sheets:**
- Free and accessible
- Easy manual editing (user can add topics directly)
- Integrates seamlessly with n8n
- No database management overhead
- User already familiar with spreadsheets

**Alternative: GCS Bucket**
- Enterperise Tier: Can be used reasonably
- Better for large file volumes
- Integrates with Google Workspace

#### 2.2.4 Visual Content Generation

| Component | Recommended Technology | Alternative Options | Decision Status |
|-----------|----------------------|---------------------|-----------------|
| **Infographic Templates** | Templated.io ($29/mo) | Bannerbear ($29/mo), Canva API | 🟡 Recommended |
| **Chart Generation** | Gemini Code Execution + Matplotlib | Python scripts locally | 🟡 Recommended |
| **Free Alternative** | Pure Gemini Code Execution | Manual Canva design | 🟡 Option for $0 budget |

**Cost Consideration:**
- **Templated.io:** $29/month for professional infographics
- **Free Option:** Use Gemini to generate all charts/visuals via code execution
- User can start free, upgrade later if needed

#### 2.2.5 Publication & Distribution

| Component | Recommended Technology | Alternative Options | Decision Status |
|-----------|----------------------|---------------------|-----------------|
| **Instagram Publishing** | MCP Server: jlbadano/ig-mcp | Instagram Graph API, Buffer, Later | 🟡 Recommended |
| **Facebook Publishing** | MCP Server: tiroshanm/facebook-mcp-server | Facebook Pages API, Buffer, Hootsuite | 🟡 Recommended |
| **Blog Platform** | Substack  Ghost, Medium | 🟡 Optional |

**Rationale for MCP Servers:**
- Open-source solutions preferred
- Direct integration with AI agents
- No third-party service dependencies
- Free to use
- Community-maintained

**MCP Server Options:**
- **jlbadano/ig-mcp:** Instagram integration via MCP protocol
- **tiroshanm/facebook-mcp-server:** Facebook Pages integration via MCP protocol
- Both enable direct publishing from agentic AI workflows

---

### 2.3 Cost Summary

> **⚠️ NOTE:** All costs are estimates and **subject to change or improvement** as free alternatives and open-source tools are evaluated. Priority is maximizing free-tier services.

| Component | Cost | Frequency | Annual Cost |
|-----------|------|-----------|-------------|
| **Gemini API** | $0 | N/A | $0 (via work) |
| **Claude Personal Plan** | $20 (optional) | Monthly | $240 (if subscribed) |
| **CrewAI** | $0 | N/A | $0 (open-source) |
| **n8n (self-hosted)** | $6 | Monthly | $72 |
| **Templated.io** | $29 (or $0 if using Gemini) | Monthly | $348 or $0 |
| **Domain Name** | $12 | Annual | $12 |
| **TOTAL** | **$35-47/mo** or **$6-26/mo** | - | **$420-564** or **$72-312** |

**Cost Decision Point:**
- **Minimum Budget:** $6/month (n8n hosting only, all visuals via Gemini)
- **Recommended Budget:** $35/month (includes professional infographic templates)
- User needs to decide: Professional templates vs pure code-generated visuals

**Technical Architecture Preference:**
> **💡 USER PREFERENCE:** Solutions should be implemented using **markdown files as much as possible** for configuration, documentation, and data structures. This enables:
> - Easy version control with Git
> - Human-readable configurations
> - Simple editing without specialized tools
> - Portability across systems
> - Clear audit trails

---

## 3. FUNCTIONAL REQUIREMENTS

### 3.1 System Must-Haves

#### FR-1: Content Ideation & Planning
**Requirement:** The system must accept both manual topic input and generate automated topic suggestions.

**Inputs:**
- Human: Manual topic entries in Google Sheets with priority, context notes, deadline, **and inspirations** (reference content, similar posts, style examples)
- Agentic AI: Weekly automated idea generation based on recent Bangladesh news, historical anniversaries, data releases
- Human: Inspiration content for agents to learn from (examples of preferred styles, successful posts from others)

**Outputs:**
- Curated topic queue with research readiness status
- Human approval/rejection flags

**Acceptance Criteria:**
- Manual topic addition takes <2 minutes
- Automated idea generator produces 10 suggestions per week
- Human can approve/reject ideas with single click

---

#### FR-2: Autonomous Research & Data Collection
**Requirement:** The system must autonomously research topics from Bangladesh government sources and verify data quality.

**Inputs:**
- Topic description (from topic queue)
- Context notes (from human)
- Editorial preferences (from config file)
- Source priorities (BBS, Bangladesh Bank, UNESCO, World Bank)

**Process:**
- Agentic research agent searches official portals
- Extracts specific data points with metadata
- Cross-references across multiple sources
- Handles ambiguous or incomplete data (interpolation, flagging)
- Self-reflects on data quality and methodology

**Outputs:**
- Structured dataset (JSON format)
- Source URLs for every data point
- Confidence score (high/medium/low)
- Methodology notes
- Human review flags (if data quality concerns)

**Acceptance Criteria:**
- 90%+ of research tasks complete without human intervention
- 100% of data points have source attribution
- Ambiguous cases flagged for human review
- Research completion time: <10 minutes per topic

---

#### FR-3: Bilingual Content Generation
**Requirement:** The system must generate content in mixed Bangla-English that matches the user's writing style profile.

**Inputs:**
- Research data (from FR-2)
- Writing style profile (config file)
- Editorial preferences (config file)
- Reference example posts
- Recent engagement data (optional, for style optimization)

**Process:**
- Agentic content writer reads style guide
- Generates draft using PRA (Perceive-Reason-Act) loop
- Self-reviews for style match
- Maintains 70% Bangla, 30% English ratio
- Includes source citations inline
- Adds engagement hooks (questions, surprising facts)

**Outputs:**
- Draft content (Instagram caption format, Facebook post format, blog article)
- Style match score (self-assessed)
- Bangla-English ratio report

**Acceptance Criteria:**
- 85%+ style match score on first draft
- 100% of statistics cited with sources
- Bangla-English ratio within ±5% of target (70-30)
- Engagement question included in 100% of posts
- Draft generation time: <5 minutes

---

#### FR-4: Automated Fact-Checking & Verification
**Requirement:** The system must verify every claim against original sources before content is approved for publication.

**Inputs:**
- Draft content (from FR-3)
- Original source URLs (from FR-2)
- Fact-checking protocols (config)

**Process:**
- Agentic fact-checker agent fetches source documents
- Extracts exact figures from PDFs/web pages (using OCR if needed)
- Compares with claims in draft
- Identifies discrepancies or misleading context
- Generates correction suggestions
- Flags high-risk claims for human verification

**Outputs:**
- Fact-check report (JSON)
- Pass/fail status
- List of corrections applied
- Human review flags (if confidence < 95%)

**Acceptance Criteria:**
- 100% of numerical claims verified against sources
- 95%+ fact-check pass rate
- Corrections automatically applied if confidence is high
- Human review triggered if confidence < 95% or sensitive topic
- Fact-check completion time: <3 minutes

---

#### FR-5: Visual Content Generation
**Requirement:** The system must generate branded infographics and charts that follow visual identity guidelines.

**Inputs:**
- Research data (for charts)
- Draft content (for infographic text)
- Visual identity config (JSON file: colors, fonts, layouts)
- Template selection (based on content type)

**Process (Option A: Using Templated.io):**
1. Agentic visual designer decides chart type and layout
2. Gemini Code Execution generates chart with brand colors
3. Chart uploaded to cloud storage
4. n8n workflow calls Templated.io API with chart + text
5. Final infographic generated and saved

**Process (Option B: Pure Gemini - Free):**
1. Agentic visual designer decides chart type and layout
2. Gemini Code Execution generates complete infographic (chart + text + branding)
3. Self-validates brand compliance
4. Saves to Google Drive

**Outputs:**
- Publication-ready infographic (1080x1080 for Instagram, 1200x630 for Facebook)
- Source citation watermark included
- Brand compliance report

**Acceptance Criteria:**
- 95%+ visual brand compliance (colors, fonts, layout)
- All visuals include source citation
- File size < 1MB (for social media)
- Generation time: <2 minutes per visual
- Human can regenerate with style adjustments if needed

---

#### FR-6: Style Consistency Validation
**Requirement:** The system must validate that all content matches the user's writing style before moving to publication.

**Inputs:**
- Draft content (from FR-3)
- Writing style profile (config file)
- Example reference posts

**Process:**
- Agentic style checker agent scores draft on 10 dimensions
- Compares tone, vocabulary, structure, Bangla-English ratio
- Identifies deviations with specific line numbers
- Generates correction suggestions
- Auto-corrects if score is marginal (80-84%)
- Returns to writer agent if score < 80%

**Outputs:**
- Style compliance report
- Overall score (0-100)
- List of deviations and corrections
- Approval status

**Acceptance Criteria:**
- 90%+ of drafts achieve 85+ score on first attempt
- Auto-correction successful in 80%+ of marginal cases
- Human intervention required only if score < 75%
- Style check completion time: <2 minutes

---

#### FR-7: Human Review & Approval Interface
**Requirement:** The system must present completed content to the user for final approval before publication.

**Inputs:**
- Completed content package (text + visual + sources + compliance reports)

**Process:**
- n8n workflow compiles review package
- Sends Slack message or email with preview
- Provides action buttons: [Approve] [Request Changes] [Reject]
- If approved: Triggers publication workflow
- If changes requested: Returns to appropriate agent with feedback
- If rejected: Logs reason and removes from queue

**Outputs:**
- Approval/rejection decision
- Feedback notes (if changes requested)

**Acceptance Criteria:**
- Review package delivered within 2 minutes of content completion
- Human can approve in < 5 minutes (mobile-friendly interface)
- Approval triggers immediate publication workflow
- Rejection reasons logged for system learning

---

#### FR-8: Multi-Platform Publication
**Requirement:** Upon approval, the system must publish content to Instagram, Facebook, and optionally blog with proper formatting for each platform.

**Inputs:**
- Approved content (text + visual)
- Platform-specific formatting rules
- Publication schedule (if delayed post)

**Process (Deterministic Workflow):**
1. Format content for each platform (character limits, hashtags, etc.)
2. Call Instagram Graph API (image + caption)
3. Call Facebook Pages API (image + post)
4. Optionally: WordPress API (blog article with embedded image)
5. Log publication metadata to Google Sheets
6. Update content status to "published"

**Outputs:**
- Published posts on all platforms
- Publication confirmation with URLs
- Analytics tracking tags

**Acceptance Criteria:**
- Publication success rate: 99%+ (with retry logic)
- Publication time: <60 seconds across all platforms
- All platforms receive properly formatted content
- Hashtags, source links, and attributions preserved
- Publication logged with timestamp, platform, engagement tracking

---

#### FR-9: Analytics & Performance Tracking
**Requirement:** The system must track engagement metrics and surface insights for content optimization.

**Inputs:**
- Post URLs from FR-8
- Social media API engagement data (likes, shares, comments)
- Publication metadata (topic, style elements used, visual type)

**Process:**
- Daily: Fetch engagement metrics via APIs
- Weekly: Analyze patterns (which topics/styles perform best)
- Monthly: Agentic reflection agent generates optimization suggestions
- Update style guide or agent instructions based on data

**Outputs:**
- Engagement dashboard (Google Sheets or simple web interface)
- Weekly performance summary
- Monthly optimization recommendations

**Acceptance Criteria:**
- Engagement data synced daily with <1% failure rate
- Top/bottom performing posts identified weekly
- Actionable insights generated monthly
- User can approve/reject optimization suggestions

---

### 3.2 System Should-Haves (Lower Priority)

#### FR-10: Content Calendar & Scheduling
**Requirement:** The system should allow scheduling content for optimal posting times.

**Priority:** Medium (can publish immediately initially, add scheduling later)

---

#### FR-11: A/B Testing Framework
**Requirement:** The system should enable testing different headlines, visuals, or formats to optimize engagement.

**Priority:** Low (implement after 3 months of baseline data)

---

#### FR-12: Audience Q&A Integration
**Requirement:** The system should accept audience questions and generate data-driven answers.

**Priority:** Low (future enhancement)

---

## 4. NON-FUNCTIONAL REQUIREMENTS

### 4.1 Performance Requirements

| Metric | Target | Critical Threshold |
|--------|--------|--------------------|
| **Research Completion Time** | <10 min | <20 min |
| **Content Generation Time** | <5 min | <10 min |
| **Fact-Check Time** | <3 min | <5 min |
| **Visual Generation Time** | <2 min | <5 min |
| **End-to-End Processing** | <30 min | <60 min |
| **Publication Time** | <60 sec | <2 min |
| **Human Review Time Required** | <5 min/post | <10 min/post |
| **Weekly System Throughput** | 15-30 posts | Minimum 10 posts |

---

### 4.2 Reliability & Quality Requirements

| Metric | Target | Monitoring Method |
|--------|--------|------------------|
| **Fact-Check Accuracy** | 95%+ pass rate | Weekly manual audit (5 random posts) |
| **Source Attribution** | 100% of stats cited | Automated validation |
| **Style Consistency** | 85%+ match score | Automated style checker |
| **Visual Brand Compliance** | 95%+ | Automated color/font validation |
| **Workflow Success Rate** | 99%+ | n8n execution logs |
| **API Uptime** | 99%+ | External monitoring |
| **Human Approval Rate** | 80%+ approved on first review | Google Sheets logs |

---

### 4.3 Scalability Requirements

- **Current Target:** 15-30 posts/week (manageable with single n8n instance)
- **6-Month Target:** 50-75 posts/week (may require distributed n8n or queue management)
- **1-Year Target:** 100+ posts/week (may require migration to dedicated infrastructure)

**Scaling Considerations:**
- Gemini API rate limits (user's enterprise plan should handle 100s of requests/day)
- n8n workflow concurrency (may need multiple workers)
- Google Sheets row limits (may need to migrate to PostgreSQL after 50k posts)

---

### 4.4 Security & Privacy Requirements

| Requirement | Implementation |
|-------------|----------------|
| **API Key Management** | Environment variables, never committed to Git |
| **Source Code Privacy** | Private GitHub repository |
| **User Data** | No collection of audience personal data |
| **Content Backup** | Daily backup of Google Sheets to Google Drive |
| **Config Version Control** | Git history for all config changes |
| **Audit Trail** | All agent decisions and reasoning logged |

---

### 4.5 Maintainability Requirements

- **Documentation:** All agents, workflows, and config files documented inline
- **Monitoring:** Slack/email alerts for all system failures
- **Debugging:** Agent reasoning steps logged for troubleshooting
- **Updates:** Ability to update agent instructions without code changes (via config files)
- **Testing:** Ability to run test workflows without affecting production

---

## 5. CONSTRAINTS & LOGIC FLOW

### 5.1 Human Touchpoints (Human-in-the-Loop Design)

The system is designed with three mandatory human intervention points:

#### Touchpoint 1: Topic Queue Management (Weekly, 30 minutes)
**When:** Every Monday morning  
**What:** Review and approve topics for the week  
**Location:** Google Sheets "Content_Queue" tab  

**Process:**
1. System generates 10 automated topic suggestions (via agentic idea generator)
2. Human reviews suggestions + adds own ideas
3. Human sets priority (High/Medium/Low) and context notes
4. Human approves topics by changing status to "Approved"
5. Agents begin research only on approved topics

**Why Human?** Strategic editorial direction, sensitivity to current events, knowledge of audience preferences

---

#### Touchpoint 2: Content Review & Approval (Daily, 20-30 minutes)
**When:** Daily at 5pm (or whenever content is ready)  
**What:** Review completed content before publication  
**Location:** Slack message or email with preview  

**Process:**
1. System completes content (research → write → fact-check → visual → style check)
2. If all automated quality checks pass (fact-check 95%+, style 85%+), send to human
3. Human reviews: caption + image + sources + quality reports
4. Human chooses: [Approve] [Request Changes] [Reject]
5. If approved: System publishes immediately
6. If changes requested: Returns to specific agent with feedback
7. If rejected: System logs reason for learning

**Why Human?** Final editorial judgment, trust validation, catches nuanced issues that automated checks miss, maintains accountability

---

#### Touchpoint 3: Monthly Optimization Review (Monthly, 1-2 hours)
**When:** First Monday of each month  
**What:** Review performance data and approve system refinements  
**Location:** Google Sheets analytics dashboard + optimization suggestions doc  

**Process:**
1. System generates monthly performance report (engagement trends, top/bottom posts, patterns)
2. Agentic reflection agent suggests optimizations (style guide updates, source priorities, visual formats)
3. Human reviews suggestions
4. Human approves/rejects each optimization
5. Approved changes automatically update config files
6. System commits changes to Git with human approval note

**Why Human?** Strategic decisions about content direction, avoiding algorithmic bias, maintaining long-term vision

---

### 5.2 Automated Quality Gates (No Human Needed)

The system has automated checkpoints that prevent low-quality content from reaching human review:

#### Gate 1: Research Quality (Automated)
**Criteria:**
- All data points have source URLs ✓
- Confidence score ≥ "medium" ✓
- No "high-risk" flags for data quality ✓

**If fails:** Flag for human review with specific issues noted

---

#### Gate 2: Fact-Check Validation (Automated)
**Criteria:**
- Fact-check pass rate ≥ 95% ✓
- No discrepancies found between draft and sources ✓
- All corrections applied successfully ✓

**If fails:** Return to content writer agent with corrections, retry up to 2 times, then flag for human review

---

#### Gate 3: Style Compliance (Automated)
**Criteria:**
- Style match score ≥ 85% ✓
- Bangla-English ratio within 70±5% / 30±5% ✓
- No banned vocabulary used ✓
- Engagement question present ✓

**If fails:** Return to content writer agent with specific deviations, retry up to 2 times, then flag for human review

---

#### Gate 4: Visual Brand Compliance (Automated)
**Criteria:**
- Colors match visual identity palette ✓
- Fonts from approved list ✓
- Dimensions correct for platform ✓
- Source citation watermark present ✓

**If fails:** Return to visual designer agent, retry once, then flag for human review

---

### 5.3 Cost & Token Budget Constraints

#### Budget Allocation Strategy

**Agentic AI Tasks (Gemini 2.5 Pro - Expensive but Necessary):**
- Research: Max 50K input + 10K output tokens = ~$0.28 per task
- Content Writing: Max 30K input + 5K output tokens = ~$0.15 per task
- Fact-Checking: Max 40K input + 3K output tokens = ~$0.17 per task
- Idea Generation: Max 20K input + 5K output tokens = ~$0.10 per task

**Workflow Tasks (Gemini 2.5 Flash - Cheap for Deterministic):**
- Data Formatting: Max 5K input + 2K output tokens = ~$0.001 per task
- Template Population: Max 3K input + 1K output tokens = ~$0.0005 per task

**Monthly Token Budget (15 posts/week = 60 posts/month):**
- Research: 60 × $0.28 = $16.80
- Writing: 60 × $0.15 = $9.00
- Fact-Checking: 60 × $0.17 = $10.20
- Style Checking: 60 × $0.10 = $6.00
- Idea Generation: 4 weeks × $0.10 = $0.40
- Workflows: 200 operations × $0.001 = $0.20
- **Total: ~$42.60/month in API costs**

**Budget Constraints:**
- User has Gemini Enterprise API via work (may be free or allocated budget)
- **Decision Point:** User needs to confirm if there are token limits or costs through work API

**Cost Optimization Strategies:**
1. Cache repeated data (e.g., visual identity config) to reduce input tokens
2. Use Flash for all deterministic tasks
3. Use Pro only for reasoning-heavy tasks
4. Implement result caching for similar research queries
5. Compress prompts by removing redundant instructions

---

### 5.4 Error Handling & Fallback Logic

#### Error Scenario 1: API Failure
**What:** Gemini API returns error or times out  
**Detection:** n8n workflow monitors HTTP status codes  
**Fallback:**
1. Retry up to 3 times with exponential backoff
2. If still fails, log error and send Slack alert to human
3. Queue task for manual retry
4. Continue processing other tasks (don't block entire pipeline)

---

#### Error Scenario 2: Research Data Unavailable
**What:** BBS portal down, data source inaccessible  
**Detection:** Agentic research agent perceives failed source access  
**Fallback:**
1. Agent autonomously tries alternative sources (World Bank, UNESCO)
2. If all sources fail, flag topic as "data unavailable"
3. Send Slack alert to human with specific issue
4. Human decides: postpone topic or use alternative approach

---

#### Error Scenario 3: Fact-Check Failure
**What:** Cannot verify claims (source links broken, data mismatch)  
**Detection:** Fact-checker agent confidence score < 70%  
**Fallback:**
1. Mark content as "fact-check failed"
2. Do NOT proceed to human review (prevent publishing unverified content)
3. Return to research agent with specific verification issues
4. Research agent re-fetches or finds alternative sources
5. If still fails after 2 attempts, escalate to human with detailed report

---

#### Error Scenario 4: Style Check Repeated Failures
**What:** Content writer cannot achieve 85%+ style match after 2 retries  
**Detection:** Style checker marks "approved: false" twice  
**Fallback:**
1. Send to human with style deviation report
2. Human provides specific feedback or rewrites section manually
3. Log issue pattern for monthly optimization review
4. May indicate need to update style guide with clearer examples

---

#### Error Scenario 5: Publication API Failure
**What:** Instagram/Facebook API rejects post (rate limit, authentication, etc.)  
**Detection:** n8n workflow receives error response  
**Fallback:**
1. Log error details (rate limit vs auth vs content policy)
2. If rate limit: Queue for retry in 1 hour
3. If auth: Send alert to human (likely need to reauthorize app)
4. If content policy: Send to human for review (may contain flagged content)
5. Mark post as "publication failed" in Google Sheets

---

### 5.5 Data Flow Diagram

```
[HUMAN: Add Topic to Google Sheets]
        ↓
[AGENTIC: Content Strategist reads weekly]
        ↓ (reasons about priority, data availability)
        ↓
[AGENTIC: Research Agent executes plan]
        ↓ (perceives sources, adapts to data quality)
        ↓
[QUALITY GATE 1: Research Quality ≥ threshold?]
        ↓ YES
[WORKFLOW: Format data to JSON, save to Sheets]
        ↓
[AGENTIC: Content Writer generates draft]
        ↓ (reasons about style, structure, tone)
        ↓
[AGENTIC: Fact-Checker validates claims]
        ↓ (perceives sources, compares with draft)
        ↓
[QUALITY GATE 2: Fact-check pass rate ≥ 95%?]
        ↓ YES
[AGENTIC: Style Checker validates voice]
        ↓ (reasons about tone, ratio, structure)
        ↓
[QUALITY GATE 3: Style match ≥ 85%?]
        ↓ YES
[WORKFLOW: Apply platform-specific formatting]
        ↓
[AGENTIC: Visual Designer creates infographic]
        ↓ (reasons about chart type, layout, emphasis)
        ↓
[WORKFLOW: Apply brand colors, generate via Templated or Gemini]
        ↓
[QUALITY GATE 4: Visual brand compliance?]
        ↓ YES
[WORKFLOW: Package for human review]
        ↓
[HUMAN TOUCHPOINT: Review and Approve]
        ↓ [Approve]
[WORKFLOW: Publish to Instagram, Facebook, Blog]
        ↓
[WORKFLOW: Log publication, track engagement]
        ↓
[MONTHLY: Agentic Reflection analyzes performance]
        ↓
[HUMAN TOUCHPOINT: Review optimization suggestions]
```

---

## 6. USER CONTROL POINTS

### 6.1 Editorial Direction Control

**Location:** Google Sheets "Content_Queue"  
**Format:**

| Topic_ID | Topic_Bangla | Topic_English | Priority | Context_Notes | Deadline | Status |
|----------|--------------|---------------|----------|---------------|----------|--------|
| T001 | শিক্ষা খরচ তুলনা | Education Spending Comparison | High | Compare 1996-2001 vs 2009-2024, focus on primary education | 2025-02-28 | Approved |
| T002 | GDP Growth Timeline | GDP Growth Timeline | Medium | 1990-2024 decade averages | 2025-03-05 | Queue |

**User Interaction:**
- Add rows manually (2 minutes per topic)
- Review automated suggestions (appear weekly)
- Set priority and context
- Change status to "Approved" when ready

**System Response:**
- Agentic Content Strategist reads sheet every Monday 6am
- Only processes "Approved" status topics
- Context_Notes passed directly to research agent as additional instructions

---

### 6.2 Writing Style Control

**Location:** `/config/writing_style_profile.txt`  
**Format:** Plain text file with sections

```markdown
# MY WRITING STYLE GUIDE

## Voice Characteristics
- Tone: Informative yet conversational
- Formality: Semi-formal (like a knowledgeable friend)
- Personality: Curious researcher, not political commentator

## Language Mix Rules
- Headline: 60% Bangla, 40% English
- Body: 70% Bangla, 30% English technical terms
- Statistics: Always in English numerals with Bangla context

## Example Posts I Love
[User adds 3-5 actual example posts they've written or admire]

## Vocabulary Rules
ALWAYS USE:
- "তথ্য" (data) not "ডেটা"

NEVER USE:
- Inflammatory words without verification
```

**User Interaction:**
- Edit text file directly (10 minutes initial setup)
- Update periodically based on feedback (5 minutes/month)
- Add new example posts as reference

**System Response:**
- All agentic writing agents load this file on every execution
- Style checker validates against these rules
- Monthly reflection agent may suggest updates based on engagement

---

### 6.3 Visual Identity Control

**Location:** `/config/visual_identity.json`  
**Format:** Structured JSON

```json
{
  "color_palette": {
    "primary": {
      "name": "Bangladesh Green",
      "hex": "#006A4E",
      "usage": "Headers, key stats, CTAs"
    },
    "secondary": {
      "name": "Liberation Red",
      "hex": "#F42A41",
      "usage": "Highlights, important dates"
    }
  },
  "typography": {
    "bangla_font": {
      "name": "Noto Sans Bengali",
      "weights": ["Regular", "Bold"]
    },
    "english_font": {
      "name": "Inter",
      "weights": ["Regular", "SemiBold", "Bold"]
    }
  }
}
```

**User Interaction:**
- Edit JSON file directly (30 minutes initial setup)
- Update colors/fonts as brand evolves (10 minutes per change)
- Version controlled via Git

**System Response:**
- Workflow layer validates all visuals against this config
- Agentic visual designer reads for creative decisions
- Automated rejection if colors/fonts not from approved list

---

### 6.4 Editorial Preferences Control

**Location:** `/config/editorial_preferences.txt`  
**Format:** Plain text with clear sections

```markdown
# EDITORIAL PREFERENCES

## Content Philosophy
- Strictly objective, data-driven
- No partisan language
- Focus on verifiable facts

## Favorite Topics (Prioritize)
1. Economic indicators
2. Education system evolution
3. Infrastructure development

## Topics to Avoid
- Religious controversies
- Active legal cases
- Unverified claims

## Tone Rules
- Informative, not preachy
- Respectful of all political periods
```

**User Interaction:**
- Define once (20 minutes)
- Update as editorial vision evolves (5 minutes per update)

**System Response:**
- Agentic Content Strategist uses for idea generation
- Agentic Researcher prioritizes sources based on philosophy
- Fact-checker applies stricter verification for sensitive topics
- All agents maintain neutral tone per rules

---

## 7. SUCCESS METRICS & KPIs

### 7.1 System Performance Metrics

| Metric | Target | Measurement Method | Review Frequency |
|--------|--------|-------------------|------------------|
| **Content Volume** | 15-30 posts/week | Google Sheets log | Weekly |
| **Human Time Required** | <10 hours/week | Manual time tracking | Weekly |
| **Research Accuracy** | 95%+ verified | Weekly audit (5 samples) | Weekly |
| **Fact-Check Pass Rate** | 95%+ on first check | Automated logging | Daily |
| **Style Match Score** | 85%+ average | Automated scoring | Daily |
| **Brand Compliance** | 95%+ visuals | Automated validation | Daily |
| **Human Approval Rate** | 80%+ approved first review | Google Sheets status | Weekly |
| **Publication Success** | 99%+ published without error | n8n logs | Daily |

---

### 7.2 Content Quality Metrics

| Metric | Target | Measurement Method | Review Frequency |
|--------|--------|-------------------|------------------|
| **Source Citation** | 100% of stats cited | Automated regex check | Daily |
| **Bangla-English Ratio** | 70±5% / 30±5% | Automated text analysis | Daily |
| **Engagement Rate** | +20% month-over-month | Social media APIs | Monthly |
| **Audience Trust Score** | Improving trend | Quarterly survey | Quarterly |
| **Content Diversity** | 5+ topic categories/month | Google Sheets analysis | Monthly |

---

### 7.3 Cost Efficiency Metrics

| Metric | Target | Calculation |
|--------|--------|-------------|
| **Cost per Post** | <$2 | Total monthly cost / posts published |
| **Time Savings** | 70%+ vs manual | (Manual hours - Automated hours) / Manual hours |
| **API Cost Efficiency** | Decreasing trend | Monthly API cost / posts published |

---

## 8. RISKS & MITIGATION STRATEGIES

### 8.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Gemini API Rate Limits** | Medium | High (blocks production) | Monitor usage, implement caching, request limit increase if needed |
| **Agentic Hallucination** | Medium | High (publishes false info) | Mandatory fact-check gate, human final approval, log all reasoning |
| **Workflow Failure** | Low | Medium (delays posts) | Retry logic, Slack alerts, queue system for manual intervention |
| **Data Source Changes** | Medium | Medium (research fails) | Agentic adaptability, fallback sources, alert human if all fail |
| **Style Drift** | Low | Low (content feels different) | Monthly optimization review, version control on configs |

---

### 8.2 Content Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Accidental Bias** | Medium | High (damages trust) | Editorial preferences file, fact-check gate, monthly bias audit |
| **Source Misattribution** | Low | High (credibility loss) | 100% citation validation, fact-check gate, human review |
| **Offensive Content** | Very Low | Very High (platform ban) | Banned vocabulary list, tone checks, human final review |
| **Timing Insensitivity** | Low | Medium (PR issue) | Human reviews current events, can reject/postpone topics |

---

### 8.3 Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **User Unavailable for Review** | Medium | Low (delays posts) | Queue system, 48-hour buffer, automated posting if no response |
| **System Requires Maintenance** | Low | Medium (downtime) | Monitoring alerts, weekly health checks, backup manual process |
| **Loss of Gemini API Access** | Very Low | Very High (full stop) | Backup plan: migrate to OpenAI or Anthropic (Claude) |

---

## 9. IMPLEMENTATION PHASES

### Phase 0: Decision & Planning (Week 1)
**Duration:** 1 week  
**User Decisions Required:**
- ✅ Approve overall hybrid architecture approach
- ✅ Decide: CrewAI vs LangGraph for agentic framework
- ✅ Decide: Templated.io ($29/mo) vs Free Gemini visuals
- ✅ Decide: n8n self-hosted ($6/mo) vs cloud alternative
- ✅ Confirm Gemini Enterprise API access and any token limits

**Deliverables:**
- Finalized tech stack decisions
- Budget approved
- GitHub repository created
- Config file templates prepared

---

### Phase 1: Foundation - Workflow Layer (Weeks 2-3)
**Duration:** 2 weeks  
**Goal:** Build deterministic workflows for mechanical tasks

**Tasks:**
1. Set up n8n (Docker or cloud)
2. Connect to Google Sheets, Google Drive
3. Create workflow: "Manual Post to Instagram"
4. Create workflow: "Fetch Data from Google Sheets"
5. Create workflow: "Format JSON and Save"
6. Test end-to-end: Manual input → Format → Output

**Deliverables:**
- n8n operational with 3 working workflows
- Can manually trigger content publishing
- 3-5 hours/week time saved on mechanical tasks

**User Time Investment:** 10 hours

---

### Phase 2: Agentic Research Layer (Weeks 4-5)
**Duration:** 2 weeks  
**Goal:** Add autonomous research capability

**Tasks:**
1. Install CrewAI and dependencies
2. Create config files (editorial preferences, source priorities)
3. Build Research Agent with PRA loop
4. Test with 3 sample topics (GDP, education, infrastructure)
5. Connect to existing workflows (Agent → JSON → Workflow)

**Deliverables:**
- Research agent successfully fetches and structures data
- 90%+ data points have source attribution
- Research output integrates with workflows

**User Time Investment:** 12 hours

---

### Phase 3: Content Creation Layer (Weeks 6-7)
**Duration:** 2 weeks  
**Goal:** Add autonomous content writing and fact-checking

**Tasks:**
1. Create writing style profile (user defines voice)
2. Build Content Writer Agent
3. Build Fact-Checker Agent
4. Build Style Checker Agent
5. Create CrewAI crew workflow (Research → Write → Fact-Check → Style-Check)
6. Test with 5 sample topics

**Deliverables:**
- Complete agent crew producing draft content
- 85%+ style match on first draft
- 95%+ fact-check pass rate

**User Time Investment:** 10 hours

---

### Phase 4: Visual Generation Layer (Weeks 8-9)
**Duration:** 2 weeks  
**Goal:** Automate infographic and chart creation

**Tasks:**
1. Create visual identity config JSON
2. Build Visual Designer Agent
3. Set up Templated.io (or pure Gemini alternative)
4. Create 3 base templates (Data Card, Timeline, Comparison)
5. Integrate with content workflow

**Deliverables:**
- Automated visual generation working
- 95%+ brand compliance
- Complete content packages (text + visual) ready for review

**User Time Investment:** 15 hours (includes template design)

---

### Phase 5: Publication & Review (Weeks 10-11)
**Duration:** 2 weeks  
**Goal:** Close the loop with human review and multi-platform publishing

**Tasks:**
1. Set up Instagram Graph API, Facebook Pages API
2. Create human review workflow (Slack or email)
3. Build publication workflow (multi-platform)
4. Set up analytics tracking
5. Create Google Sheets dashboard for metrics

**Deliverables:**
- One-click approval → publish across platforms
- Human review time <5 minutes per post
- Analytics automatically logged

**User Time Investment:** 8 hours

---

### Phase 6: Optimization & Scaling (Weeks 12+)
**Duration:** Ongoing  
**Goal:** Refine based on real-world usage

**Tasks:**
1. Add automated idea generator (agentic)
2. Implement monthly reflection agent
3. A/B test content formats
4. Optimize costs and speed
5. Scale to 30+ posts/week

**Deliverables:**
- Self-optimizing system
- <10 hours/week human time
- 15-30 posts/week consistently

**User Time Investment:** 5-10 hours/week (steady state)

---

## 10. OPEN QUESTIONS & DECISIONS NEEDED

### 10.1 Tech Stack Decisions
- [ ] **Agentic Framework:** CrewAI (recommended) or LangGraph?
- [ ] **Visual Generation:** Templated.io ($29/mo) or free Gemini Code Execution?
- [ ] **Workflow Hosting:** Self-hosted n8n ($6/mo) or cloud alternative?
- [ ] **Blog Platform:** WordPress, Substack, or none initially?

### 10.2 Operational Decisions
- [ ] **Posting Schedule:** Daily? Specific times? Or as-ready?
- [ ] **Content Mix:** What % economic vs education vs infrastructure?
- [ ] **Language Ratio:** Confirm 70% Bangla / 30% English is correct?
- [ ] **Approval Process:** Slack, email, or custom dashboard?

### 10.3 Budget Decisions
- [ ] **Gemini API:** Confirm availability and any token limits through work
- [ ] **Infographic Tool:** Approve $29/month for Templated.io or go free?
- [ ] **Domain/Hosting:** Approve $12/year domain + $6/month hosting?

### 10.4 Content Strategy Decisions
- [ ] **Launch Date:** When should first automated post go live?
- [ ] **Initial Topics:** What are the first 10 topics to tackle?
- [ ] **Audience Building:** Organic growth or paid promotion?
- [ ] **Engagement Strategy:** How to handle comments/questions?

---

## 11. APPENDIX

### 11.1 Glossary

**Agentic AI:** Autonomous AI system that uses Perception-Reasoning-Action loops to make decisions and adapt to context (not just follow fixed rules)

**Hybrid Architecture:** System design that combines agentic AI (for reasoning tasks), deterministic workflows (for mechanical tasks), and human oversight (for strategic decisions)

**PRA Loop:** Perception (observe context) → Reasoning (plan approach) → Action (execute) → Reflection (learn from outcome)

**CrewAI:** Open-source Python framework for building multi-agent AI systems with role-based agents

**n8n:** Open-source workflow automation tool (alternative to Zapier/Make)

**Gemini 2.5 Pro:** Google's most capable reasoning model (expensive but powerful)

**Gemini 2.5 Flash:** Google's fast, cost-effective model for deterministic tasks

**HITL (Human-in-the-Loop):** Design pattern where AI does bulk work but humans provide oversight at critical checkpoints

---

### 11.2 Reference Documents

**Architecture Documents:**
- `bangladesh-hybrid-ai-architecture-v2.md` - Full technical architecture
- `bangladesh-content-automation-architecture.md` - Original architecture (superseded)

**Config File Templates:**
- `/config/editorial_preferences.txt`
- `/config/writing_style_profile.txt`
- `/config/visual_identity.json`

**Code Repositories:**
- GitHub: [To be created]

---

### 11.3 Contact & Support

**Document Owner:** [User Name]  
**Technical Advisor:** AI Assistant (Claude)  
**Review Cycle:** Monthly  
**Next Review Date:** March 22, 2026

---

## Document Approval

**Created By:** AI Assistant (Claude) based on user requirements  
**Review Status:** ⏳ Pending User Approval  
**Approval Required For:**
1. Tech stack decisions (Section 2.2)
2. Budget allocation (Section 2.3, 10.3)
3. Functional requirements (Section 3)
4. Implementation timeline (Section 9)

**Next Steps:**
1. User reviews document
2. User makes decisions on open questions (Section 10)
3. User approves/modifies requirements
4. Move to Phase 0: Decision & Planning

---

**END OF DOCUMENT**