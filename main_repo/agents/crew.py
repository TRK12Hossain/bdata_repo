"""
Crew Orchestrator
Chains all agents in sequence:
  Researcher → Writer → Fact-Checker → Style-Checker → Visual Designer

Each agent's output is written to a file and passed as text to the next agent.
Called by the CLI scripts and later by n8n workflows.
"""
import os
import re
from pathlib import Path
from datetime import datetime
from crewai import Crew, Process

from .researcher import build_researcher_agent, build_research_task
from .writer import build_writer_agent, build_writer_task
from .fact_checker import build_fact_checker_agent, build_fact_check_task
from .style_checker import build_style_checker_agent, build_style_check_task
from .visual_designer import generate_visual, validate_visual_output


def _now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _run_single_agent_crew(agent, task) -> str:
    """Run one agent + one task, return the raw output as a string."""
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )
    result = crew.kickoff()
    return str(result.raw) if hasattr(result, "raw") else str(result)


def run_research_crew(
    topic_id: str,
    topic_english: str,
    topic_bangla: str,
    context_notes: str,
    pipeline_data_dir: str = None,
) -> dict:
    """Run only the Research Agent. Returns output path."""
    pipeline_data_dir = pipeline_data_dir or os.getenv(
        "PIPELINE_DATA_DIR",
        str(Path(__file__).parent.parent.parent / "pipeline-data")
    )
    research_dir = Path(pipeline_data_dir) / "research"
    research_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(research_dir / f"{topic_id}_research_{_now()}.md")

    try:
        researcher = build_researcher_agent()
        task = build_research_task(
            researcher=researcher,
            topic_id=topic_id,
            topic_english=topic_english,
            topic_bangla=topic_bangla,
            context_notes=context_notes,
            output_path=output_path,
        )
        output = _run_single_agent_crew(researcher, task)
        Path(output_path).write_text(output, encoding="utf-8")
        return {"status": "success", "topic_id": topic_id, "output_path": output_path, "error": None}
    except Exception as e:
        return {"status": "error", "topic_id": topic_id, "output_path": output_path, "error": str(e)}


