#!/usr/bin/env python3
"""
Full Pipeline CLI
Runs all 5 agents in sequence: Research → Write → Fact-Check → Style-Check → Visual Designer

Usage:
    # Full pipeline on a new topic:
    python scripts/run_pipeline.py --topic-id T001 --topic-en "Education Spending" \
        --topic-bn "শিক্ষা খরচ তুলনা" --context "Compare 1996-2024..."

    # Skip research, use an existing research file:
    python scripts/run_pipeline.py --topic-id T001 --topic-en "Education Spending" \
        --topic-bn "শিক্ষা খরচ তুলনা" \
        --research-file pipeline-data/research/T001_research_20260223_123609.md

Output files are saved to:
    pipeline-data/research/{topic_id}_research_{ts}.md
    pipeline-data/content/{topic_id}_draft_{ts}.md
    pipeline-data/reports/{topic_id}_factcheck_{ts}.md
    pipeline-data/reports/{topic_id}_stylecheck_{ts}.md
    pipeline-data/visuals/{topic_id}_ig_{ts}.png
"""
import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

repo_root = Path(__file__).parent.parent
load_dotenv(repo_root / ".env")
sys.path.insert(0, str(repo_root))

console = Console()


def parse_args():
    parser = argparse.ArgumentParser(description="Run the full Bangladesh Data content pipeline")
    parser.add_argument("--topic-id",  default="T001", help="Topic ID, e.g. T001")
    parser.add_argument("--topic-en",  default="Education Spending Comparison", help="Topic in English")
    parser.add_argument("--topic-bn",  default="শিক্ষা খরচ তুলনা", help="Topic in Bangla")
    parser.add_argument("--context",
        default="Compare Bangladesh education budget as percentage of GDP across government periods (1991-2024). Include primary enrollment rates. Use BBS, UNESCO, and World Bank.",
        help="Context notes for the researcher")
    parser.add_argument("--research-file", default=None,
        help="Path to an existing research .md file — skips the research stage")
    return parser.parse_args()


def check_env():
    has_gemini = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    has_claude = bool(os.getenv("ANTHROPIC_API_KEY"))
    primary = os.getenv("PRIMARY_MODEL", "")

    if primary.startswith("gemini/") and not has_gemini:
        console.print(Panel("[red]GEMINI_API_KEY not set but PRIMARY_MODEL is Gemini.[/red]", title="Config Error"))
        sys.exit(1)
    if not primary.startswith("gemini/") and not has_claude:
        console.print(Panel("[red]ANTHROPIC_API_KEY not set.[/red]", title="Config Error"))
        sys.exit(1)


def print_summary(results: dict):
    status = results["final_status"]
    color = "green" if status == "ready_for_human_review" else "red"

    console.print()
    console.print(Panel(
        f"[bold {color}]Pipeline Status: {status.upper().replace('_', ' ')}[/bold {color}]",
        title="Pipeline Complete"
    ))

    # Stage results table
    table = Table(title="Stage Results", box=box.SIMPLE)
    table.add_column("Stage", style="cyan")
    table.add_column("Status")
    table.add_column("Output File")

    stage_map = {
        "research":    ("1. Research",     results["paths"].get("research", "")),
        "write":       ("2. Write",        results["paths"].get("draft", "")),
        "fact_check":  ("3. Fact-Check",   results["paths"].get("fact_check", "")),
        "style_check": ("4. Style-Check",  results["paths"].get("style_check", "")),
        "visual":      ("5. Visual",       results["paths"].get("visual_ig", "")),
    }

    for key, (label, path) in stage_map.items():
        stage_status = results["stages"].get(key, "not reached")
        color = "green" if stage_status in ("completed", "skipped (existing file used)") else "red"
        table.add_row(label, f"[{color}]{stage_status}[/{color}]", Path(path).name if path else "—")

    console.print(table)

    if status == "ready_for_human_review":
        visual_path = results["paths"].get("visual_ig", "")
        console.print(Panel(
            "[green]Content is ready for your review![/green]\n\n"
            f"Approved caption (text):\n[bold]{results['paths']['style_check']}[/bold]\n\n"
            f"Visual (PNG):\n[bold]{visual_path}[/bold]\n\n"
            "Review both files, then approve or reject.",
            title="[green]Next Step[/green]"
        ))
    elif results.get("error"):
        console.print(Panel(
            f"[red]Pipeline stopped:[/red] {results['error']}",
            title="[red]Error[/red]"
        ))


def main():
    args = parse_args()
    check_env()

    console.print(Panel(
        "[bold green]Bangladesh Data Content Pipeline[/bold green]\n"
        "Research → Write → Fact-Check → Style-Check → Visual Designer",
        title="Starting Full Pipeline"
    ))

    info = Table(show_header=False, box=None, padding=(0, 2))
    info.add_row("[cyan]Topic ID[/cyan]",    args.topic_id)
    info.add_row("[cyan]English[/cyan]",     args.topic_en)
    info.add_row("[cyan]Bangla[/cyan]",      args.topic_bn)
    info.add_row("[cyan]Model[/cyan]",       os.getenv("PRIMARY_MODEL", "not set"))
    if args.research_file:
        info.add_row("[cyan]Research file[/cyan]", args.research_file)
    console.print(info)
    console.print()

    from agents.crew import run_full_pipeline

    results = run_full_pipeline(
        topic_id=args.topic_id,
        topic_english=args.topic_en,
        topic_bangla=args.topic_bn,
        context_notes=args.context,
        existing_research_path=args.research_file,
    )

    print_summary(results)

    if results["final_status"] != "ready_for_human_review":
        sys.exit(1)


if __name__ == "__main__":
    main()
