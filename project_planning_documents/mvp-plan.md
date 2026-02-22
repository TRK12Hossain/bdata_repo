
## 12. MVP Plan — 6-Week Sprint

### 12.1 MVP Philosophy

The MVP produces 1 fully verified, published post per day with less than 15 minutes of human time. It never trades trust (source attribution + human approval) for speed. Every component included in the MVP earns its place by being on the critical path to that outcome.

### 12.2 MVP Scope Decision

| Capability | In MVP? | Reason |
|---|---|---|
| Manual topic entry (Google Sheets) | ✅ YES | Non-negotiable editorial control |
| Automated topic suggestions (Strategist) | ✅ YES | PRD FR-1 must-have; adds <1hr setup |
| Research Agent (Claude + MCP fetch + Playwright) | ✅ YES | Core value — eliminates research time |
| Content Writer Agent (bilingual, Claude) | ✅ YES | Core value — eliminates writing time |
| Fact-Checker Agent (Claude + MCP fetch) | ✅ YES | Non-negotiable — trust is the product |
| Style Checker Agent (Claude Haiku) | ✅ YES | Brand consistency from day one |
| Visual Designer (Claude Code + Matplotlib) | ✅ YES (simplified) | Required for Instagram posts |
| n8n Pipeline Orchestrator (WF-02) | ✅ YES | Ties all agents together |
| Human review via Slack (WF-03) | ✅ YES | Non-negotiable — no auto-publish |
| Instagram publish (WF-04) | ✅ YES | Primary channel |
| Facebook publish (WF-04) | ⚠️ OPTIONAL | Add if Instagram works smoothly in Week 5 |
| Error alerting (WF-06) | ✅ YES | Must know when pipeline breaks |
| Health monitor (WF-09) | ✅ YES | Simple; prevents silent failures |
| Config backup (WF-08) | ✅ YES | Simple; prevents catastrophic loss |
| Analytics tracking (WF-05) | ❌ DEFER | Manual tracking OK in Month 1 |
| Monthly Reflection Agent | ❌ DEFER | Needs 30+ posts of data first |
| Templated.io visuals | ❌ DEFER | Claude Code + Matplotlib sufficient for MVP |
| Blog publishing | ❌ DEFER | Social media is the MVP channel |
| Dry-run mode | ✅ YES | Essential for testing without publishing |
| Claude Cowork integration | ⚠️ OPTIONAL | Nice-to-have; add if review is slow |

### 12.3 Week-by-Week Build Plan

---

#### Week 1: Infrastructure & Configuration

**Goal:** Everything needed to run agents is set up; all configs written.

| Task | Time | Output |
|---|---|---|
| Provision Digital Ocean 2vCPU/4GB droplet; install Docker, Docker Compose | 2 hrs | Droplet accessible via SSH; Docker running |
| Deploy n8n via Docker; configure HTTPS with nginx | 1 hr | n8n accessible at `https://n8n.yourdomain.com` |
| Create private GitHub repo; create `/config/` and `/agents/` folder structure | 30 min | Repo with initial commit |
| Write `writing_style_profile.md` (2-3 hrs of genuine work — defines the brand) | 2 hrs | Style guide with 3+ example posts included |
| Write `editorial_preferences.md` (topic rules, banned topics, sensitivity flags) | 1 hr | Editorial preferences defined |
| Write `visual_identity.md` (colors, fonts, templates) | 45 min | Brand guide in Markdown |
| Write `source_priority.md` (all Tier 1/2/3 sources with URLs) | 45 min | Source hierarchy documented |
| Configure all environment variables on droplet | 30 min | `.env` file with all API keys |
| Test n8n → Google Sheets connectivity | 30 min | n8n can read/write all 4 Sheets tabs |
| Deploy MCP servers (fetch, filesystem, playwright) | 1 hr | 3 MCP servers running in Docker |

**Week 1 Total: ~10 hours**

---

#### Week 2: Research & Strategist Agents

**Goal:** The system can autonomously research any Bangladesh topic and generate topic ideas.

| Task | Time | Output |
|---|---|---|
| Set up Python venv on droplet; install CrewAI, LiteLLM, Anthropic SDK | 1 hr | `pip install crewai litellm anthropic` working |
| Configure LiteLLM with Claude primary + Gemini fallback | 30 min | `litellm_config.md` → runtime YAML; both LLMs callable |
| Build Research Agent with MCP tools (fetch, playwright, filesystem) | 3 hrs | Agent reads source .md, fetches URLs, writes `research/{id}_research.md` |
| Build Content Strategist Agent with MCP brave-search | 2 hrs | Agent searches Brave, reads editorial prefs, writes `topic_suggestions_{week}.md` |
| Test both agents with 3 real Bangladesh topics | 2 hrs | 3 research .md files reviewed; quality assessed manually |
| Fix any issues from testing (prompt tuning, MCP connection issues) | 1 hr | Agents passing manual QA |

