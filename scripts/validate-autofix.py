"""
validate-autofix.py — CoDev routing validation with auto-fix and reporting.

Detects and optionally fixes three error classes:
  1. Missing alias  — capability in capabilities.yaml has no entry in aliases.yaml
  2. Invalid agent  — agent name in matrix.yaml does not match any .agent.md file
  3. Orphaned prompt — prompt referenced in matrix.yaml has no matching .prompt.md file

Usage:
  python scripts/validate-autofix.py               # detect only
  python scripts/validate-autofix.py --fix          # detect + fix in place
  python scripts/validate-autofix.py --report       # detect + write Markdown report
  python scripts/validate-autofix.py --report --report-format json   # JSON report
  python scripts/validate-autofix.py --fix --report # fix + report
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ROUTING_DIR = ROOT / "routing"
AGENTS_DIR = ROOT / ".github" / "agents"
PROMPTS_DIR = ROOT / ".github" / "prompts"

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def dump_yaml(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        yaml.dump(data, fh, allow_unicode=True, sort_keys=False, default_flow_style=False)


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1))
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        return {}


def collect_agent_names() -> set[str]:
    """Return the set of all valid agent display names from .agent.md files."""
    names: set[str] = set()
    for path in AGENTS_DIR.glob("*.agent.md"):
        fm = parse_frontmatter(path)
        name = fm.get("name")
        if isinstance(name, str) and name.strip():
            names.add(name.strip())
    return names


def collect_prompt_ids() -> set[str]:
    """Return the set of all valid prompt IDs (stem without .prompt.md)."""
    return {p.name.removesuffix(".prompt.md") for p in PROMPTS_DIR.glob("*.prompt.md")}


def closest_match(value: str, candidates: set[str], n: int = 1) -> list[str]:
    """Return up to n closest matches for value in candidates."""
    return difflib.get_close_matches(value, candidates, n=n, cutoff=0.4)


# ---------------------------------------------------------------------------
# Issue dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Issue:
    error_class: str          # "missing-alias" | "invalid-agent" | "orphaned-prompt"
    location: str             # human-readable location
    detail: str               # description
    auto_fixable: bool = True
    fixed: bool = False
    suggestion: str = ""


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------


def detect_missing_aliases(
    capabilities: list[dict[str, Any]],
    aliases: dict[str, Any],
) -> list[Issue]:
    issues: list[Issue] = []
    alias_keys = set((aliases or {}).keys())
    for cap in capabilities:
        cap_id = cap.get("id", "")
        if cap_id and cap_id not in alias_keys:
            issues.append(
                Issue(
                    error_class="missing-alias",
                    location=f"routing/aliases.yaml → capability '{cap_id}'",
                    detail=(
                        f"Capability '{cap_id}' exists in capabilities.yaml "
                        "but has no entry in aliases.yaml."
                    ),
                    suggestion=f"Add an aliases entry for '{cap_id}'.",
                )
            )
    return issues


def detect_invalid_agents(
    routing_rules: list[dict[str, Any]],
    valid_agents: set[str],
) -> list[Issue]:
    issues: list[Issue] = []
    for idx, rule in enumerate(routing_rules, start=1):
        agent = rule.get("suggest", {}).get("agent")
        if agent and agent not in valid_agents:
            closest = closest_match(agent, valid_agents)
            suggestion = f"Did you mean '{closest[0]}'?" if closest else "No close match found."
            issues.append(
                Issue(
                    error_class="invalid-agent",
                    location=f"routing/matrix.yaml → rule #{idx} (when={rule.get('when')})",
                    detail=f"Agent '{agent}' does not match any .agent.md file.",
                    suggestion=suggestion,
                    auto_fixable=bool(closest),
                )
            )
    return issues


def detect_orphaned_prompts(
    routing_rules: list[dict[str, Any]],
    valid_prompts: set[str],
) -> list[Issue]:
    issues: list[Issue] = []
    for idx, rule in enumerate(routing_rules, start=1):
        prompts = rule.get("suggest", {}).get("prompts", []) or []
        for prompt in prompts:
            if prompt not in valid_prompts:
                issues.append(
                    Issue(
                        error_class="orphaned-prompt",
                        location=(
                            f"routing/matrix.yaml → rule #{idx} "
                            f"(when={rule.get('when')}), prompt='{prompt}'"
                        ),
                        detail=(
                            f"Prompt '{prompt}' is referenced but has no "
                            "matching .prompt.md file."
                        ),
                        suggestion=f"Remove '{prompt}' or create .github/prompts/{prompt}.prompt.md",
                    )
                )
    return issues


# ---------------------------------------------------------------------------
# Auto-fix
# ---------------------------------------------------------------------------


def fix_missing_aliases(
    issues: list[Issue],
    aliases_path: Path,
    aliases_doc: dict[str, Any],
) -> int:
    """Add stub alias entries for missing capabilities. Returns number of fixes applied."""
    applied = 0
    aliases: dict[str, Any] = aliases_doc.setdefault("aliases", {})

    for issue in issues:
        if issue.error_class != "missing-alias" or issue.fixed:
            continue
        # Extract capability id from detail
        match = re.search(r"Capability '([^']+)'", issue.detail)
        if not match:
            continue
        cap_id = match.group(1)
        if cap_id not in aliases:
            aliases[cap_id] = [cap_id]
            issue.fixed = True
            applied += 1

    if applied:
        dump_yaml(aliases_path, aliases_doc)

    return applied


def fix_invalid_agents(
    issues: list[Issue],
    matrix_path: Path,
    matrix_doc: dict[str, Any],
    valid_agents: set[str],
) -> int:
    """Replace invalid agent names with closest match. Returns number of fixes applied."""
    applied = 0
    routing_rules: list[dict[str, Any]] = matrix_doc.get("routing_rules", [])

    for issue in issues:
        if issue.error_class != "invalid-agent" or issue.fixed or not issue.auto_fixable:
            continue
        # Extract agent name from detail
        match = re.search(r"Agent '([^']+)'", issue.detail)
        if not match:
            continue
        bad_agent = match.group(1)
        closest = closest_match(bad_agent, valid_agents)
        if not closest:
            continue
        replacement = closest[0]
        for rule in routing_rules:
            suggest = rule.get("suggest", {})
            if suggest.get("agent") == bad_agent:
                suggest["agent"] = replacement
                issue.fixed = True
                applied += 1

    if applied:
        dump_yaml(matrix_path, matrix_doc)

    return applied


def fix_orphaned_prompts(
    issues: list[Issue],
    matrix_path: Path,
    matrix_doc: dict[str, Any],
) -> int:
    """Remove orphaned prompt references. Returns number of fixes applied."""
    applied = 0
    routing_rules: list[dict[str, Any]] = matrix_doc.get("routing_rules", [])

    orphaned: set[str] = set()
    for issue in issues:
        if issue.error_class == "orphaned-prompt" and not issue.fixed:
            m = re.search(r"prompt='([^']+)'", issue.location)
            if m:
                orphaned.add(m.group(1))

    if not orphaned:
        return 0

    for rule in routing_rules:
        suggest = rule.get("suggest", {})
        prompts = suggest.get("prompts")
        if prompts is None:
            continue
        before = list(prompts)
        suggest["prompts"] = [p for p in prompts if p not in orphaned]
        if suggest["prompts"] != before:
            applied += len(before) - len(suggest["prompts"])

    if applied:
        dump_yaml(matrix_path, matrix_doc)
        for issue in issues:
            if issue.error_class == "orphaned-prompt":
                issue.fixed = True

    return applied


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def render_markdown_report(
    issues: list[Issue],
    total_fixed: int,
    fix_mode: bool,
) -> str:
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total = len(issues)
    fixable = sum(1 for i in issues if i.auto_fixable)
    unfixable = total - fixable

    lines: list[str] = [
        "# CoDev Validation Auto-Fix Report",
        "",
        f"**Generated**: {now}",
        f"**Mode**: {'fix + detect' if fix_mode else 'detect only'}",
        f"**Total issues**: {total}",
        f"**Auto-fixable**: {fixable}",
        f"**Not auto-fixable**: {unfixable}",
        f"**Fixed this run**: {total_fixed}",
        "",
    ]

    for cls, label in [
        ("missing-alias", "Missing Aliases"),
        ("invalid-agent", "Invalid Agent Names"),
        ("orphaned-prompt", "Orphaned Prompt References"),
    ]:
        subset = [i for i in issues if i.error_class == cls]
        if not subset:
            continue
        lines += [f"## {label}", ""]
        lines += ["| Location | Detail | Fixable | Fixed | Suggestion |"]
        lines += ["| --- | --- | --- | --- | --- |"]
        for iss in subset:
            fixable_cell = "✅" if iss.auto_fixable else "❌"
            fixed_cell = "✅" if iss.fixed else ("⏳" if fix_mode else "—")
            lines.append(
                f"| {iss.location} | {iss.detail} | {fixable_cell} | {fixed_cell} | {iss.suggestion} |"
            )
        lines.append("")

    if not issues:
        lines += ["## Result", "", "✅ No issues found. All checks passed."]

    return "\n".join(lines)


def render_json_report(
    issues: list[Issue],
    total_fixed: int,
    fix_mode: bool,
) -> str:
    now = datetime.now(tz=timezone.utc).isoformat()
    payload = {
        "generated_at": now,
        "mode": "fix" if fix_mode else "detect",
        "summary": {
            "total": len(issues),
            "auto_fixable": sum(1 for i in issues if i.auto_fixable),
            "fixed": total_fixed,
        },
        "issues": [
            {
                "error_class": i.error_class,
                "location": i.location,
                "detail": i.detail,
                "auto_fixable": i.auto_fixable,
                "fixed": i.fixed,
                "suggestion": i.suggestion,
            }
            for i in issues
        ],
    }
    return json.dumps(payload, indent=2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    # Ensure UTF-8 output on Windows terminals
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Detect (and optionally fix) common CoDev routing errors.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply auto-fixes in place (modifies YAML files).",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Write a validation report to the reports/ directory.",
    )
    parser.add_argument(
        "--report-format",
        choices=["markdown", "json"],
        default="markdown",
        help="Report format (default: markdown).",
    )
    args = parser.parse_args(argv)

    # Load routing data
    capabilities_doc = load_yaml(ROUTING_DIR / "capabilities.yaml")
    aliases_path = ROUTING_DIR / "aliases.yaml"
    matrix_path = ROUTING_DIR / "matrix.yaml"
    aliases_doc = load_yaml(aliases_path)
    matrix_doc = load_yaml(matrix_path)

    capabilities: list[dict[str, Any]] = capabilities_doc.get("capabilities", [])
    aliases: dict[str, Any] = aliases_doc.get("aliases", {})
    routing_rules: list[dict[str, Any]] = matrix_doc.get("routing_rules", [])

    valid_agents = collect_agent_names()
    valid_prompts = collect_prompt_ids()

    # Detect
    issues: list[Issue] = []
    issues += detect_missing_aliases(capabilities, aliases)
    issues += detect_invalid_agents(routing_rules, valid_agents)
    issues += detect_orphaned_prompts(routing_rules, valid_prompts)

    total_fixed = 0

    # Fix
    if args.fix:
        # Reload docs fresh for fix phase (avoid stale refs)
        aliases_doc_fix = load_yaml(aliases_path)
        matrix_doc_fix = load_yaml(matrix_path)
        total_fixed += fix_missing_aliases(issues, aliases_path, aliases_doc_fix)
        total_fixed += fix_invalid_agents(issues, matrix_path, matrix_doc_fix, valid_agents)
        total_fixed += fix_orphaned_prompts(issues, matrix_path, matrix_doc_fix)

    # Report
    if args.report:
        reports_dir = ROOT / "reports"
        reports_dir.mkdir(exist_ok=True)
        ts = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        if args.report_format == "json":
            content = render_json_report(issues, total_fixed, args.fix)
            out_path = reports_dir / f"autofix-{ts}.json"
        else:
            content = render_markdown_report(issues, total_fixed, args.fix)
            out_path = reports_dir / f"autofix-{ts}.md"
        out_path.write_text(content, encoding="utf-8")
        print(f"Report written: {out_path.relative_to(ROOT)}")

    # Console summary
    total = len(issues)
    if total == 0:
        print("✅ validate-autofix: no issues found.")
        return 0

    unfixed = [i for i in issues if not i.fixed]
    print(f"{'✅' if not unfixed else '❌'} validate-autofix: {total} issue(s) found, {total_fixed} fixed.")
    for issue in issues:
        status = "[FIXED]" if issue.fixed else ("[AUTO-FIX AVAILABLE]" if issue.auto_fixable else "[MANUAL FIX REQUIRED]")
        print(f"  {status} [{issue.error_class}] {issue.location}")
        print(f"    → {issue.detail}")
        if not issue.fixed and issue.suggestion:
            print(f"    💡 {issue.suggestion}")

    return 0 if not unfixed else 1


if __name__ == "__main__":
    sys.exit(main())
