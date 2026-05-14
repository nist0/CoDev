"""
codev-dev — CoDev interactive developer CLI.

Provides fast, read-safe tooling for CoDev contributors:
    test-route  : run the routing engine on a phrase and explain the result
    guide       : preview guided contributor flows with exact next commands
    doctor      : health-check the repository (read-only, calls all validators)
    new agent   : scaffold a new agent file (dry-run by default, --write to persist)

Usage:
  python scripts/codev-dev.py test-route "debug kubernetes pod"
  python scripts/codev-dev.py guide route "debug kubernetes pod"
    python scripts/codev-dev.py guide extension --kind prompt
  python scripts/codev-dev.py guide issue --title "Add guided CLI flow" --summary "Help contributors prepare issue bodies"
  python scripts/codev-dev.py doctor
  python scripts/codev-dev.py doctor --validators smoke registry
  python scripts/codev-dev.py new agent my-specialist
  python scripts/codev-dev.py new agent my-specialist --write

Safety contract:
  - test-route and doctor are 100% read-only; they never modify any file.
  - new agent is dry-run by default; pass --write to actually create files.
  - No existing file is ever modified by this CLI.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ROUTING_DIR = ROOT / "routing"
AGENTS_DIR = ROOT / ".github" / "agents"
PROMPTS_DIR = ROOT / ".github" / "prompts"
SKILLS_DIR = ROOT / ".github" / "skills"
SCRIPTS_DIR = ROOT / "scripts"

# ANSI colours (degraded gracefully on non-TTY)
def _c(code: str, text: str) -> str:
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text

GREEN  = lambda t: _c("92", t)   # noqa: E731
RED    = lambda t: _c("91", t)   # noqa: E731
YELLOW = lambda t: _c("93", t)   # noqa: E731
CYAN   = lambda t: _c("96", t)   # noqa: E731
BOLD   = lambda t: _c("1",  t)   # noqa: E731
DIM    = lambda t: _c("2",  t)   # noqa: E731


def _ensure_utf8_stdout() -> None:
    """Best-effort UTF-8 stdout setup for Windows and wrapped streams."""
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if not callable(reconfigure):
        return
    try:
        reconfigure(encoding="utf-8")
    except (OSError, ValueError):
        return


# ---------------------------------------------------------------------------
# YAML helpers (read-only)
# ---------------------------------------------------------------------------


def _load(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _load_routing() -> dict[str, Any]:
    """Load all routing YAML files. Raises FileNotFoundError on missing files."""
    return {
        "capabilities": _load(ROUTING_DIR / "capabilities.yaml").get("capabilities", []),
        "aliases":      _load(ROUTING_DIR / "aliases.yaml").get("aliases", {}),
        "domains":      _load(ROUTING_DIR / "domains.yaml").get("domains", []),
        "rules":        _load(ROUTING_DIR / "matrix.yaml").get("routing_rules", []),
    }


# ---------------------------------------------------------------------------
# Routing engine (replicated from validate-route-smoke.py, read-only)
# ---------------------------------------------------------------------------


def detect_capability(
    request: str, aliases: dict[str, list[str]]
) -> tuple[str | None, str | None]:
    """Return (capability_id, matched_phrase) for the best alias match."""
    text = request.lower()
    best: tuple[int, str, str] | None = None
    for capability, phrases in aliases.items():
        for phrase in (phrases or []):
            p = str(phrase).lower()
            if p in text:
                score = len(p)
                if best is None or score > best[0]:
                    best = (score, capability, phrase)
    if best:
        return best[1], best[2]
    return None, None


def detect_domain(
    request: str, domains: list[dict[str, Any]]
) -> tuple[str | None, str | None]:
    """Return (domain_id, matched_keyword)."""
    text = request.lower()
    best: tuple[int, str, str] | None = None
    for domain in domains:
        domain_id = domain["id"]
        for kw in domain.get("keywords", []):
            k = str(kw).lower()
            if k in text:
                score = len(k)
                if best is None or score > best[0]:
                    best = (score, domain_id, kw)
    if best:
        return best[1], best[2]
    return None, None


def resolve_route(
    capability: str,
    domain: str | None,
    rules: list[dict[str, Any]],
    capabilities: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return the suggest block for the best matching rule."""
    for rule in rules:
        when = rule.get("when", {})
        if when.get("capability") != capability:
            continue
        required_domain = when.get("domain")
        if required_domain is not None and required_domain != domain:
            continue
        return rule.get("suggest", {})
    # Fallback: default_agent from capabilities
    for cap in capabilities:
        if cap.get("id") == capability:
            default = cap.get("default_agent")
            return {"agent": default, "prompts": [], "skills": []}
    return {}