**Week 2 Total: ~9.5 hours**

---

#### Week 3: Writing, Fact-Check, and Style Agents

**Goal:** The full content creation pipeline works end-to-end without visuals.

| Task | Time | Output |
|---|---|---|
| Build Content Writer Agent (reads research .md + style profile .md) | 3 hrs | Produces bilingual draft `.md` files for all 3 platforms |
| Build Fact-Checker Agent (reads draft .md + fetches source URLs via MCP) | 3 hrs | Produces `factcheck_{id}.md` with claim-by-claim results |
| Build Style Checker Agent (reads draft .md + style profile .md) | 2 hrs | Produces `stylecheck_{id}.md` with dimension scores |
| Implement Gate 1 + Gate 2 + Gate 3 logic in Python orchestrator script | 1 hr | Gate evaluation functions; retry logic; error flagging |
| End-to-end test (Research → Write → Fact-Check → Style) with 5 topics | 1.5 hrs | 5 content packages; human reviews all manually |
| Tune prompts based on quality review | 1 hr | Agent prompts refined based on real outputs |

**Week 3 Total: ~11.5 hours**

---

#### Week 4: Visuals + n8n Pipeline Orchestration

**Goal:** Full pipeline with visuals; n8n connecting all agents.

| Task | Time | Output |
|---|---|---|
| Build Visual Designer Agent (Claude Sonnet writes Matplotlib code, Claude Code executes) | 3 hrs | Produces `{id}_ig.png` and `{id}_fb.png` for 3 test topics |
| Implement Gate 4 brand compliance check (parse visual report .md) | 30 min | Gate 4 working; rejects off-brand visuals |
| Build WF-02 (Pipeline Orchestrator) in n8n (spawns Python subprocess, monitors completion) | 2.5 hrs | n8n triggers full CrewAI crew; reads output MD files |
| Build WF-01 (Topic Queue Sync, Monday cron) | 30 min | Reads approved Sheets rows; triggers WF-02 |
| Test full n8n-orchestrated pipeline with dry_run=true | 1.5 hrs | Full pipeline runs via n8n without publishing |

**Week 4 Total: ~8 hours**

---

#### Week 5: Human Review + Publishing

**Goal:** One-click approval → live on Instagram.

| Task | Time | Output |
|---|---|---|
| Deploy MCP Slack server; configure Slack app with interactive buttons | 1 hr | Slack app responding to button clicks |
| Build WF-03 (Human Review Notifier) — compiles package, sends Slack message | 1.5 hrs | Human receives Slack with preview, scores, action buttons |
| Set up Instagram Graph API app (Facebook Business → Developer App → IG API) | 2 hrs | Authenticated Instagram API; test post works |
| Build WF-04 (Publisher) — Approve button → Instagram post → Sheets log | 1.5 hrs | Approval publishes to Instagram and logs metadata |
| Build WF-06 (Error Alert Handler) | 30 min | Errors route to `#errors` Slack channel |
| Build WF-09 (Health Monitor) | 30 min | 6-hourly health pings; alerts on failure |
| Build WF-08 (Config Backup) | 30 min | Daily Drive backup of all config .md files |
| Full test with real content, Slack approval, Instagram publish | 1 hr | First automated post live on Instagram |

**Week 5 Total: ~8.5 hours**

---

#### Week 6: Integration Test + First Real Posts

**Goal:** System is stable, tested, and publishing real content consistently.

| Task | Time | Output |
|---|---|---|
| Run 5 topics through complete pipeline (non-dry-run) | 2 hrs | 5 content packages created |
| Human review all 5 packages; provide feedback for agent tuning | 1 hr | Feedback notes for prompt refinement |
| Tune prompts based on feedback (writing quality, style match, visual quality) | 1 hr | Agent prompts improved |
| Run 3 more topics with tuned agents; assess quality improvement | 1 hr | Quality assessment; ≥80% approval rate target |
| Publish 3 real posts to Instagram | 30 min | 3 live posts; first real audience interaction |
| Document MVP learnings; create post-MVP roadmap in GitHub Issues | 30 min | Roadmap documented for Month 2+ |

**Week 6 Total: ~6 hours**

---

### 12.4 MVP Build Summary

| Week | Focus | Human Hours | Key Output |
|---|---|---|---|
| 1 | Infrastructure & Config | 10 hrs | Droplet + n8n + MCP servers + all config .md files |
| 2 | Research & Strategist Agents | 9.5 hrs | Agents producing research .md files |
| 3 | Writing, Fact-Check, Style Agents | 11.5 hrs | Full text pipeline working |
| 4 | Visuals + n8n Orchestration | 8 hrs | Full pipeline in n8n with dry-run |
| 5 | Review + Publishing | 8.5 hrs | One-click Slack → Instagram |
| 6 | Integration Testing + Launch | 6 hrs | First 3 real posts published |
| **TOTAL** | | **~53 hours** | **Production-ready MVP** |

