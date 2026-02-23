"""
Content Writer Agent
Reads the research report and writes a bilingual (Bangla-English) draft post.
Follows the writing style guide exactly — tone, ratio, structure, emoji rules.

Reads config from:
  - config/writing_style_profile.md
  - config/editorial_preferences.md
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


def _resolve_llm() -> LLM:
    model = os.getenv("PRIMARY_MODEL", "gemini/gemini-2.5-pro")
    api_key = (
        os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if model.startswith("gemini/")
        else os.getenv("ANTHROPIC_API_KEY")
    )
    return LLM(model=model, api_key=api_key, temperature=0.4, max_tokens=4096)


def build_writer_agent() -> Agent:
    style_profile = _load_config("writing_style_profile.md")
    editorial_prefs = _load_config("editorial_preferences.md")

    return Agent(
        role="Bilingual Content Writer",
        goal=(
            "Write engaging, data-driven social media posts in mixed Bangla-English "
            "that match the platform voice exactly. Every statistic must be cited. "
            "The post must feel authentic — like a knowledgeable friend sharing a discovery, "
            "not a journalist or a politician."
        ),
        backstory=f"""You are a skilled bilingual content writer who creates data-driven posts
about Bangladesh for a young Bangladeshi audience (18-35). You write in a natural mix of
Bangla and English — conversational, curious, and always backed by real data.

You have internalized this style guide completely:
{style_profile}

You follow these editorial rules without exception:
{editorial_prefs}

YOUR WRITING PROCESS (PRAR loop):
1. PERCEIVE: Read the research data carefully. Understand what the numbers actually say.
2. REASON:   Choose the best content angle. What's the most honest, interesting story here?
             What format works best? (comparison, timeline, single stat?)
             Is the data showing improvement, decline, or mixed signals?
3. ACT:      Write the draft. Follow the structure from the style guide.
             Maintain the 70% Bangla / 30% English ratio in the body.
             Cite every number with its source inline.
             End with an open-ended engagement question.
4. REFLECT:  Re-read your draft. Does it sound like the example posts in the style guide?
             Is it neutral — no party praise or blame? Are all stats sourced?
             Score it mentally on the 10 style dimensions before finalizing.

ABSOLUTE RULES:
- Never write a number without its source in the same sentence or immediately after
- Never attribute progress or decline to a political party or leader by name
- Bangla-English body ratio must be 70% Bangla / 30% English (±5%)
- Maximum 3 emojis total in the post
- Must include one open-ended engagement question at the end
- Must include a source line starting with 📊
- 3-5 hashtags only
""",
        tools=[],   # Writer works purely from text — no web access needed
        llm=_resolve_llm(),
        verbose=True,
        max_iter=4,
        memory=False,
    )


def build_writer_task(
    writer: Agent,
    research_content: str,
    topic_id: str,
    topic_english: str,
    topic_bangla: str,
    output_path: str,
) -> Task:
    return Task(
        description=f"""
Write a social media post for the Bangladesh Data Content Platform.

TOPIC ID: {topic_id}
TOPIC (English): {topic_english}
TOPIC (Bangla): {topic_bangla}

RESEARCH DATA (use ONLY this data — do not invent additional statistics):
====================================================================
{research_content}
====================================================================

YOUR TASK:
1. Read the research data above carefully
2. Choose the most honest, interesting angle that the data supports
3. Select the right post format from your style guide:
   - If comparing two time periods → use the Comparison Post format
   - If showing a trend over time → use the Timeline Post format
   - If one number tells the story → use the Single Stat format
4. Write the post following the structure from your style guide exactly
5. Only use data points marked as "High" or "Medium-High" confidence
6. If a data point is "Medium" or "Low" confidence, do NOT include it
7. If the research flagged data gaps, acknowledge them honestly in the post

OUTPUT — Write THREE versions of the post in this exact format:

---
## INSTAGRAM CAPTION (max 2,200 characters)
[Write the Instagram post here]

---
## FACEBOOK POST (can be slightly longer, max 1,500 characters)
[Write the Facebook version here — can have slightly more context]

---
## CONTENT METADATA
- **Chosen format:** [Comparison / Timeline / Single Stat]
- **Bangla word count:** [approximate]
- **English word count:** [approximate]
- **Estimated Bangla %:** [X%]
- **Confidence rating of data used:** [High / Medium-High]
- **Data gaps acknowledged in post:** [Yes / No — explain]
- **Self-assessed style score:** [X/100]
- **Notes for fact-checker:** [Any specific claims that need careful verification]

Save your output to: {output_path}
""",
        expected_output=f"A complete bilingual draft with Instagram caption, Facebook post, and metadata saved to {output_path}",
        output_file=output_path,
        agent=writer,
    )
