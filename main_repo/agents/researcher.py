"""
Research Agent
Autonomously researches Bangladesh data topics from trusted government
and international sources. Outputs a structured research markdown file.

Reads config from:
  - config/source_priority.md   (which sources to trust and in what order)
  - config/editorial_preferences.md (what topics and framing to use)
"""
import os
from pathlib import Path
from crewai import Agent, Task, LLM

# Import tools from sibling package
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools import FetchWebPageTool, WebSearchTool, ReadPDFTool


def _load_config(filename: str) -> str:
    config_dir = Path(os.getenv("CONFIG_DIR", Path(__file__).parent.parent / "config"))
    config_path = Path(config_dir) / filename
    if config_path.exists():
        return config_path.read_text(encoding="utf-8")
    return f"[WARNING: Config file {filename} not found at {config_path}]"


def build_researcher_agent() -> Agent:
    source_priority = _load_config("source_priority.md")
    editorial_prefs = _load_config("editorial_preferences.md")

    model = os.getenv("PRIMARY_MODEL", "gemini/gemini-2.5-pro")
    # Route API key based on which provider is being used
    if model.startswith("gemini/"):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    else:
        api_key = os.getenv("ANTHROPIC_API_KEY")

    llm = LLM(
        model=model,
        api_key=api_key,
        temperature=0.1,   # Low temp for factual research — we want accuracy, not creativity
        max_tokens=4096,
    )

    return Agent(
        role="Bangladesh Data Researcher",
        goal=(
            "Find accurate, verifiable data about Bangladesh from trusted government "
            "and international sources. Every data point you return must have a source URL. "
            "You never fabricate numbers. If you cannot find data, you say so clearly."
        ),
        backstory=f"""You are a meticulous data researcher specializing in Bangladesh's
political, economic, and social statistics. You have deep knowledge of where to find
authoritative Bangladesh data — from the Bangladesh Bureau of Statistics (BBS),
Bangladesh Bank, the Ministry of Finance, and international bodies like the World Bank,
UNESCO, and IMF.

You follow a strict Perception-Reasoning-Action-Reflection (PRAR) loop:
1. PERCEIVE: Read the topic and understand exactly what data is needed
2. REASON: Identify the best sources to check (always try Tier 1 first)
3. ACT: Search the web, fetch pages, and extract the specific numbers
4. REFLECT: Verify consistency across sources; flag any gaps or discrepancies

YOUR SOURCE PRIORITY RULES (follow these exactly):
{source_priority}

YOUR EDITORIAL GUIDELINES (use these to frame the research):
{editorial_prefs}

CRITICAL RULES:
- Never invent or estimate numbers — only report what you find in actual sources
- Every data point must include its exact source URL
- If BBS data has gaps, try World Bank next, then UNESCO, then IMF
- If sources disagree, report both values and explain the difference
- Flag any data that scores Medium or Low confidence
- Disclose any data interpolation or estimation clearly
""",
        tools=[WebSearchTool(), FetchWebPageTool(), ReadPDFTool()],
        llm=llm,
        verbose=True,
        max_iter=12,       # Max tool-call iterations before stopping
        memory=False,      # Stateless per-run; session state is in output files
    )


def build_research_task(
    researcher: Agent,
    topic_id: str,
    topic_english: str,
    topic_bangla: str,
    context_notes: str,
    output_path: str,
) -> Task:
    """
    Build the research task for a given topic.

    Args:
        topic_id:       Unique ID, e.g. "T001"
        topic_english:  Topic in English, e.g. "Education Spending Comparison"
        topic_bangla:   Topic in Bangla, e.g. "শিক্ষা খরচ তুলনা"
        context_notes:  Human-provided context, e.g. "Compare 1996-2001 vs 2009-2024"
        output_path:    Full path where the research .md file will be written
    """
    return Task(
        description=f"""
Research the following topic for the Bangladesh Data Content Platform.

TOPIC ID: {topic_id}
TOPIC (English): {topic_english}
TOPIC (Bangla): {topic_bangla}
CONTEXT NOTES FROM EDITOR: {context_notes}

YOUR RESEARCH PROCESS:
========================

STEP 1 — PERCEIVE & PLAN
Understand exactly what data points are needed for this topic.
Ask yourself:
- What specific metrics are needed? (percentages, absolute values, rankings?)
- What time periods are relevant?
- Which Tier 1 sources are most likely to have this data?

STEP 2 — SEARCH
Use the Web Search tool to find relevant sources.
Search queries should be specific. Examples:
- "Bangladesh education budget percent GDP BBS 2023"
- "site:data.worldbank.org Bangladesh education expenditure"
- "UNESCO education spending Bangladesh site:uis.unesco.org"

Always try Bangladesh government sources first (BBS, Bangladesh Bank, Ministry of Finance).

STEP 3 — FETCH & EXTRACT
Use the Fetch Web Page tool to read the actual source pages.
Use the Read PDF tool for any PDF documents.
Extract the exact numbers — not approximate, not estimated.

STEP 4 — CROSS-REFERENCE
For every key data point, try to verify it with a second source.
If sources disagree, note both values and the methodology difference.

STEP 5 — ASSESS CONFIDENCE
For each data point, assign a confidence level:
- High: Verified against Tier 1 source, exact match with raw data
- Medium-High: Verified against Tier 2 source (World Bank, UNESCO, etc.)
- Medium: Single source, could not cross-reference
- Low: Estimated or interpolated — must be flagged in output

STEP 6 — WRITE OUTPUT
Write a structured research file to: {output_path}

OUTPUT FORMAT (write this exact structure):
===========================================

# Research Report: {topic_id} — {topic_english}
**Topic (Bangla):** {topic_bangla}
**Research Date:** [today's date]
**Researcher Agent:** v1.0
**Overall Confidence:** [High / Medium-High / Medium / Low]

---

## Research Summary
[2-3 sentence summary of what was found and overall data quality]

---

## Data Points

### [Data Point Name, e.g., "Education Budget 1996-2001"]
- **Value:** [exact value with unit, e.g., "2.1% of GDP"]
- **Time Period:** [exact year or range]
- **Source Name:** [e.g., "UNESCO Institute for Statistics"]
- **Source URL:** [exact URL]
- **Source Section:** [e.g., "Table 3.2, page 14" or "Education Indicators dataset"]
- **Confidence:** [High / Medium-High / Medium / Low]
- **Notes:** [any caveats, methodology notes, or discrepancies]

[Repeat for each data point]

---

## Source Conflicts & Discrepancies
[List any cases where two sources gave different numbers, and explain why]

---

## Data Gaps & Missing Information
[List any data points that could not be found, and what was tried]

---

## Human Review Flags
[List any issues that require human judgment before this data is used in content]

---

## Recommended Content Angle
[Based on the data, suggest 1-2 honest, neutral content angles.
Do not editorialize — just suggest what the data naturally suggests.]

---

## Sources Used
[Numbered list of all URLs actually accessed]
""",
        expected_output=f"A complete research report saved as a markdown file at {output_path}",
        output_file=output_path,
        agent=researcher,
    )
