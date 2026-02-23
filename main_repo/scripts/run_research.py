#!/usr/bin/env python3
"""
Research Pipeline CLI
Run the Research Agent from the command line to test it on any topic.

Usage:
    python scripts/run_research.py
    python scripts/run_research.py --topic-id T001 --topic-en "Education Spending" \
        --topic-bn "শিক্ষা খরচ" --context "Compare 1996-2001 vs 2009-2024"

The output is saved to pipeline-data/research/{topic_id}_research_{timestamp}.md
"""
import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Load .env from repo root or main_repo
repo_root = Path(__file__).parent.parent
load_dotenv(repo_root / ".env")

# Add main_repo to path so imports work
sys.path.insert(0, str(repo_root))

console = Console()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Bangladesh Data Research Agent on a topic"
    )
    parser.add_argument(
        "--topic-id", default="T001",
        help="Topic ID (e.g. T001). Default: T001"
    )
    parser.add_argument(
        "--topic-en", default="Education Spending Comparison",
        help="Topic in English"
    )
    parser.add_argument(
        "--topic-bn", default="শিক্ষা খরচ তুলনা",
        help="Topic in Bangla (Bengali script)"
    )
    parser.add_argument(
        "--context",
        default="Compare education budget as percentage of GDP across different government periods (1991-2024). Focus on primary and secondary education enrollment rates. Use UNESCO and BBS as primary sources.",
        help="Context notes for the researcher (what to focus on, which periods, etc.)"
    )
    return parser.parse_args()


def check_env():
    """Verify required environment variables are set."""
    missing = []
    if not os.getenv("ANTHROPIC_API_KEY"):
        missing.append("ANTHROPIC_API_KEY")

    if missing:
        console.print(
            Panel(
                f"[red]Missing required environment variables:[/red]\n"
                + "\n".join(f"  • {k}" for k in missing)
                + "\n\n[yellow]Create a .env file from .env.example and fill in your API keys.[/yellow]",
                title="[red]Configuration Error[/red]",
            )
        )
        sys.exit(1)


def main():
    args = parse_args()
    check_env()

    console.print(Panel(
        "[bold green]Bangladesh Data Research Agent[/bold green]\n"
        "Researching topic from trusted Bangladesh data sources...",
        title="Starting Research Pipeline"
    ))

    # Show what we're researching
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row("[cyan]Topic ID[/cyan]",       args.topic_id)
    table.add_row("[cyan]Topic (English)[/cyan]", args.topic_en)
    table.add_row("[cyan]Topic (Bangla)[/cyan]",  args.topic_bn)
    table.add_row("[cyan]Context Notes[/cyan]",   args.context[:100] + "..." if len(args.context) > 100 else args.context)
    table.add_row("[cyan]Model[/cyan]",            os.getenv("PRIMARY_MODEL", "claude-sonnet-4-6"))
    console.print(table)
    console.print()

    # Run the research crew
    from agents.crew import run_research_crew

    result = run_research_crew(
        topic_id=args.topic_id,
        topic_english=args.topic_en,
        topic_bangla=args.topic_bn,
        context_notes=args.context,
    )

    # Show result
    if result["status"] == "success":
        console.print(Panel(
            f"[green]Research completed successfully![/green]\n\n"
            f"Output file: [bold]{result['output_path']}[/bold]",
            title="[green]Success[/green]"
        ))
    else:
        console.print(Panel(
            f"[red]Research failed.[/red]\n\n"
            f"Error: {result['error']}\n\n"
            f"Partial output (if any): {result['output_path']}",
            title="[red]Error[/red]"
        ))
        sys.exit(1)


if __name__ == "__main__":
    main()