def route(request: str, routing: dict[str, Any]) -> dict[str, Any]:
    """Run full routing pipeline. Returns a result dict (never raises)."""
    capability, matched_alias = detect_capability(request, routing["aliases"])
    domain, matched_keyword = detect_domain(request, routing["domains"])
    if capability is None:
        return {
            "ok": False,
            "request": request,
            "error": "No capability matched. Try adding aliases or rephrasing.",
        }
    suggest = resolve_route(capability, domain, routing["rules"], routing["capabilities"])
    return {
        "ok": True,
        "request": request,
        "capability": capability,
        "matched_alias": matched_alias,
        "domain": domain,
        "matched_keyword": matched_keyword,
        "agent": suggest.get("agent"),
        "prompts": suggest.get("prompts") or [],
        "skills": suggest.get("skills") or [],
    }


# ---------------------------------------------------------------------------
# command: test-route
# ---------------------------------------------------------------------------


def cmd_test_route(phrase: str, routing: dict[str, Any]) -> int:
    result = route(phrase, routing)

    print()
    print(BOLD(f"  Routing: {phrase!r}"))
    print()

    if not result["ok"]:
        print(f"  {RED('❌')} {result['error']}")
        print()
        print(f"  {DIM('Tip: run  python scripts/codev-dev.py test-route --list  to see all aliases.')}")
        print()
        return 1

    # Capability
    cap_line = GREEN(result["capability"])
    alias_hint = DIM(f"  (matched alias: \"{result['matched_alias']}\")")
    print(f"  {BOLD('Capability')}   {cap_line} {alias_hint}")

    # Domain
    if result["domain"]:
        dom_line = CYAN(result["domain"])
        kw_hint = DIM(f"  (matched keyword: \"{result['matched_keyword']}\")")
        print(f"  {BOLD('Domain')}       {dom_line} {kw_hint}")
    else:
        print(f"  {BOLD('Domain')}       {DIM('unknown')}")

    # Agent
    agent = result["agent"] or DIM("none")
    print(f"  {BOLD('Agent')}        {YELLOW(str(agent))}")

    # Prompts
    if result["prompts"]:
        prompts_str = "  ".join(f"/{p}" for p in result["prompts"])
        print(f"  {BOLD('Prompts')}      {prompts_str}")
    else:
        print(f"  {BOLD('Prompts')}      {DIM('none')}")

    # Skills
    if result["skills"]:
        skills_str = "  ".join(result["skills"])
        print(f"  {BOLD('Skills')}       {skills_str}")
    else:
        print(f"  {BOLD('Skills')}       {DIM('none')}")

    print()
    return 0


# ---------------------------------------------------------------------------
# command: guide
# ---------------------------------------------------------------------------


def _print_next_command(command: str) -> None:
    print(f"  {BOLD('Next command')} {command}")


def _print_preview_block(title: str, lines: list[str]) -> None:
    print()
    print(f"  {BOLD(title)}")
    print()
    for line in lines:
        print(f"    {line}")


def _shell_quote(value: str) -> str:
    escaped = value.replace('"', '\\"')
    return f'"{escaped}"'


def cmd_guide_route(request: str | None, routing: dict[str, Any]) -> int:
    if not request or not request.strip():
        print(f"  {YELLOW('WARN')} Please provide a request to route.", file=sys.stderr)
        print(
            "       Example: python scripts/codev-dev.py guide route \"debug kubernetes pod\"",
            file=sys.stderr,
        )
        return 1

    normalized_request = request.strip()
    result = route(normalized_request, routing)

    print()
    print(BOLD("  guide: route"))
    print()
    print(f"  {BOLD('Request')}      {normalized_request}")

    if result["ok"]:
        _print_next_command(f"/route {normalized_request}")
        print(f"  {BOLD('Capability')}   {result['capability']}")
        print(f"  {BOLD('Domain')}       {result['domain'] or 'unknown'}")
        print(f"  {BOLD('Agent')}        {result['agent'] or 'none'}")
        if result["prompts"]:
            print(f"  {BOLD('Prompts')}      {' '.join(f'/{prompt}' for prompt in result['prompts'])}")
    else:
        _print_next_command("/quickstart")
        print(f"  {BOLD('Why')}          {result['error']}")
        print(f"  {BOLD('Fallback')}     Use /quickstart to narrow role, domain, and goal first.")

    print()
    return 0 if result["ok"] else 1


