"""
Benchmark CoDev against similar GitHub projects.

Features:
- Project discovery via gh CLI (API mode) or manual input file (offline mode)
- Deterministic top-N project selection
- Optional shallow cloning into a local external directory
- Weighted scoring rubric (0-100)
- Markdown and JSON report emission

This script is reusable and deterministic when the same input data is provided.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from typing import Any

DEFAULT_TOP_COUNT = 10
DEFAULT_CLONE_DIR = "external"
DEFAULT_MARKDOWN_OUTPUT = "reports/benchmark-similar-projects.md"
DEFAULT_JSON_OUTPUT = "reports/benchmark-similar-projects.json"

# Weight sum must stay at 100.
DEFAULT_RUBRIC_WEIGHTS: dict[str, int] = {
    "community": 20,
    "maintenance": 15,
    "documentation": 15,
    "architecture": 15,
    "quality_gates": 15,
    "extensibility": 10,
    "testing": 10,
}

BASELINE_PROJECTS: list[dict[str, Any]] = [
    {
        "full_name": "microsoft/vscode-copilot-release",
        "clone_url": "https://github.com/microsoft/vscode-copilot-release.git",
        "html_url": "https://github.com/microsoft/vscode-copilot-release",
        "description": "Official Copilot issue and release tracking repository.",
        "stargazers_count": 2100,
        "pushed_at": "2026-05-01T12:00:00Z",
        "language": "Markdown",
        "signals": {
            "community": 8,
            "maintenance": 8,
            "documentation": 8,
            "architecture": 7,
            "quality_gates": 6,
            "extensibility": 6,
            "testing": 5,
        },
    },
    {
        "full_name": "github/awesome-copilot",
        "clone_url": "https://github.com/github/awesome-copilot.git",
        "html_url": "https://github.com/github/awesome-copilot",
        "description": "Curated Copilot resources and examples.",
        "stargazers_count": 3900,
        "pushed_at": "2026-04-20T08:00:00Z",
        "language": "Markdown",
        "signals": {
            "community": 9,
            "maintenance": 7,
            "documentation": 9,
            "architecture": 6,
            "quality_gates": 5,
            "extensibility": 7,
            "testing": 4,
        },
    },
    {
        "full_name": "continuedev/continue",
        "clone_url": "https://github.com/continuedev/continue.git",
        "html_url": "https://github.com/continuedev/continue",
        "description": "Open-source AI coding assistant extension with config and tooling.",
        "stargazers_count": 22000,
        "pushed_at": "2026-05-07T11:30:00Z",
        "language": "TypeScript",
        "signals": {
            "community": 10,
            "maintenance": 9,
            "documentation": 8,
            "architecture": 8,
            "quality_gates": 8,
            "extensibility": 9,
            "testing": 8,
        },
    },
    {
        "full_name": "microsoft/promptflow",
        "clone_url": "https://github.com/microsoft/promptflow.git",
        "html_url": "https://github.com/microsoft/promptflow",
        "description": "Prompt orchestration and evaluation framework.",
        "stargazers_count": 21000,
        "pushed_at": "2026-05-05T09:45:00Z",
        "language": "Python",
        "signals": {
            "community": 10,
            "maintenance": 8,
            "documentation": 8,
            "architecture": 8,
            "quality_gates": 8,
            "extensibility": 8,
            "testing": 8,
        },
    },
    {
        "full_name": "All-Hands-AI/OpenHands",
        "clone_url": "https://github.com/All-Hands-AI/OpenHands.git",
        "html_url": "https://github.com/All-Hands-AI/OpenHands",
        "description": "Agentic software engineering platform.",
        "stargazers_count": 41000,
        "pushed_at": "2026-05-08T10:15:00Z",
        "language": "Python",
        "signals": {
            "community": 10,
            "maintenance": 8,
            "documentation": 7,
            "architecture": 8,
            "quality_gates": 7,
            "extensibility": 8,
            "testing": 7,
        },
    },
    {
        "full_name": "Aider-AI/aider",
        "clone_url": "https://github.com/Aider-AI/aider.git",
        "html_url": "https://github.com/Aider-AI/aider",
        "description": "AI pair programming in terminal with repository edits.",
        "stargazers_count": 30000,
        "pushed_at": "2026-05-06T15:00:00Z",
        "language": "Python",
        "signals": {
            "community": 10,
            "maintenance": 9,
            "documentation": 8,
            "architecture": 7,
            "quality_gates": 7,
            "extensibility": 7,
            "testing": 7,
        },
    },
    {
        "full_name": "microsoft/autogen",
        "clone_url": "https://github.com/microsoft/autogen.git",
        "html_url": "https://github.com/microsoft/autogen",
        "description": "Multi-agent orchestration framework.",
        "stargazers_count": 38000,
        "pushed_at": "2026-05-03T14:00:00Z",
        "language": "Python",
        "signals": {
            "community": 10,
            "maintenance": 8,
            "documentation": 8,
            "architecture": 9,
            "quality_gates": 7,
            "extensibility": 9,
            "testing": 7,
        },
    },
    {
        "full_name": "langchain-ai/langchain",
        "clone_url": "https://github.com/langchain-ai/langchain.git",
        "html_url": "https://github.com/langchain-ai/langchain",
        "description": "LLM application framework with broad integrations.",
        "stargazers_count": 98000,
        "pushed_at": "2026-05-08T13:30:00Z",
        "language": "Python",
        "signals": {
            "community": 10,
            "maintenance": 8,
            "documentation": 8,
            "architecture": 8,
            "quality_gates": 7,
            "extensibility": 10,
            "testing": 7,
        },
    },
    {
        "full_name": "crewAIInc/crewAI",
        "clone_url": "https://github.com/crewAIInc/crewAI.git",
        "html_url": "https://github.com/crewAIInc/crewAI",
        "description": "Role-based AI agent collaboration framework.",
        "stargazers_count": 32000,
        "pushed_at": "2026-05-04T16:20:00Z",
        "language": "Python",
        "signals": {
            "community": 10,
            "maintenance": 8,
            "documentation": 7,
            "architecture": 8,
            "quality_gates": 7,
            "extensibility": 8,
            "testing": 6,
        },
    },
    {
        "full_name": "agno-agi/agno",
        "clone_url": "https://github.com/agno-agi/agno.git",
        "html_url": "https://github.com/agno-agi/agno",
        "description": "Agent engineering framework for production use-cases.",
        "stargazers_count": 23000,
        "pushed_at": "2026-05-02T10:00:00Z",
        "language": "Python",
        "signals": {
            "community": 9,
            "maintenance": 7,
            "documentation": 7,
            "architecture": 8,
            "quality_gates": 6,
            "extensibility": 8,
            "testing": 6,
        },
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark CoDev against similar projects")
    parser.add_argument("--top-count", type=int, default=DEFAULT_TOP_COUNT, help="How many top projects to keep")
    parser.add_argument("--clone-dir", default=DEFAULT_CLONE_DIR, help="Directory used for shallow clones")
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN_OUTPUT, help="Markdown report path")
    parser.add_argument("--json-output", default=DEFAULT_JSON_OUTPUT, help="JSON report path")
    parser.add_argument(
        "--input-file",
        default=None,
        help="Optional manual input file (.json or .csv). If provided, no GitHub API query is required.",
    )
    parser.add_argument(
        "--mode",
        choices=("auto", "gh", "manual", "baseline"),
        default="auto",
        help="Discovery mode: auto tries input-file, then gh, then baseline fallback.",
    )
    parser.add_argument("--query", default="copilot framework prompts agents routing", help="GitHub search query for gh mode")
    parser.add_argument("--dry-run", action="store_true", help="Plan actions only, do not clone or write output files")
    parser.add_argument("--no-clone", action="store_true", help="Skip cloning projects")
    return parser.parse_args()


def parse_repo_slug(raw: str) -> tuple[str, str] | None:
    value = raw.strip()
    match = re.fullmatch(r"([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", value)
    if not match:
        return None
    return match.group(1), match.group(2)


def normalize_project(raw: dict[str, Any]) -> dict[str, Any]:
    full_name = str(raw.get("full_name") or "").strip()
    if not full_name and raw.get("owner") and raw.get("name"):
        full_name = f"{raw['owner']}/{raw['name']}"

    slug = parse_repo_slug(full_name)
    if slug is None:
        raise ValueError(f"Invalid project slug: {full_name!r}")

    owner, repo = slug
    clone_url = str(raw.get("clone_url") or f"https://github.com/{owner}/{repo}.git")
    html_url = str(raw.get("html_url") or f"https://github.com/{owner}/{repo}")

    project = {
        "full_name": f"{owner}/{repo}",
        "clone_url": clone_url,
        "html_url": html_url,
        "description": str(raw.get("description") or ""),
        "stargazers_count": int(raw.get("stargazers_count") or 0),
        "pushed_at": str(raw.get("pushed_at") or ""),
        "language": str(raw.get("language") or ""),
        "signals": dict(raw.get("signals") or {}),
    }
    return project


def load_projects_from_input_file(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError("JSON input must be an array of project objects")
        return [normalize_project(item) for item in payload]

    if path.suffix.lower() == ".csv":
        rows: list[dict[str, Any]] = []
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                rows.append(normalize_project(row))
        return rows

    raise ValueError("Input file must be .json or .csv")


def discover_projects_via_gh(query: str, limit: int) -> list[dict[str, Any]]:
    cmd = [
        "gh",
        "search",
        "repos",
        query,
        "--limit",
        str(limit),
        "--json",
        "nameWithOwner,description,stargazersCount,pushedAt,primaryLanguage,url",
    ]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "gh search repos failed")

    data = json.loads(proc.stdout)
    projects: list[dict[str, Any]] = []
    for item in data:
        full_name = item.get("nameWithOwner")
        if not full_name:
            continue
        owner, repo = full_name.split("/", 1)
        projects.append(
            normalize_project(
                {
                    "owner": owner,
                    "name": repo,
                    "description": item.get("description") or "",
                    "stargazers_count": item.get("stargazersCount") or 0,
                    "pushed_at": item.get("pushedAt") or "",
                    "language": ((item.get("primaryLanguage") or {}).get("name") or ""),
                    "html_url": item.get("url") or f"https://github.com/{full_name}",
                    "clone_url": f"https://github.com/{full_name}.git",
                }
            )
        )
    return projects


def dedupe_projects(projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_name: dict[str, dict[str, Any]] = {}
    for project in projects:
        key = project["full_name"].lower()
        current = by_name.get(key)
        if current is None or project.get("stargazers_count", 0) > current.get("stargazers_count", 0):
            by_name[key] = project
    return list(by_name.values())


def select_top_projects(projects: list[dict[str, Any]], top_count: int) -> list[dict[str, Any]]:
    deduped = dedupe_projects(projects)
    ordered = sorted(
        deduped,
        key=lambda item: (
            -int(item.get("stargazers_count", 0)),
            str(item.get("full_name", "")).lower(),
        ),
    )
    return ordered[:top_count]


def weighted_score(project: dict[str, Any], weights: dict[str, int]) -> tuple[int, dict[str, int]]:
    signals = project.get("signals") or {}
    breakdown: dict[str, int] = {}
    total = 0.0
    for criterion, weight in weights.items():
        signal_raw = signals.get(criterion, 5)
        signal_value = max(0, min(10, int(signal_raw)))
        breakdown[criterion] = signal_value
        total += (signal_value / 10.0) * float(weight)
    return int(round(total)), breakdown


def score_projects(projects: list[dict[str, Any]], weights: dict[str, int]) -> list[dict[str, Any]]:
    scored: list[dict[str, Any]] = []
    for project in projects:
        total, breakdown = weighted_score(project, weights)
        enriched = dict(project)
        enriched["score"] = total
        enriched["score_breakdown"] = breakdown
        scored.append(enriched)

    return sorted(
        scored,
        key=lambda item: (
            -int(item.get("score", 0)),
            -int(item.get("stargazers_count", 0)),
            str(item.get("full_name", "")).lower(),
        ),
    )


def clone_projects(projects: list[dict[str, Any]], clone_dir: Path, dry_run: bool) -> list[str]:
    if not dry_run:
        clone_dir.mkdir(parents=True, exist_ok=True)
    actions: list[str] = []

    for project in projects:
        slug = project["full_name"].replace("/", "__")
        dest = clone_dir / slug
        clone_url = project["clone_url"]
        if dest.exists():
            actions.append(f"skip existing {dest}")
            continue
        if dry_run:
            actions.append(f"dry-run clone --depth 1 {clone_url} -> {dest}")
            continue

        cmd = ["git", "clone", "--depth", "1", clone_url, str(dest)]
        proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
        if proc.returncode == 0:
            actions.append(f"cloned {project['full_name']}")
        else:
            actions.append(f"clone failed {project['full_name']}: {proc.stderr.strip()}")
    return actions


def build_json_report(
    *,
    mode: str,
    query: str,
    top_count: int,
    weights: dict[str, int],
    projects: list[dict[str, Any]],
    clone_actions: list[str],
) -> dict[str, Any]:
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "mode": mode,
        "query": query,
        "top_count": top_count,
        "weights": weights,
        "projects": projects,
        "clone_actions": clone_actions,
    }


def render_markdown_report(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Competitive benchmark report")
    lines.append("")
    lines.append(f"Mode: {report['mode']}")
    lines.append(f"Top count: {report['top_count']}")
    lines.append(f"Query: {report['query']}")
    lines.append("")
    lines.append("## Weighted rubric")
    lines.append("")
    lines.append("| Criterion | Weight |")
    lines.append("| --- | --- |")
    for criterion, weight in report["weights"].items():
        lines.append(f"| {criterion} | {weight} |")
    lines.append("")
    lines.append("## Ranked projects")
    lines.append("")
    lines.append("| Rank | Project | Score | Stars | Notes |")
    lines.append("| --- | --- | --- | --- | --- |")

    for idx, project in enumerate(report["projects"], start=1):
        notes = str(project.get("description") or "").replace("|", "/")
        lines.append(
            f"| {idx} | {project['full_name']} | {project['score']} | {project.get('stargazers_count', 0)} | {notes} |"
        )

    lines.append("")
    lines.append("## Clone actions")
    lines.append("")
    if report["clone_actions"]:
        for action in report["clone_actions"]:
            lines.append(f"- {action}")
    else:
        lines.append("- none")

    lines.append("")
    lines.append("## Rerun")
    lines.append("")
    lines.append(
        "python scripts/benchmark-similar-projects.py --mode baseline --dry-run --top-count 10 "
        "--markdown-output reports/benchmark-similar-projects.md "
        "--json-output reports/benchmark-similar-projects.json"
    )
    lines.append("")
    return "\n".join(lines)


def write_report_files(markdown: str, json_payload: dict[str, Any], markdown_path: Path, json_path: Path, dry_run: bool) -> None:
    if dry_run:
        return
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(json_payload, indent=2), encoding="utf-8")


def resolve_projects(
    mode: str, query: str, top_count: int, input_file: str | None
) -> tuple[str, list[dict[str, Any]], list[str]]:
    manual_projects: list[dict[str, Any]] = []
    diagnostics: list[str] = []
    if input_file:
        manual_projects = load_projects_from_input_file(Path(input_file))

    if mode == "manual":
        if not manual_projects:
            raise ValueError("manual mode requires --input-file")
        return "manual", manual_projects, diagnostics

    if mode == "baseline":
        return "baseline", [normalize_project(item) for item in BASELINE_PROJECTS], diagnostics

    if mode == "gh":
        return "gh", discover_projects_via_gh(query, limit=max(30, top_count * 3)), diagnostics

    # auto mode
    if manual_projects:
        return "manual", manual_projects, diagnostics

    try:
        discovered = discover_projects_via_gh(query, limit=max(30, top_count * 3))
        if discovered:
            return "gh", discovered, diagnostics
        diagnostics.append("auto mode fallback to baseline because gh returned zero repositories")
    except Exception as exc:
        diagnostics.append(f"auto mode fallback to baseline because gh failed: {exc}")

    return "baseline", [normalize_project(item) for item in BASELINE_PROJECTS], diagnostics


def main() -> int:
    args = parse_args()

    if args.top_count <= 0:
        raise SystemExit("--top-count must be greater than zero")

    if sum(DEFAULT_RUBRIC_WEIGHTS.values()) != 100:
        raise SystemExit("Rubric weights must sum to 100")

    resolved_mode, discovered, discovery_diagnostics = resolve_projects(args.mode, args.query, args.top_count, args.input_file)
    for diagnostic in discovery_diagnostics:
        print(f"Warning: {diagnostic}")
    selected = select_top_projects(discovered, args.top_count)
    scored = score_projects(selected, DEFAULT_RUBRIC_WEIGHTS)

    clone_actions: list[str] = []
    if not args.no_clone:
        clone_actions = clone_projects(scored, Path(args.clone_dir), args.dry_run)

    payload = build_json_report(
        mode=resolved_mode,
        query=args.query,
        top_count=args.top_count,
        weights=DEFAULT_RUBRIC_WEIGHTS,
        projects=scored,
        clone_actions=clone_actions,
    )
    markdown = render_markdown_report(payload)
    write_report_files(markdown, payload, Path(args.markdown_output), Path(args.json_output), args.dry_run)

    print(f"Discovery mode: {resolved_mode}")
    print(f"Projects discovered: {len(discovered)}")
    print(f"Projects selected: {len(selected)}")
    print(f"Top score: {scored[0]['score'] if scored else 0}")
    if args.dry_run:
        print("Dry-run enabled: no files written and no clones performed.")
    else:
        print(f"Markdown report: {args.markdown_output}")
        print(f"JSON report: {args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())