def run_full_pipeline(
    topic_id: str,
    topic_english: str,
    topic_bangla: str,
    context_notes: str,
    pipeline_data_dir: str = None,
    existing_research_path: str = None,
) -> dict:
    """
    Run the full pipeline: Research → Write → Fact-Check → Style-Check.

    If existing_research_path is provided, skips the research step and uses
    that file directly (useful for re-running the pipeline on existing research).

    Returns a dict with paths to all output files and final status.
    """
    pipeline_data_dir = pipeline_data_dir or os.getenv(
        "PIPELINE_DATA_DIR",
        str(Path(__file__).parent.parent.parent / "pipeline-data")
    )

    # Create all output directories
    for subdir in ["research", "content", "reports"]:
        Path(pipeline_data_dir, subdir).mkdir(parents=True, exist_ok=True)

    ts = _now()
    paths = {
        "research":    str(Path(pipeline_data_dir) / "research"  / f"{topic_id}_research_{ts}.md"),
        "draft":       str(Path(pipeline_data_dir) / "content"   / f"{topic_id}_draft_{ts}.md"),
        "fact_check":  str(Path(pipeline_data_dir) / "reports"   / f"{topic_id}_factcheck_{ts}.md"),
        "style_check": str(Path(pipeline_data_dir) / "reports"   / f"{topic_id}_stylecheck_{ts}.md"),
        "visual_ig":   str(Path(pipeline_data_dir) / "visuals"   / f"{topic_id}_ig_{ts}.png"),
    }
    Path(pipeline_data_dir, "visuals").mkdir(parents=True, exist_ok=True)

    results = {
        "topic_id": topic_id,
        "paths": paths,
        "stages": {},
        "final_status": "pending",
        "error": None,
    }

    # ── STAGE 1: RESEARCH ────────────────────────────────────────────────────
    if existing_research_path and Path(existing_research_path).exists():
        print(f"\n[Pipeline] Skipping research — using existing file: {existing_research_path}")
        research_content = Path(existing_research_path).read_text(encoding="utf-8")
        paths["research"] = existing_research_path
        results["stages"]["research"] = "skipped (existing file used)"
    else:
        print(f"\n[Pipeline] Stage 1/4: Research Agent starting...")
        try:
            researcher = build_researcher_agent()
            research_task = build_research_task(
                researcher=researcher,
                topic_id=topic_id,
                topic_english=topic_english,
                topic_bangla=topic_bangla,
                context_notes=context_notes,
                output_path=paths["research"],
            )
            research_content = _run_single_agent_crew(researcher, research_task)
            Path(paths["research"]).write_text(research_content, encoding="utf-8")
            results["stages"]["research"] = "completed"
            print(f"[Pipeline] Research done → {paths['research']}")
        except Exception as e:
            results["stages"]["research"] = f"failed: {e}"
            results["final_status"] = "failed_at_research"
            results["error"] = str(e)
            return results

    # ── STAGE 2: WRITE ───────────────────────────────────────────────────────
    print(f"\n[Pipeline] Stage 2/4: Content Writer Agent starting...")
    try:
        writer = build_writer_agent()
        write_task = build_writer_task(
            writer=writer,
            research_content=research_content,
            topic_id=topic_id,
            topic_english=topic_english,
            topic_bangla=topic_bangla,
            output_path=paths["draft"],
        )
        draft_content = _run_single_agent_crew(writer, write_task)
        Path(paths["draft"]).write_text(draft_content, encoding="utf-8")
        results["stages"]["write"] = "completed"
        print(f"[Pipeline] Draft written → {paths['draft']}")
    except Exception as e:
        results["stages"]["write"] = f"failed: {e}"
        results["final_status"] = "failed_at_write"
        results["error"] = str(e)
        return results

    # ── STAGE 3: FACT-CHECK ──────────────────────────────────────────────────
    print(f"\n[Pipeline] Stage 3/4: Fact-Checker Agent starting...")
    try:
        fact_checker = build_fact_checker_agent()
        fact_check_task = build_fact_check_task(
            fact_checker=fact_checker,
            draft_content=draft_content,
            research_content=research_content,
            topic_id=topic_id,
            output_path=paths["fact_check"],
        )
        fact_check_content = _run_single_agent_crew(fact_checker, fact_check_task)
        Path(paths["fact_check"]).write_text(fact_check_content, encoding="utf-8")
        results["stages"]["fact_check"] = "completed"
        print(f"[Pipeline] Fact-check done → {paths['fact_check']}")

        # Gate 2: if fact-check clearly failed, stop here
        if "**Overall Result:** FAIL" in fact_check_content or "**Overall Result:** ESCALATE" in fact_check_content:
            results["final_status"] = "blocked_at_fact_check"
            results["error"] = "Fact-check FAILED or requires ESCALATION. See fact-check report."
            print(f"[Pipeline] ⚠️  Fact-check failed — pipeline stopped. Review: {paths['fact_check']}")
            return results

    except Exception as e:
        results["stages"]["fact_check"] = f"failed: {e}"
        results["final_status"] = "failed_at_fact_check"
        results["error"] = str(e)
        return results

    # ── STAGE 4: STYLE CHECK ─────────────────────────────────────────────────
    print(f"\n[Pipeline] Stage 4/4: Style Checker Agent starting...")
    try:
        style_checker = build_style_checker_agent()
        style_check_task = build_style_check_task(
            style_checker=style_checker,
            draft_content=draft_content,
            fact_check_result=fact_check_content,
            topic_id=topic_id,
            output_path=paths["style_check"],
        )
        style_check_content = _run_single_agent_crew(style_checker, style_check_task)
        Path(paths["style_check"]).write_text(style_check_content, encoding="utf-8")
        results["stages"]["style_check"] = "completed"
        print(f"[Pipeline] Style-check done → {paths['style_check']}")

        # Gate 3: determine final status from style check result
        if "**Overall Result:** FAIL" in style_check_content:
            results["final_status"] = "blocked_at_style_check"
            results["error"] = "Style check FAILED. Draft needs revision. See style report."
            return results
        # PASS or MARGINAL → continue to visual

    except Exception as e:
        results["stages"]["style_check"] = f"failed: {e}"
        results["final_status"] = "failed_at_style_check"
        results["error"] = str(e)
        return results

    # ── STAGE 5: VISUAL DESIGNER ─────────────────────────────────────────────
    import time; time.sleep(8)  # brief pause — avoid Gemini rate limit after 4 prior calls
    print(f"\n[Pipeline] Stage 5/5: Visual Designer Agent starting...")

    # Extract the approved Instagram caption from the style-check report
    approved_caption = _extract_approved_caption(style_check_content)

    try:
        gen = generate_visual(
            approved_draft=approved_caption,
            research_content=research_content,
            topic_id=topic_id,
            output_path_ig=paths["visual_ig"],
        )

        gate4 = validate_visual_output(paths["visual_ig"])
        if gate4["passed"]:
            results["stages"]["visual"] = "completed"
            results["final_status"] = "ready_for_human_review"
            print(f"[Pipeline] Visual done → {paths['visual_ig']} ({gate4['size_kb']:.0f}KB, {gate4['dimensions']})")
        else:
            results["stages"]["visual"] = f"gate4_failed: {gate4['failures']}"
            results["final_status"] = "blocked_at_gate4"
            results["error"] = f"Gate 4 failed: {gate4['failures']}"
            print(f"[Pipeline] Gate 4 failed: {gate4['failures']}")

    except Exception as e:
        results["stages"]["visual"] = f"failed: {e}"
        results["final_status"] = "failed_at_visual"
        results["error"] = str(e)

    return results


def _extract_approved_caption(style_check_content: str) -> str:
    """Pull the Final Approved Draft (Instagram) section from the style-check report."""
    match = re.search(
        r"## Final Approved Draft \(Instagram Caption\)\s*\n(.*?)(?=\n---|\n## |\Z)",
        style_check_content,
        re.DOTALL,
    )
    if match:
        return match.group(1).strip()
    # Fallback: return the whole style check content and let agent parse it
    return style_check_content