def cmd_guide_extension(kind: str | None) -> int:
    normalized_kind = (kind or "agent").strip().lower()
    prompt_map = {
        "agent": "/new-agent agentId=<kebab> mission=<text>",
        "skill": "/new-skill skillId=<kebab> theme=<text> scope=<when-to-use>",
        "instruction": "/new-instructions file=<name>.instructions.md applyTo=<glob> rules=<text>",
        "prompt": "/prompt-from-theme theme=<goal> intent=<what the prompt should do>",
    }
    output_path_map = {
        "agent": ".github/agents/<id>.agent.md",
        "skill": ".github/skills/<theme>/SKILL.md + examples/README.md",
        "instruction": ".github/instructions/<name>.instructions.md",
        "prompt": ".github/prompts/<name>.prompt.md",
    }

    if normalized_kind not in prompt_map:
        print(f"  {YELLOW('WARN')} --kind must be one of: agent, skill, instruction, prompt.", file=sys.stderr)
        print(
            "       Example: python scripts/codev-dev.py guide extension --kind skill",
            file=sys.stderr,
        )
        return 1

    preview_lines = [
        "1. Create the asset with the shortest matching slash prompt:",
        f"   {prompt_map[normalized_kind]}",
        "2. Confirm the generated file lands in the expected path:",
        f"   {output_path_map[normalized_kind]}",
        "3. Run the structural validators before opening a PR:",
        "   python scripts/validate-customization-registry.py",
        "   python scripts/validate-readme-registry.py",
        "   python scripts/validate-markdown-lint.py",
        "4. If the asset changes routing behavior, also run:",
        "   python scripts/validate-route-smoke.py",
        "5. Open the relevant docs for the longer reference path:",
        "   docs/codev-dev-guide.md",
        "   docs/submodule-guide.md",
    ]

    print()
    print(BOLD("  guide: extension"))
    print()
    print(f"  {BOLD('Kind')}         {normalized_kind}")
    _print_next_command(prompt_map[normalized_kind])
    _print_preview_block("Minimal extension path", preview_lines)
    print()
    return 0


def cmd_guide_issue(
    title: str | None,
    summary: str | None,
    files: list[str],
    acceptance: list[str],
    verification: list[str],
) -> int:
    if not title or not title.strip() or not summary or not summary.strip():
        print(f"  {YELLOW('WARN')} --title and --summary are required.", file=sys.stderr)
        print(
            "       Example: python scripts/codev-dev.py guide issue --title \"Add guided CLI flow\" --summary \"Help contributors prepare issue bodies\"",
            file=sys.stderr,
        )
        return 1

    normalized_title = title.strip()
    normalized_summary = summary.strip()
    issue_slug = re.sub(r"[^a-z0-9]+", "-", normalized_title.lower()).strip("-") or "new-issue"
    issue_title = f"enh: {normalized_title}"
    body_lines = [
        "## Summary",
        normalized_summary,
        "",
        "## Technical approach",
        "- Preview-first contributor flow through scripts/codev-dev.py.",
        "- Keep guided commands read-safe unless the user explicitly writes/publishes later.",
        "",
        "## Files to modify",
    ]
    if files:
        body_lines.extend(f"- `{path}` -- update for this contributor workflow" for path in files)
    else:
        body_lines.append("- `scripts/codev-dev.py` -- implement the guided flow")
        body_lines.append("- `tests/test_codev_dev.py` -- add focused coverage")
    body_lines.extend(
        [
            "",
            "## Sub-tasks",
            "- [ ] Implement the CLI guidance flow",
            "- [ ] Add regression coverage",
            "- [ ] Update contributor docs",
            "",
            "## Acceptance criteria",
        ]
    )
    if acceptance:
        body_lines.extend(f"- [ ] {item}" for item in acceptance)
    else:
        body_lines.append("- [ ] Preview output shows exact next commands")
        body_lines.append("- [ ] Incomplete input returns actionable guidance")
    body_lines.extend(["", "## Verification steps"])
    if verification:
        body_lines.extend(f"1. {step}" for step in verification)
    else:
        body_lines.append("1. python -m pytest tests/test_codev_dev.py -q")
    body_lines.extend(["", "## Progress log", "- Created from codev-dev guide issue preview."])

    print()
    print(BOLD("  guide: issue"))
    print()
    print(f"  {BOLD('Issue title')}   {issue_title}")
    _print_next_command(
        "gh issue create --title "
        f"{_shell_quote(issue_title)} --body-file temp/{issue_slug}.md"
    )
    _print_preview_block("Preview body", body_lines)
    print()
    return 0


