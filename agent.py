#!/usr/bin/env python3
"""
AI Maturity Research Agent

Runs each morning to surface companies with genuine AI depth — Databricks
customers and builder-mentality organizations actively engineering AI, not
just deploying off-the-shelf tools like Copilot.

Usage:
    python agent.py                  # run and save report to reports/
    python agent.py --print-only     # run and print, don't save

Scheduling (cron):
    0 7 * * 1-5 cd /path/to/repo && python agent.py >> logs/agent.log 2>&1
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import anthropic


# ---------------------------------------------------------------------------
# Scoring rubric and search strategy embedded in the system prompt so Claude
# has a consistent frame across all web_search + web_fetch calls.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a senior enterprise technology analyst specializing in AI/ML adoption intelligence for a Databricks sales team.

Your mission: identify companies that demonstrate GENUINE AI maturity — organizations actively building, engineering, and deeply integrating AI into their stack. These are the companies worth a conversation.

## HIGH VALUE signals (hunt for these):

**Databricks ecosystem**
- Companies publishing technical content that references Databricks, Delta Lake, Unity Catalog, MLflow, or Apache Spark in a hands-on context (not just "we use Databricks")
- Customers sharing architecture diagrams, benchmark results, or migration stories involving the lakehouse stack
- Partners or ISVs building on top of the Databricks platform

**Builder mentality**
- Technical engineering blogs describing custom ML infrastructure, LLMOps pipelines, feature stores, or model serving platforms they built
- Companies that have open-sourced AI tooling or contributed to projects like Ray, MLflow, Delta, Hugging Face
- "We built X" > "We deployed X" — builders vs. buyers
- Hiring patterns: ML platform engineers, AI infra, data platform, GPU cluster teams

**Custom AI development**
- Fine-tuning or pre-training their own models
- Production RAG pipelines described with architectural depth
- AI-native products where the ML stack is a core differentiator
- Publishing research or attending technical AI conferences as speakers

## LOW VALUE signals (skip these, don't report them):

- "We've deployed Microsoft Copilot to all employees"
- "We're rolling out ChatGPT/Gemini internally"
- "Our AI strategy focuses on [buzzwords with no engineering specifics]"
- Generic press releases drafted by PR agencies
- SaaS vendors passively adding AI features (Salesforce Einstein, HubSpot AI, etc.)
- Analyst and consultant opinion pieces about AI trends
- "We're exploring AI opportunities" — no timeline, no engineers mentioned

## AI Maturity Score (1–10):
- 9–10: Building custom models or deep ML infrastructure; publishing research; engineering-driven content with real depth
- 7–8: Active ML/AI development, clear technical substance, Databricks/MLflow power users
- 5–6: Real implementation with some customization — beyond off-the-shelf
- 1–4: Generic adoption, copilot deployments, no technical depth → **EXCLUDE from report**

Only include companies scoring 7 or higher."""


def build_search_queries() -> list[str]:
    """Generate time-bounded queries across the key signal dimensions."""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    return [
        # Databricks ecosystem signals
        f'Databricks customer "data platform" OR "ML platform" technical blog after:{yesterday}',
        f'"Delta Lake" OR "Unity Catalog" OR "MLflow" engineering case study after:{yesterday}',
        f'"Apache Spark" production ML platform engineering announcement after:{yesterday}',

        # Builder mentality
        f'company "built" "AI platform" OR "ML platform" OR "data platform" engineering after:{yesterday}',
        f'"LLMOps" OR "MLOps" OR "feature store" production platform announcement after:{yesterday}',
        f'"RAG" OR "retrieval augmented generation" production engineering blog after:{yesterday}',
        f'"fine-tuning" OR "fine-tuned" LLM enterprise production after:{yesterday}',

        # Infrastructure depth
        f'"ML infrastructure" OR "AI infrastructure" engineering blog launch after:{yesterday}',
        f'"data lakehouse" OR lakehouse platform engineering announcement after:{yesterday}',

        # Conference and research signals
        f'"Data+AI Summit" OR "Ray Summit" speaker OR presentation after:{yesterday}',
        f'company "open source" AI OR ML tooling release GitHub after:{yesterday}',
    ]


def load_seen_companies(path: Path) -> set[str]:
    """Load previously reported companies to avoid re-surfacing them."""
    if path.exists():
        try:
            data = json.loads(path.read_text())
            return set(data.get("companies", []))
        except (json.JSONDecodeError, KeyError):
            pass
    return set()


def save_seen_companies(path: Path, companies: set[str]) -> None:
    """Persist the set of reported companies."""
    path.write_text(json.dumps({"companies": sorted(companies)}, indent=2))


def run_agent() -> str:
    """Run the research agent and return the formatted report text."""
    client = anthropic.Anthropic()

    today = datetime.now().strftime("%A, %B %d, %Y")
    queries = build_search_queries()
    queries_text = "\n".join(f"{i + 1}. {q}" for i, q in enumerate(queries))

    messages: list[dict] = [
        {
            "role": "user",
            "content": f"""Today is {today}.

Run a targeted research sweep to find companies demonstrating genuine AI maturity — content published in the last 24–48 hours.

**Search angles to work through:**
{queries_text}

**Instructions:**
- For each promising snippet, fetch the actual page to verify depth. Don't judge from the headline alone.
- Be ruthless with the filter: if it's a Copilot rollout or a generic "AI strategy" PR, skip it.
- When you confirm a strong signal, note the exact evidence (quote or specific feature described).

**Output format — produce exactly this structure:**

# AI Maturity Daily Brief — {today}

## Overview
[2–3 sentences on today's landscape: any themes, volume of signal, quality]

## Top Findings

[Repeat this block for each qualifying company, score 7+:]

### [Company Name] — [Score]/10
**Industry**: [sector]
**Signal**: [1–2 sentences on what caught your eye — be specific]
**Databricks / Builder connection**: [direct evidence, or "Not confirmed"]
**Source**: [URL]
**Why engage**: [one-sentence talking point for an outbound touch]

---

## Patterns & Themes
[2–3 sentences on recurring themes across today's findings — useful for BDR messaging]

Aim for 5–10 companies. Fewer is fine if the bar is genuinely high today.""",
        }
    ]

    # Agentic loop — re-sends on pause_turn so long tool chains can complete
    max_continuations = 5
    continuations = 0

    while continuations <= max_continuations:
        with client.messages.stream(
            model="claude-opus-4-7",
            max_tokens=8000,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            tools=[
                {"type": "web_search_20260209", "name": "web_search"},
                {"type": "web_fetch_20260209", "name": "web_fetch"},
            ],
            messages=messages,
        ) as stream:
            response = stream.get_final_message()

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "pause_turn":
            # Server-side tool loop hit its iteration cap; continue
            continuations += 1
            messages.append({
                "role": "user",
                "content": "Continue your research and complete the report.",
            })
        else:
            break

    # Collect all text blocks from the final assistant turn
    final_content = messages[-1]["content"]
    text_parts = [
        block.text
        for block in final_content
        if hasattr(block, "type") and block.type == "text"
    ]
    return "\n".join(text_parts)


def save_report(report: str) -> Path:
    """Write the report to a dated markdown file under reports/."""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d")
    output_path = reports_dir / f"ai_maturity_{timestamp}.md"
    output_path.write_text(report, encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Maturity Research Agent")
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Print report to stdout without saving",
    )
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] Starting AI Maturity Research Agent...", file=sys.stderr)

    report = run_agent()

    if args.print_only:
        print(report)
    else:
        output_path = save_report(report)
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] Report saved → {output_path}", file=sys.stderr)
        print(report)


if __name__ == "__main__":
    main()