---

### 12.5 MVP Success Criteria

| Metric | Target | Measurement |
|---|---|---|
| Posts per week (steady state after Week 6) | 5-7 | Sheets Published log |
| Human time per post (review + approve) | <15 minutes | Self-tracked |
| Fact-check pass rate | ≥90% on first check | Automated log |
| Style score average | ≥80/100 | Automated log |
| Human first-review approval rate | ≥70% | Sheets status |
| System uptime | ≥95% | WF-09 health log |
| Pipeline end-to-end time | <45 minutes | n8n timestamps |
| Total monthly cost | <$50 | Invoice review |

---

### 12.6 Post-MVP Roadmap

| Month | Milestone | Key Additions |
|---|---|---|
| Month 2 | Volume Ramp | Facebook publishing (WF-04); Analytics Fetcher (WF-05); ramp to 15 posts/week |
| Month 3 | Quality & Brand Polish | Templated.io for professional infographics; style guide v2 based on first 60 posts; optimal posting schedule |
| Month 4 | Analytics & Learning | Monthly Reflection Agent (WF-07); engagement dashboard; top/bottom performer analysis |
| Month 5-6 | Scale | Target 20-30 posts/week; result caching for API cost reduction; potential Substack blog launch |
| Month 7+ | Advanced Features | A/B testing framework; audience Q&A integration; PostgreSQL migration if Sheets hitting limits |

---

## Appendix A: File & Folder Structure

```
/ (GitHub repo root)
├── README.md
├── .env.example                          # Template — never commit .env
│
├── config/                               # All Markdown configs
│   ├── writing_style_profile.md
│   ├── visual_identity.md
│   ├── editorial_preferences.md
│   ├── source_priority.md
│   ├── fact_check_protocols.md
│   └── platform_formatting.md
│
├── agents/                               # Python CrewAI agent code
│   ├── crew.py                           # Main crew definition
│   ├── strategist.py
│   ├── researcher.py
│   ├── writer.py
│   ├── fact_checker.py
│   ├── style_checker.py
│   ├── visual_designer.py
│   └── reflection.py
│
├── tools/                                # MCP tool wrappers for CrewAI
│   ├── mcp_fetch.py
│   ├── mcp_filesystem.py
│   ├── mcp_playwright.py
│   └── mcp_brave_search.py
│
├── n8n/                                  # n8n workflow export files (.json)
│   ├── WF-01_topic_queue_sync.json
│   ├── WF-02_pipeline_orchestrator.json
│   └── ...
│
├── docker-compose.yml                    # n8n + all services
├── docker-compose.mcp.yml               # MCP servers
│
└── docs/
    ├── bangladesh-content-platform-PRD.md
    └── bangladesh-system-architecture.md  # This document
```

**Runtime directories (on droplet, not in Git):**

```
/pipeline-data/
├── research/           # {topic_id}_research.md files
├── content/            # {topic_id}_draft.md files
├── reports/            # factcheck, stylecheck, visual .md reports
├── visuals/            # PNG output files
├── audit/              # pipeline_run_{id}_{timestamp}.md (reasoning logs)
└── topic_suggestions/  # Weekly topic suggestion .md files
```

---

## Appendix B: Glossary

| Term | Definition |
|---|---|
| **Agent** | A Claude/LLM instance with a specific role, set of MCP tools, and defined output format |
| **CrewAI** | Open-source Python framework for orchestrating multiple agents in sequence or parallel |
| **LiteLLM** | Universal LLM proxy that allows calling Claude, Gemini, or any LLM through a single interface |
| **MCP (Model Context Protocol)** | Anthropic's open protocol for giving AI models structured access to external tools and data sources |
| **MCP Server** | A small service (usually Node.js or Python) that implements the MCP protocol for a specific tool category (web fetch, filesystem, etc.) |
| **PRA Loop** | Perceive → Reason → Act → Reflect loop used by research and fact-checking agents |
| **HITL** | Human-in-the-Loop — design pattern where AI handles bulk work but humans approve at critical gates |
| **Gate** | An automated quality checkpoint that stops the pipeline if minimum quality standards are not met |
| **Dry-Run** | Pipeline execution mode that runs all agents but does not publish to social media |
| **Markdown-First** | Architectural principle that all config, data exchange, and reports use `.md` files as the canonical format |
| **LLM Fallback** | Automatic routing to Gemini API when Claude API rate limits are hit, via LiteLLM |

---

*Document Version: 2.0 | Revised February 22, 2026*  
*Supersedes: bangladesh-system-architecture v1.0 (DOCX)*  
*Next Review: March 22, 2026*