def cmd_guide_test_plan(
    what: str | None,
    why: str | None,
    unit_items: list[str],
    integration_items: list[str],
    manual_items: list[str],
    not_tested_items: list[str],
) -> int:
    if not what or not what.strip() or not why or not why.strip():
        print(f"  {YELLOW('WARN')} --what and --why are required.", file=sys.stderr)
        print(
            "       Example: python scripts/codev-dev.py guide test-plan --what \"guided route flow\" --why \"Contributors need exact next commands\"",
            file=sys.stderr,
        )
        return 1

    unit_lines = unit_items or ["parser accepts the guided flow arguments", "happy path preview renders exact next commands"]
    integration_lines = integration_items or ["subprocess invocation returns preview-only output", "missing input exits non-zero with actionable guidance"]
    manual_lines = manual_items or ["spot-check the suggested command text against the intended workflow"]
    not_tested_lines = not_tested_items or ["publishing to GitHub -- preview only in this flow"]

    preview_lines = [
        f"## Test plan -- {what.strip()}",
        "",
        f"**What**: {what.strip()}",
        f"**Why**: {why.strip()}",
        "**How**:",
        f"- Unit: {'; '.join(unit_lines)}",
        f"- Integration: {'; '.join(integration_lines)}",
        f"- E2E / manual: {'; '.join(manual_lines)}",
        f"**Not tested**: {'; '.join(not_tested_lines)}",
        "**CI gate**: `python -m pytest tests/test_codev_dev.py -q` exits 0",
    ]

    print()
    print(BOLD("  guide: test-plan"))
    print()
    _print_next_command("python -m pytest tests/test_codev_dev.py -q")
    _print_preview_block("Preview test plan", preview_lines)
    print()
    return 0


def cmd_guide_pr_checklist(
    issue: str | None,
    verification: list[str],
    risks: list[str],
) -> int:
    if not issue or not issue.strip():
        print(f"  {YELLOW('WARN')} --issue is required.", file=sys.stderr)
        print(
            "       Example: python scripts/codev-dev.py guide pr-checklist --issue 40",
            file=sys.stderr,
        )
        return 1

    verification_items = verification or [
        "python -m pytest tests/test_codev_dev.py -q",
        "python scripts/validate-markdown-lint.py",
    ]
    risk_items = risks or [
        "CLI preview text drifts from actual repository workflow -- mitigation: keep tests on exact command strings",
    ]
    preview_lines = [
        f"Closes #{issue.strip()}",
        "",
        "## Summary",
        "- Add guided contributor CLI flows with preview-first output.",
        "",
        "## Verification",
    ]
    preview_lines.extend(f"- {item}" for item in verification_items)
    preview_lines.extend(["", "## Risk notes"])
    preview_lines.extend(f"- {item}" for item in risk_items)

    print()
    print(BOLD("  guide: pr-checklist"))
    print()
    _print_next_command(f"gh pr create --fill --body-file temp/pr-{issue.strip()}.md")
    _print_preview_block("Preview PR checklist", preview_lines)
    print()
    return 0


def cmd_test_route_list(routing: dict[str, Any]) -> int:
    """Print all registered aliases grouped by capability."""
    print()
    print(BOLD("  Registered aliases by capability"))
    print()
    aliases: dict[str, Any] = routing["aliases"]
    for cap, phrases in aliases.items():
        print(f"  {CYAN(cap)}")
        for phrase in (phrases or []):
            print(f"    {DIM('·')} {phrase}")
        print()
    return 0


# ---------------------------------------------------------------------------
# command: doctor
# ---------------------------------------------------------------------------

DOCTOR_VALIDATORS: dict[str, str] = {
    "smoke":    "validate-route-smoke.py",
    "autofix":  "validate-autofix.py",
    "registry": "validate-customization-registry.py",
    "readme":   "validate-readme-registry.py",
    "coverage": "validate-routing-coverage.py",
}

