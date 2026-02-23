"""
Visual Designer Agent
Reads the approved draft and research data, then generates a branded
infographic as a 1080x1080 PNG using Matplotlib.

Follows visual_identity.md rules exactly.
Uses PythonExecutorTool to render the chart code it writes.
Gate 4 validates the output (dimensions, file size, existence).
"""
import os
from pathlib import Path
from crewai import Agent, Task, LLM

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.python_executor import PythonExecutorTool


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
    return LLM(model=model, api_key=api_key, temperature=0.2, max_tokens=8192)


def build_visual_designer_agent() -> Agent:
    visual_identity = _load_config("visual_identity.md")

    return Agent(
        role="Data Visualization Designer",
        goal=(
            "Generate a branded infographic PNG for Instagram (1080x1080) "
            "that visually tells the data story from the approved draft. "
            "The chart must be honest, readable on mobile, and comply with brand rules."
        ),
        backstory=f"""You are a data visualization expert who creates clean, honest,
mobile-friendly infographics about Bangladesh. You write Python Matplotlib code to
generate charts, then use the Execute Chart Code tool to render them.

YOUR VISUAL IDENTITY RULES (follow exactly):
{visual_identity}

AVAILABLE FONTS ON THIS SYSTEM:
- Bangla text: use fontfamily='Bangla MN' (verified working for Bengali Unicode)
- English text: use fontfamily='DejaVu Sans' (matplotlib default, clean and reliable)
- Numbers/data labels: use fontfamily='DejaVu Sans', fontweight='bold'

CHART CODE TEMPLATE (always start from this structure):
```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Brand constants — do not change these
BRAND = {{
    'green':      '#006A4E',
    'red':        '#F42A41',
    'white':      '#FFFFFF',
    'off_white':  '#F5F5F0',
    'dark':       '#1A1A1A',
    'gray':       '#6B7280',
    'light_gray': '#E5E7EB',
}}

# Canvas: 1080x1080 at 100dpi
fig = plt.figure(figsize=(10.8, 10.8), dpi=100)
fig.patch.set_facecolor(BRAND['off_white'])

# Chart axes — leave room for headline (top 25%) and footer (bottom 12%)
ax = fig.add_axes([0.1, 0.18, 0.80, 0.58])
ax.set_facecolor(BRAND['off_white'])

# === YOUR CHART CODE HERE ===
# (bars, lines, labels, etc.)

# Headline — Bangla text at top
fig.text(0.5, 0.90, 'HEADLINE IN BANGLA', ha='center', va='top',
         fontsize=26, fontweight='bold', fontfamily='Bangla MN',
         color=BRAND['dark'], wrap=True)

# Optional sub-headline in English
fig.text(0.5, 0.83, 'English sub-headline if needed', ha='center', va='top',
         fontsize=14, fontfamily='DejaVu Sans', color=BRAND['gray'])

# Source watermark — MANDATORY, always at bottom-left
fig.text(0.04, 0.025, '📊 Source: SOURCE NAME', fontsize=11,
         fontfamily='DejaVu Sans', color=BRAND['gray'], alpha=0.85)

# Save — do NOT use bbox_inches='tight' (it changes dimensions from 1080x1080)
output_path = 'REPLACE_WITH_ACTUAL_PATH'
plt.savefig(output_path, dpi=100, bbox_inches=None,
            facecolor=BRAND['off_white'], format='png')
plt.close()
print(f"Chart saved: {{output_path}}")
```

CHART TYPE SELECTION:
- Comparing exactly 2 time periods → grouped or side-by-side bar chart
- Trend over 4+ data points → line chart with marked data points
- Single striking statistic → large centered number (no axes)
- Multiple metrics across periods → horizontal grouped bar chart

CRITICAL RULES:
- Bar charts: y-axis ALWAYS starts at 0
- Data labels: always show the value on each bar/point
- Reference lines (UNESCO benchmarks etc.): use BRAND['red'] dashed line
- Both periods same color (BRAND['green']) — never color-code periods differently
- Minimum font size 12pt anywhere on the chart
- Always print the output path as the last stdout line
""",
        tools=[PythonExecutorTool()],
        llm=_resolve_llm(),
        verbose=True,
        max_iter=6,    # Allow retries if first render has errors
        memory=False,
    )


def validate_visual_output(output_path: str) -> dict:
    """
    Gate 4: Automated brand compliance check.
    Returns dict with passed=True/False and list of failures.
    """
    from PIL import Image

    failures = []
    path = Path(output_path)

    if not path.exists():
        return {"passed": False, "failures": ["Output file does not exist"]}

    # File size check
    size_kb = path.stat().st_size / 1024
    if size_kb > 1024:
        failures.append(f"File size {size_kb:.0f}KB exceeds 1MB limit")

    # Image dimensions check
    try:
        img = Image.open(output_path)
        w, h = img.size
        if not (1070 <= w <= 1090 and 1070 <= h <= 1090):
            failures.append(f"Dimensions {w}x{h} — expected ~1080x1080")
        if img.format != "PNG":
            failures.append(f"File format {img.format} — expected PNG")
    except Exception as e:
        failures.append(f"Cannot open image: {e}")

    return {
        "passed": len(failures) == 0,
        "failures": failures,
        "size_kb": size_kb,
        "dimensions": f"{w}x{h}" if "w" in dir() else "unknown",
    }


def build_visual_designer_task(
    designer: Agent,
    approved_draft: str,
    research_content: str,
    topic_id: str,
    output_path_ig: str,
) -> Task:
    return Task(
        description=f"""
Create a branded infographic for topic {topic_id}.

APPROVED INSTAGRAM CAPTION (use this for headline and data):
====================================================================
{approved_draft}
====================================================================

RESEARCH DATA (for exact numbers and source attribution):
====================================================================
{research_content}
====================================================================

YOUR TASK:
1. Read the approved caption above
2. Extract the key data points (the numbers, time periods, and source)
3. Identify the best chart type:
   - If the caption compares 2 time periods → bar chart (side by side)
   - If the caption shows a trend → line chart
   - If the caption has one big stat → large number layout
4. Write complete Python Matplotlib code following the template in your guide
5. Set the headline to the FIRST LINE of the approved caption (in Bangla)
6. Execute the code using the 'Execute Chart Code' tool
7. If it fails, read the error, fix the code, and try again (up to 3 times)
8. Confirm the file was saved successfully

OUTPUT FILE PATH (use this exact path):
{output_path_ig}

CHECKLIST before running the code:
- [ ] Y-axis starts at 0 (for bar charts)
- [ ] Data labels visible on every bar/point
- [ ] Source watermark at bottom-left with 📊
- [ ] Headline is the first line of the approved caption
- [ ] Output saved to: {output_path_ig}
- [ ] plt.savefig uses bbox_inches=None (NOT 'tight') so dimensions stay exactly 1080x1080
- [ ] plt.close() called after savefig
- [ ] print(f"Chart saved: {{output_path}}") is the last line

After successful execution, confirm:
"Visual saved to {output_path_ig}"
""",
        expected_output=f"Infographic PNG saved to {output_path_ig} and confirmed with Gate 4 check",
        agent=designer,
    )
