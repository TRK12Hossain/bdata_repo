"""
Visual Designer — hybrid matplotlib + Pillow approach.

Uses LiteLLM directly (no CrewAI wrapper) to generate chart code,
then executes it via PythonExecutorTool.

matplotlib  → chart data, English axis labels
Pillow+Raqm → Bengali headline (Bangla Sangam MN system font)

Gate 4 validates output: 1080x1080, PNG, <1MB.
"""
import os
import re
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent
_TEMPLATE_PATH = _REPO_ROOT / "assets" / "chart_template.py"

sys.path.insert(0, str(_REPO_ROOT))
from tools.python_executor import PythonExecutorTool


def _load_template() -> str:
    return _TEMPLATE_PATH.read_text(encoding="utf-8") if _TEMPLATE_PATH.exists() else ""


def _resolve_model_and_key() -> tuple[str, str]:
    model = os.getenv("FAST_MODEL", os.getenv("PRIMARY_MODEL", "gemini/gemini-2.5-flash"))
    api_key = (
        os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if model.startswith("gemini/")
        else os.getenv("ANTHROPIC_API_KEY")
    )
    return model, api_key


def _call_llm(prompt: str) -> str:
    """Call LiteLLM directly — no CrewAI overhead."""
    import litellm
    model, api_key = _resolve_model_and_key()
    resp = litellm.completion(
        model=model,
        api_key=api_key,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""


def _extract_code(text: str) -> str:
    """Pull the first Python code block from the LLM response."""
    # Try ```python ... ``` first
    m = re.search(r"```python\s*(.*?)```", text, re.DOTALL)
    if m:
        code = m.group(1).strip()
        if code and not code.startswith("`"):
            return code

    # Try any generic fenced block (handles ``` without language tag)
    m = re.search(r"```\s*(.*?)```", text, re.DOTALL)
    if m:
        code = m.group(1).strip()
        # Drop leading language identifier line if LLM put it inside the fence
        if code.startswith("python\n"):
            code = code[7:]
        if code and not code.startswith("`"):
            return code

    # Last resort: strip all leading/trailing fence lines from the raw text
    lines = text.strip().splitlines()
    while lines and lines[0].strip().startswith("`"):
        lines.pop(0)
    while lines and lines[-1].strip().startswith("`"):
        lines.pop()
    return "\n".join(lines).strip()


def generate_visual(
    approved_draft: str,
    research_content: str,
    topic_id: str,
    output_path_ig: str,
) -> dict:
    """
    Generate an infographic PNG for the given topic.
    Returns dict with keys: passed, output_path, error (if any).
    """
    template = _load_template()

    prompt = f"""You are a Python data visualisation expert. Generate chart code for a Bangladesh data infographic.

APPROVED INSTAGRAM CAPTION (source of headline and data):
{approved_draft}

RESEARCH DATA (use these exact numbers):
{research_content[:2500]}

CHART TEMPLATE — copy this structure exactly and fill in the blanks:
{template}

INSTRUCTIONS:
1. Read the caption above and extract the key data points and source name.
2. Fill in "YOUR CHART CODE HERE" with a horizontal bar chart (or line chart if showing a trend).
3. Set headline_raw to the FIRST LINE of the approved caption.
4. Set source_text to a plain-text source name (no emoji).
5. Set output_path to: {output_path_ig}
6. Use ENGLISH for all matplotlib axis labels. Bengali goes only in headline_raw.
7. Use BRAND['green'] for ALL bars. Use BRAND['red'] only for reference lines.
8. Keep ax = fig.add_axes([0.18, 0.12, 0.74, 0.50]) unchanged.
9. Do NOT use bbox_inches='tight'.

Respond with ONLY the complete Python code, inside a ```python block."""

    executor = PythonExecutorTool()

    for attempt in range(3):
        try:
            print(f"[Visual] Generating code (attempt {attempt + 1}/3)...")
            llm_response = _call_llm(prompt)
            code = _extract_code(llm_response)

            if not code or len(code) < 200 or code.startswith("`"):
                print(f"[Visual] Code extraction failed ({len(code)} chars), retrying...")
                continue

            print(f"[Visual] Executing chart code ({len(code)} chars)...")
            result = executor._run(code)

            if "Chart saved:" in result or "saved" in result.lower():
                print(f"[Visual] Execution succeeded: {result.strip()}")
                return {"passed": True, "output_path": output_path_ig, "error": None}
            else:
                print(f"[Visual] Execution output unexpected: {result[:200]}")
                # Give the code the benefit of the doubt — check if file exists
                if Path(output_path_ig).exists():
                    return {"passed": True, "output_path": output_path_ig, "error": None}
                # Inject the error into the next prompt for self-correction
                prompt += f"\n\nThe previous code produced this error — fix it:\n{result[:500]}"

        except Exception as e:
            print(f"[Visual] Attempt {attempt + 1} error: {e}")
            if attempt == 2:
                return {"passed": False, "output_path": output_path_ig, "error": str(e)}

    return {"passed": False, "output_path": output_path_ig, "error": "Failed after 3 attempts"}


def validate_visual_output(output_path: str) -> dict:
    """Gate 4: check file exists, is PNG, ~1080x1080, <1MB."""
    from PIL import Image
    failures = []
    path = Path(output_path)

    if not path.exists():
        return {"passed": False, "failures": ["Output file does not exist"]}

    size_kb = path.stat().st_size / 1024
    if size_kb > 1024:
        failures.append(f"File size {size_kb:.0f}KB exceeds 1MB")

    try:
        img = Image.open(output_path)
        w, h = img.size
        if not (1070 <= w <= 1090 and 1070 <= h <= 1090):
            failures.append(f"Dimensions {w}x{h} — expected ~1080x1080")
        if img.format != "PNG":
            failures.append(f"Format {img.format} — expected PNG")
    except Exception as e:
        failures.append(f"Cannot open image: {e}")
        w, h = 0, 0

    return {
        "passed": len(failures) == 0,
        "failures": failures,
        "size_kb": size_kb,
        "dimensions": f"{w}x{h}",
    }