DOCTOR_RECOVERY_HINTS: dict[str, list[str]] = {
    "smoke": [
        'Replay a phrase with: python scripts/codev-dev.py test-route "debug kubernetes pod"',
        "Review routing/aliases.yaml, routing/matrix.yaml, and routing/route-smoke-tests.yaml.",
    ],
    "autofix": [
        "Review the reported routing mismatch and then re-run: python scripts/validate-autofix.py",
    ],
    "registry": [
        "Review .github/ agents/prompts/skills/instructions plus routing/*.yaml for the referenced contract mismatch.",
        "Re-run: python scripts/validate-customization-registry.py",
    ],
    "readme": [
        "Review README.md plus the referenced asset inventory entries, then re-run: python scripts/validate-readme-registry.py",
    ],
    "coverage": [
        "Review routing/matrix.yaml and routing/domains.yaml for uncovered capability/domain pairs.",
        "Re-run: python scripts/validate-routing-coverage.py",
    ],
}


def _run_validator(name: str) -> tuple[bool, str, str, float]:
    """Run one validator. Returns (passed, stdout, stderr, elapsed_seconds)."""
    script = SCRIPTS_DIR / DOCTOR_VALIDATORS[name]
    if not script.exists():
        return True, f"[SKIP] {script.name} not found", "", 0.0
    t0 = time.monotonic()
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    elapsed = time.monotonic() - t0
    return result.returncode == 0, result.stdout, result.stderr, elapsed


def cmd_doctor(validators: list[str]) -> int:
    print()
    print(BOLD("  CoDev doctor"))
    print()

    # 1. Check required files exist
    required_files = [
        ROUTING_DIR / "capabilities.yaml",
        ROUTING_DIR / "aliases.yaml",
        ROUTING_DIR / "domains.yaml",
        ROUTING_DIR / "matrix.yaml",
        ROUTING_DIR / "route-smoke-tests.yaml",
        AGENTS_DIR,
        PROMPTS_DIR,
        SKILLS_DIR,
    ]
    all_present = True
    print(f"  {BOLD('Required files')}")
    for path in required_files:
        exists = path.exists()
        icon = GREEN("✅") if exists else RED("❌")
        label = str(path.relative_to(ROOT))
        print(f"    {icon} {label}")
        if not exists:
            all_present = False
    print()

    # 2. Run validators
    print(f"  {BOLD('Validators')}")
    passed_count = 0
    failed: list[str] = []

    for name in validators:
        ok, stdout, stderr, elapsed = _run_validator(name)
        icon = GREEN("✅") if ok else RED("❌")
        script_name = DOCTOR_VALIDATORS[name]
        timing = DIM(f"({elapsed:.2f}s)")
        print(f"    {icon} {script_name} {timing}")
        # Show first error line if failed
        if not ok:
            failed.append(name)
            for line in (stdout + stderr).strip().splitlines()[:3]:
                print(f"       {DIM(line)}")
            for hint in DOCTOR_RECOVERY_HINTS.get(name, []):
                print(f"       {DIM(f'Next: {hint}')}")
        else:
            passed_count += 1

    total = len(validators)
    print()

    # 3. Summary
    all_ok = all_present and not failed
    if all_ok:
        print(f"  {GREEN('✅')} {BOLD('All checks passed')} ({passed_count}/{total} validators, all required files present)")
    else:
        if not all_present:
            print(f"  {RED('❌')} Some required files are missing")
        if failed:
            print(
                f"  {RED('❌')} {len(failed)}/{total} validator(s) failed: "
                + ", ".join(failed)
            )
        print()
        print(f"  {DIM('Run:  python scripts/validate-autofix.py  for auto-fix suggestions.')}")

    print()
    return 0 if all_ok else 1


# ---------------------------------------------------------------------------
# command: new agent
# ---------------------------------------------------------------------------

_AGENT_TEMPLATE = """\
---
name: "{name}"
description: "{description}"
---

# {name}

## Responsibilities

- TODO: define the primary responsibilities of this agent.

## Output format

- TODO: define the expected output format and structure.

## Constraints

- TODO: define what this agent must not do.
"""


