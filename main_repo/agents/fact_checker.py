"""
Fact-Checker Agent
Verifies every numerical claim in the draft against the original source URLs.
Follows fact_check_protocols.md exactly.

Tools used:
  - FetchWebPageTool: fetches source pages to verify numbers
  - ReadPDFTool: for PDF-based sources
"""
import os
from pathlib import Path
from crewai import Agent, Task, LLM

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools import FetchWebPageTool, ReadPDFTool


def _load_config(filename: str) -> str:
    config_dir = Path(os.getenv("CONFIG_DIR", Path(__file__).parent.parent / "config"))
    config_path = Path(config_dir) / filename
    if config_path.exists():
        return config_path.read_text(encoding="utf-8")
    return f"[WARNING: Config file {filename} not found]"


def _resolve_llm() -> LLM:
    model = os.getenv("PRIMARY_MODEL", "gemini/gemini-2.5-pro")
    api_key = (
        os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if model.startswith("gemini/")
        else os.getenv("ANTHROPIC_API_KEY")
    )
    return LLM(model=model, api_key=api_key, temperature=0.0, max_tokens=4096)


def build_fact_checker_agent() -> Agent:
    protocols = _load_config("fact_check_protocols.md")

    return Agent(
        role="Fact Verification Specialist",
        goal=(
            "Verify every numerical claim in the draft content against its original source. "
            "Never pass content that contains an unverified or inaccurately cited statistic. "
            "Trust is the product — one wrong number destroys the platform's credibility."
        ),
        backstory=f"""You are a rigorous fact-checker specializing in Bangladesh government
and economic statistics. You have zero tolerance for inaccurate numbers in published content.

Your verification process is methodical and documented. For every claim you check:
- You fetch the actual source URL
- You find the exact number in the source (not approximate, not estimated)
- You compare it precisely to what the draft says
- You document what you found and any discrepancy

YOUR FACT-CHECK PROTOCOLS (follow these exactly):
{protocols}

CRITICAL RULES:
- Temperature is 0.0 — you do not guess, infer, or estimate
- If you cannot access a source, mark the claim as UNVERIFIED, not PASS
- If a source says "at least 4%" and the draft says "4-6%", that is a FAIL
- Report exact wording differences — they matter for trust
- Never auto-correct a claim unless you have verified the correct figure from the source
- A claim that cannot be verified = a claim that cannot be published
""",
        tools=[FetchWebPageTool(), ReadPDFTool()],
        llm=_resolve_llm(),
        verbose=True,
        max_iter=15,   # Higher limit — may need to check multiple sources
        memory=False,
    )


def build_fact_check_task(
    fact_checker: Agent,
    draft_content: str,
    research_content: str,
    topic_id: str,
    output_path: str,
) -> Task:
    return Task(
        description=f"""
Fact-check the following draft content for topic {topic_id}.

DRAFT CONTENT TO VERIFY:
====================================================================
{draft_content}
====================================================================

RESEARCH REPORT (contains source URLs for each data point):
====================================================================
{research_content}
====================================================================

YOUR VERIFICATION PROCESS:
1. Extract every numerical claim from the draft (percentages, counts, rankings, dates)
2. For each claim, find the matching source URL in the research report
3. Fetch that URL using the Fetch Web Page tool
4. Locate the exact number in the page content
5. Compare: does the draft match the source exactly?
6. Assign confidence: High / Medium-High / Medium / Low / UNVERIFIED
7. Apply corrections for minor discrepancies (rounding, wording)
8. Flag anything that needs human review

APPLY THESE THRESHOLDS (from protocols):
- ≥90/100 overall → PASS (proceed to style check)
- 85–89/100 → PASS WITH CORRECTIONS (apply fixes, proceed)
- <85/100 → FAIL (return to research/writer with specific issues)
- Any ESCALATE trigger → ESCALATE TO HUMAN

OUTPUT FORMAT — Write this exactly:

---
# Fact-Check Report: {topic_id}
**Date:** [today]
**Agent:** Fact-Checker v1.0
**Overall Result:** [PASS / PASS WITH CORRECTIONS / FAIL / ESCALATE]
**Overall Confidence Score:** [X/100]

---
## Claim-by-Claim Results

### Claim 1: "[exact text of claim from draft]"
- **Source cited in draft:** [source name]
- **Source URL fetched:** [URL]
- **Value found in source:** [exact value as it appears]
- **Draft value:** [what the draft says]
- **Result:** [MATCH / CORRECTED / DISCREPANCY / UNVERIFIED]
- **Confidence:** [High / Medium-High / Medium / Low]
- **Action:** [None / Corrected to X / Flagged]

[Repeat for every numerical claim]

---
## Corrected Draft
[If any corrections were applied, write the FULL corrected Instagram caption here.
If no corrections needed, write "No corrections needed — original draft stands."]

---
## Human Review Flags
[List anything requiring human judgment]

---
## Verification Notes
[Any methodology notes, source access issues, or important observations]

Save this report to: {output_path}
""",
        expected_output=f"A complete fact-check report with claim-by-claim results saved to {output_path}",
        output_file=output_path,
        agent=fact_checker,
    )
