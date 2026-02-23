"""
Style Checker Agent
Scores the draft content against the writing style guide on 10 dimensions.
Uses the fast model — this is a lightweight evaluation task.

Reads config from:
  - config/writing_style_profile.md
"""
import os
from pathlib import Path
from crewai import Agent, Task, LLM


def _load_config(filename: str) -> str:
    config_dir = Path(os.getenv("CONFIG_DIR", Path(__file__).parent.parent / "config"))
    config_path = Path(config_dir) / filename
    if config_path.exists():
        return config_path.read_text(encoding="utf-8")
    return f"[WARNING: Config file {filename} not found]"


def _resolve_fast_llm() -> LLM:
    # Style checking uses the FAST (cheaper) model — it's a structured evaluation task
    model = os.getenv("FAST_MODEL", "gemini/gemini-2.5-flash")
    api_key = (
        os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if model.startswith("gemini/")
        else os.getenv("ANTHROPIC_API_KEY")
    )
    return LLM(model=model, api_key=api_key, temperature=0.1, max_tokens=2048)


def build_style_checker_agent() -> Agent:
    style_profile = _load_config("writing_style_profile.md")

    return Agent(
        role="Quality Control Editor",
        goal=(
            "Score draft content against the platform's writing style guide on 10 dimensions. "
            "Identify specific deviations with line-level feedback. "
            "Approve content that scores ≥85/100 or provide precise corrections."
        ),
        backstory=f"""You are a meticulous quality control editor who knows the platform
voice inside and out. You have read hundreds of example posts and can immediately tell
whether a draft "sounds right" for this platform.

Your job is NOT to rewrite the content. Your job is to:
1. Score it objectively on 10 defined dimensions
2. Point to specific lines or phrases that don't match the style
3. Suggest minimal targeted fixes
4. Give a clear PASS or FAIL verdict

THE COMPLETE STYLE GUIDE YOU ENFORCE:
{style_profile}

YOUR 10 SCORING DIMENSIONS (from the Style Checker Scoring Rubric in the style guide):
1. Tone (conversational, not preachy) — 15 points
2. Bangla-English ratio (70% Bangla / 30% English target in body) — 15 points
3. No partisan language (no party/leader credit or blame) — 15 points
4. Source citation present (every number has a source) — 15 points
5. Engagement question included (open-ended, not leading) — 10 points
6. Post structure followed (Hook → Data → Context → Question → Source) — 10 points
7. Sentence length appropriate (avg 15-20 words) — 5 points
8. Emoji count correct (2-3 max total) — 5 points
9. Hashtag count correct (3-5 only, no partisan tags) — 5 points
10. Overall "sounds authentic" (holistic judgment) — 5 points

PASS THRESHOLDS:
- ≥85/100 → PASS (proceed to human review)
- 80–84/100 → MARGINAL (apply targeted fixes and re-score)
- <80/100 → FAIL (return to writer with detailed feedback)
- <75/100 after 2 attempts → ESCALATE TO HUMAN
""",
        tools=[],   # Pure text evaluation — no web access needed
        llm=_resolve_fast_llm(),
        verbose=True,
        max_iter=3,
        memory=False,
    )


def build_style_check_task(
    style_checker: Agent,
    draft_content: str,
    fact_check_result: str,
    topic_id: str,
    output_path: str,
) -> Task:
    # Extract the corrected draft from the fact-check report if corrections were applied
    return Task(
        description=f"""
Score and validate this draft content for topic {topic_id} against the style guide.

DRAFT TO EVALUATE (use the corrected version if fact-checker made changes):
====================================================================
{draft_content}
====================================================================

FACT-CHECK RESULT (for context — check if the corrected draft was provided there):
====================================================================
{fact_check_result}
====================================================================

IMPORTANT: If the fact-checker's report contains a "Corrected Draft" section,
evaluate THAT version, not the original above.

YOUR EVALUATION PROCESS:
1. Identify which version of the draft to evaluate (original or fact-corrected)
2. Score each of the 10 dimensions from your style guide
3. For any dimension scoring below its maximum:
   - Quote the specific line/phrase that caused the deduction
   - Explain why it doesn't match the style guide
   - Suggest the minimal fix
4. Calculate the total score
5. Give PASS / MARGINAL / FAIL verdict

OUTPUT FORMAT — Write this exactly:

---
# Style Check Report: {topic_id}
**Date:** [today]
**Agent:** Style Checker v1.0
**Draft version evaluated:** [Original / Fact-Corrected]
**Overall Result:** [PASS / MARGINAL / FAIL / ESCALATE]
**Total Score:** [X/100]

---
## Dimension Scores

| # | Dimension | Score | Max | Notes |
|---|---|---|---|---|
| 1 | Tone (conversational) | X | 15 | [specific note] |
| 2 | Bangla-English ratio | X | 15 | [estimated ratio] |
| 3 | No partisan language | X | 15 | [any flags] |
| 4 | Source citations | X | 15 | [all cited?] |
| 5 | Engagement question | X | 10 | [present? open-ended?] |
| 6 | Post structure | X | 10 | [follows template?] |
| 7 | Sentence length | X | 5 | [avg word count] |
| 8 | Emoji count | X | 5 | [count found] |
| 9 | Hashtag count | X | 5 | [count found] |
| 10 | Overall authenticity | X | 5 | [holistic judgment] |
| **TOTAL** | | **X** | **100** | |

---
## Issues Found
[For each deducted point, quote the specific line and explain the issue]

---
## Suggested Fixes
[Minimal targeted fixes only — do not rewrite the whole post]

---
## Final Approved Draft (Instagram Caption)
[Write the final approved Instagram caption here, with any fixes applied.
If no fixes needed, copy the draft as-is.]

---
## Final Approved Draft (Facebook Post)
[Write the final approved Facebook post here, with any fixes applied.]

Save this report to: {output_path}
""",
        expected_output=f"A style compliance report with scores and approved final draft saved to {output_path}",
        output_file=output_path,
        agent=style_checker,
    )