def cmd_new_agent(
    name: str,
    description: str,
    write: bool,
    output_dir: Path | None = None,
) -> int:
    """
    Scaffold a new agent file.

    Args:
        name:        Display name of the agent (e.g. "My Specialist")
        description: One-line description for the frontmatter
        write:       If True, write the file to disk. If False, dry-run only.
        output_dir:  Override directory for the output file (default: .github/agents/).
    """
    # Derive safe slug and filename
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    filename = f"{slug}.agent.md"
    target_dir = output_dir if output_dir is not None else AGENTS_DIR
    target_path = target_dir / filename

    content = _AGENT_TEMPLATE.format(name=name, description=description)

    print()
    print(BOLD(f"  new agent: {name!r}"))
    print()
    print(f"  {BOLD('File')}         {target_path.relative_to(ROOT) if output_dir is None else target_path}")
    print(f"  {BOLD('Slug')}         {slug}")
    print()
    print(f"  {BOLD('Preview')} {'(dry-run — nothing written)' if not write else ''}")
    if write:
        print(f"  {BOLD('Execution')}    write requested — review the preview above before file creation continues")
    print()
    for line in content.splitlines():
        print(f"    {DIM(line)}")
    print()

    # Safety: never overwrite an existing file
    if target_path.exists():
        print(f"  {RED('❌')} File already exists: {target_path}")
        print(f"       Choose a different name or delete the existing file first.")
        print()
        return 1

    if not write:
        print(f"  {YELLOW('ℹ')}  Dry-run mode. Pass --write to create the file.")
        print()
        return 0

    target_dir.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    print(f"  {GREEN('✅')} Created: {target_path}")
    print()
    print(f"  {DIM('Next steps:')}")
    print(f"  {DIM('  1. Edit')} {target_path.name} {DIM('— fill in responsibilities and output format')}")
    print(f"  {DIM('  2. Add a routing rule in routing/matrix.yaml pointing to')} \"{name}\"")
    print(f"  {DIM('  3. Run:  python scripts/validate-customization-registry.py')}")
    print()
    return 0


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="codev-dev",
        description=textwrap.dedent("""\
            CoDev interactive developer CLI.
            All commands are read-safe by default.
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # --- test-route ---
    tr = sub.add_parser(
        "test-route",
        help="Run the routing engine on a phrase and explain the result.",
        description="Route a phrase and explain capability, domain, agent, prompts, and skills.",
    )
    tr.add_argument(
        "phrase",
        nargs="?",
        help="The phrase to route (e.g. \"debug kubernetes pod\").",
    )
    tr.add_argument(
        "--list",
        action="store_true",
        help="List all registered aliases grouped by capability.",
    )

    # --- doctor ---
    doc = sub.add_parser(
        "doctor",
        help="Health-check the repository (read-only).",
        description="Run all validation scripts and check required files.",
    )
    doc.add_argument(
        "--validators",
        nargs="+",
        choices=list(DOCTOR_VALIDATORS.keys()),
        default=list(DOCTOR_VALIDATORS.keys()),
        metavar="VALIDATOR",
        help=(
            "Validators to run. Choices: "
            + ", ".join(DOCTOR_VALIDATORS.keys())
            + ". Default: all."
        ),
    )

    # --- guide ---
    guide = sub.add_parser(
        "guide",
        help="Preview guided contributor flows with exact next commands.",
        description="Show preview-first contributor workflows for route, issues, test plans, and PR checklists.",
    )
    guide_sub = guide.add_subparsers(dest="guide_type", metavar="FLOW")

    guide_route = guide_sub.add_parser(
        "route",
        help="Preview the best next routing command for a request.",
    )
    guide_route.add_argument(
        "request",
        nargs="?",
        help="Free-form request to route.",
    )

    guide_extension = guide_sub.add_parser(
        "extension",
        help="Preview the shortest extension onboarding path.",
    )
    guide_extension.add_argument(
        "--kind",
        default="agent",
        help="Asset kind: agent, skill, instruction, or prompt.",
    )

    guide_issue = guide_sub.add_parser(
        "issue",
        help="Preview a governance-compliant issue body.",
    )
    guide_issue.add_argument("--title", help="Short issue title without the enh: prefix.")
    guide_issue.add_argument("--summary", help="Why this work is needed.")
    guide_issue.add_argument(
        "--file",
        dest="files",
        action="append",
        default=[],
        help="File to include under Files to modify. Repeat as needed.",
    )
    guide_issue.add_argument(
        "--acceptance",
        action="append",
        default=[],
        help="Acceptance criterion to include. Repeat as needed.",
    )
    guide_issue.add_argument(
        "--verification",
        action="append",
        default=[],
        help="Verification step to include. Repeat as needed.",
    )

    guide_test_plan = guide_sub.add_parser(
        "test-plan",
        help="Preview a test-plan template for the current change.",
    )
    guide_test_plan.add_argument("--what", help="Behavior or change under test.")
    guide_test_plan.add_argument("--why", help="Why this test coverage matters.")
    guide_test_plan.add_argument("--unit", action="append", default=[], help="Unit-test focus area. Repeat as needed.")
    guide_test_plan.add_argument(
        "--integration",
        action="append",
        default=[],
        help="Integration-test focus area. Repeat as needed.",
    )
    guide_test_plan.add_argument("--manual", action="append", default=[], help="Manual verification step. Repeat as needed.")
    guide_test_plan.add_argument(
        "--not-tested",
        dest="not_tested",
        action="append",
        default=[],
        help="Explicit exclusion. Repeat as needed.",
    )

    guide_pr = guide_sub.add_parser(
        "pr-checklist",
        help="Preview a PR description checklist.",
    )
    guide_pr.add_argument("--issue", help="Linked issue number.")
    guide_pr.add_argument(
        "--verification",
        action="append",
        default=[],
        help="Verification command or result. Repeat as needed.",
    )
    guide_pr.add_argument(
        "--risk",
        dest="risks",
        action="append",
        default=[],
        help="Risk note with mitigation. Repeat as needed.",
    )

    # --- new ---
    new = sub.add_parser(
        "new",
        help="Scaffold a new CoDev asset (dry-run by default).",
    )
    new_sub = new.add_subparsers(dest="asset_type", metavar="ASSET")

    ag = new_sub.add_parser(
        "agent",
        help="Scaffold a new agent file.",
        description=(
            "Scaffold a new .agent.md file under .github/agents/. "
            "Dry-run by default; pass --write to create the file."
        ),
    )
    ag.add_argument("name", help="Display name for the agent (e.g. \"My Specialist\").")
    ag.add_argument(
        "--description",
        default="TODO: describe what this agent does.",
        help="One-line description for the agent frontmatter.",
    )
    ag.add_argument(
        "--write",
        action="store_true",
        help="Actually write the file to disk (default: dry-run).",
    )

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    # Ensure UTF-8 output on Windows terminals
    _ensure_utf8_stdout()

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    # Load routing data once (shared across commands that need it)
    try:
        routing = _load_routing()
    except FileNotFoundError as exc:
        print(f"  {RED('❌')} {exc}", file=sys.stderr)
        print(
            f"  Are you running from the CoDev repository root?",
            file=sys.stderr,
        )
        return 2

    if args.command == "test-route":
        if args.list:
            return cmd_test_route_list(routing)
        if not args.phrase:
            print(f"  {YELLOW('⚠')}  Please provide a phrase. Example:", file=sys.stderr)
            print(f'       python scripts/codev-dev.py test-route "debug kubernetes pod"',
                  file=sys.stderr)
            return 1
        return cmd_test_route(args.phrase, routing)

    if args.command == "doctor":
        return cmd_doctor(args.validators)

    if args.command == "guide":
        if args.guide_type is None:
            print("  WARN Specify guide flow: route, issue, test-plan, pr-checklist", file=sys.stderr)
            return 1
        if args.guide_type == "route":
            return cmd_guide_route(args.request, routing)
        if args.guide_type == "extension":
            return cmd_guide_extension(args.kind)
        if args.guide_type == "issue":
            return cmd_guide_issue(
                title=args.title,
                summary=args.summary,
                files=args.files,
                acceptance=args.acceptance,
                verification=args.verification,
            )
        if args.guide_type == "test-plan":
            return cmd_guide_test_plan(
                what=args.what,
                why=args.why,
                unit_items=args.unit,
                integration_items=args.integration,
                manual_items=args.manual,
                not_tested_items=args.not_tested,
            )
        if args.guide_type == "pr-checklist":
            return cmd_guide_pr_checklist(
                issue=args.issue,
                verification=args.verification,
                risks=args.risks,
            )

    if args.command == "new":
        if args.asset_type is None:
            print(f"  {YELLOW('⚠')}  Specify asset type: agent", file=sys.stderr)
            return 1
        if args.asset_type == "agent":
            return cmd_new_agent(
                name=args.name,
                description=args.description,
                write=args.write,
            )

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
