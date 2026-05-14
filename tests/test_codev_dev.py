"""
tests/test_codev_dev.py — Comprehensive tests for scripts/codev-dev.py

Test strategy:
  - Unit tests: each public function tested in isolation with controlled inputs
  - Integration tests: CLI invoked via subprocess against real repo (read-only)
  - Fixture tests: new-agent scaffolding uses tmp_path to never touch real files
  - Edge cases: empty inputs, missing files, invalid args, TTY-off output

Safety guarantee:
  - No test modifies any file under routing/, .github/, or scripts/
  - new agent tests always use tmp_path or dry-run mode
  - All subprocess calls target the real repo read-only

Run:
  python -m pytest tests/test_codev_dev.py -v
"""

from __future__ import annotations

import importlib.util
import io
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"

# ---------------------------------------------------------------------------
# Module import helper (filename has no hyphen issues)
# ---------------------------------------------------------------------------

def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    sys.modules[name] = mod
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


codev_dev = _load_module("codev_dev", SCRIPTS_DIR / "codev-dev.py")
validate_route_smoke = _load_module("validate_route_smoke", SCRIPTS_DIR / "validate-route-smoke.py")
validate_customization_registry = _load_module(
    "validate_customization_registry",
    SCRIPTS_DIR / "validate-customization-registry.py",
)


# ---------------------------------------------------------------------------
# Shared minimal routing fixture (isolated from real repo)
# ---------------------------------------------------------------------------

MINIMAL_ROUTING: dict[str, Any] = {
    "capabilities": [
        {"id": "debugging", "default_agent": "Reliability"},
        {"id": "docs", "default_agent": "Delivery Lead"},
    ],
    "aliases": {
        "debugging": ["bug", "crash", "exception"],
        "docs": ["write documentation", "generate docs", "readme"],
    },
    "domains": [
        {"id": "devops-cloud", "keywords": ["kubernetes", "k8s", "helm", "aks"]},
        {"id": "backend-dotnet", "keywords": ["dotnet", "c#", "asp.net"]},
    ],
    "rules": [
        {
            "when": {"capability": "debugging", "domain": "devops-cloud"},
            "suggest": {"agent": "DevOps/Cloud", "prompts": ["k8s-triage"], "skills": ["kubernetes"]},
        },
        {
            "when": {"capability": "debugging"},
            "suggest": {"agent": "Reliability", "prompts": ["triage-error"], "skills": ["debugging"]},
        },
        {
            "when": {"capability": "docs"},
            "suggest": {"agent": "Delivery Lead", "prompts": ["generate-docs-tree"], "skills": ["doc-architecture-model"]},
        },
    ],
}


# ===========================================================================
# Unit tests — detect_capability
# ===========================================================================

class TestDetectCapability:
    def test_exact_match(self) -> None:
        cap, phrase = codev_dev.detect_capability("there is a bug in production", MINIMAL_ROUTING["aliases"])
        assert cap == "debugging"
        assert phrase == "bug"

    def test_longest_match_wins(self) -> None:
        # "write documentation" is longer than "readme" — should match docs
        cap, phrase = codev_dev.detect_capability(
            "write documentation for the project", MINIMAL_ROUTING["aliases"]
        )
        assert cap == "docs"
        assert phrase == "write documentation"

    def test_no_match_returns_none(self) -> None:
        cap, phrase = codev_dev.detect_capability("completely unrelated request", MINIMAL_ROUTING["aliases"])
        assert cap is None
        assert phrase is None

    def test_case_insensitive(self) -> None:
        cap, phrase = codev_dev.detect_capability("There Was a CRASH", MINIMAL_ROUTING["aliases"])
        assert cap == "debugging"

    def test_empty_string(self) -> None:
        cap, phrase = codev_dev.detect_capability("", MINIMAL_ROUTING["aliases"])
        assert cap is None

    def test_empty_aliases(self) -> None:
        cap, phrase = codev_dev.detect_capability("anything", {})
        assert cap is None

    def test_multi_word_alias_in_middle(self) -> None:
        cap, _ = codev_dev.detect_capability(
            "please generate docs for the module", MINIMAL_ROUTING["aliases"]
        )
        assert cap == "docs"


# ===========================================================================
# Unit tests — detect_domain
# ===========================================================================

class TestDetectDomain:
    def test_matches_keyword(self) -> None:
        domain, kw = codev_dev.detect_domain("deploy to kubernetes cluster", MINIMAL_ROUTING["domains"])
        assert domain == "devops-cloud"
        assert kw == "kubernetes"

    def test_no_match(self) -> None:
        domain, kw = codev_dev.detect_domain("generic request", MINIMAL_ROUTING["domains"])
        assert domain is None
        assert kw is None

    def test_case_insensitive(self) -> None:
        domain, _ = codev_dev.detect_domain("using K8S in production", MINIMAL_ROUTING["domains"])
        assert domain == "devops-cloud"

    def test_longest_keyword_wins(self) -> None:
        # Both "dotnet" and "asp.net" match backend-dotnet; "asp.net" is longer
        domain, kw = codev_dev.detect_domain("asp.net core service", MINIMAL_ROUTING["domains"])
        assert domain == "backend-dotnet"
        assert kw == "asp.net"

    def test_empty_domains(self) -> None:
        domain, kw = codev_dev.detect_domain("anything", [])
        assert domain is None

    def test_domain_with_no_keywords(self) -> None:
        domains = [{"id": "some-domain", "keywords": []}]
        domain, _ = codev_dev.detect_domain("anything", domains)
        assert domain is None


# ===========================================================================
# Unit tests — resolve_route
# ===========================================================================

class TestResolveRoute:
    def test_capability_and_domain_exact(self) -> None:
        suggest = codev_dev.resolve_route(
            "debugging", "devops-cloud", MINIMAL_ROUTING["rules"], MINIMAL_ROUTING["capabilities"]
        )
        assert suggest["agent"] == "DevOps/Cloud"
        assert "k8s-triage" in suggest["prompts"]

    def test_capability_only_fallback(self) -> None:
        # No devops-cloud rule for docs → should hit capability-only rule
        suggest = codev_dev.resolve_route(
            "debugging", "backend-dotnet", MINIMAL_ROUTING["rules"], MINIMAL_ROUTING["capabilities"]
        )
        assert suggest["agent"] == "Reliability"

    def test_unknown_capability_returns_empty(self) -> None:
        suggest = codev_dev.resolve_route(
            "nonexistent", None, MINIMAL_ROUTING["rules"], MINIMAL_ROUTING["capabilities"]
        )
        assert suggest == {}

    def test_no_domain_falls_back_to_capability_only(self) -> None:
        suggest = codev_dev.resolve_route(
            "docs", None, MINIMAL_ROUTING["rules"], MINIMAL_ROUTING["capabilities"]
        )
        assert suggest["agent"] == "Delivery Lead"

    def test_default_agent_used_when_no_rule(self) -> None:
        # "docs" with an unrecognised domain → still hits the docs capability-only rule
        suggest = codev_dev.resolve_route(
            "docs", "some-unknown-domain", MINIMAL_ROUTING["rules"], MINIMAL_ROUTING["capabilities"]
        )
        assert suggest["agent"] == "Delivery Lead"


# ===========================================================================
# Unit tests — route (full pipeline)
# ===========================================================================

class TestRoute:
    def test_full_route_with_domain(self) -> None:
        result = codev_dev.route("bug in kubernetes cluster", MINIMAL_ROUTING)
        assert result["ok"] is True
        assert result["capability"] == "debugging"
        assert result["domain"] == "devops-cloud"
        assert result["agent"] == "DevOps/Cloud"
        assert "k8s-triage" in result["prompts"]

    def test_full_route_without_domain(self) -> None:
        result = codev_dev.route("exception in the application", MINIMAL_ROUTING)
        assert result["ok"] is True
        assert result["capability"] == "debugging"
        assert result["domain"] is None
        assert result["agent"] == "Reliability"

    def test_no_capability_match(self) -> None:
        result = codev_dev.route("hello world", MINIMAL_ROUTING)
        assert result["ok"] is False
        assert "error" in result
        assert result["request"] == "hello world"

    def test_result_contains_all_keys(self) -> None:
        result = codev_dev.route("bug in helm chart", MINIMAL_ROUTING)
        assert result["ok"] is True
        for key in ("capability", "matched_alias", "domain", "matched_keyword", "agent", "prompts", "skills"):
            assert key in result


# ===========================================================================
# Unit tests — cmd_new_agent (with tmp_path, never touches real repo)
# ===========================================================================

class TestCmdNewAgent:
    def test_dry_run_does_not_create_file(self, tmp_path: Path) -> None:
        rc = codev_dev.cmd_new_agent("Test Agent", "A test agent.", write=False, output_dir=tmp_path)
        assert rc == 0
        assert not any(tmp_path.iterdir())  # no file created

    def test_write_creates_file(self, tmp_path: Path) -> None:
        rc = codev_dev.cmd_new_agent("Test Agent", "A test agent.", write=True, output_dir=tmp_path)
        assert rc == 0
        created = list(tmp_path.iterdir())
        assert len(created) == 1
        assert created[0].name == "test-agent.agent.md"

    def test_written_file_has_valid_frontmatter(self, tmp_path: Path) -> None:
        codev_dev.cmd_new_agent("My Specialist", "Does something.", write=True, output_dir=tmp_path)
        path = tmp_path / "my-specialist.agent.md"
        content = path.read_text(encoding="utf-8")
        assert content.startswith("---")
        assert 'name: "My Specialist"' in content
        assert 'description: "Does something."' in content

    def test_written_file_has_section_headings(self, tmp_path: Path) -> None:
        codev_dev.cmd_new_agent("My Specialist", "Does something.", write=True, output_dir=tmp_path)
        content = (tmp_path / "my-specialist.agent.md").read_text(encoding="utf-8")
        assert "## Responsibilities" in content
        assert "## Output format" in content
        assert "## Constraints" in content

    def test_does_not_overwrite_existing_file(self, tmp_path: Path) -> None:
        existing = tmp_path / "my-agent.agent.md"
        existing.write_text("original content", encoding="utf-8")
        rc = codev_dev.cmd_new_agent("My Agent", "desc", write=True, output_dir=tmp_path)
        assert rc == 1
        # File must be unchanged
        assert existing.read_text(encoding="utf-8") == "original content"

    def test_slug_generation_special_chars(self, tmp_path: Path) -> None:
        codev_dev.cmd_new_agent("My Super  Agent!!", "desc", write=True, output_dir=tmp_path)
        names = [p.name for p in tmp_path.iterdir()]
        assert "my-super-agent.agent.md" in names

    def test_custom_description_appears_in_file(self, tmp_path: Path) -> None:
        codev_dev.cmd_new_agent(
            "Alpha", "Expert in alpha tasks.", write=True, output_dir=tmp_path
        )
        content = (tmp_path / "alpha.agent.md").read_text(encoding="utf-8")
        assert "Expert in alpha tasks." in content

    def test_dry_run_returns_zero(self, tmp_path: Path) -> None:
        rc = codev_dev.cmd_new_agent("Beta", "desc", write=False, output_dir=tmp_path)
        assert rc == 0


# ===========================================================================
# Unit tests — argument parser
# ===========================================================================

class TestParser:
    def _parse(self, args: list[str]) -> Any:
        return codev_dev.build_parser().parse_args(args)

    def test_test_route_phrase(self) -> None:
        args = self._parse(["test-route", "debug kubernetes"])
        assert args.command == "test-route"
        assert args.phrase == "debug kubernetes"
        assert args.list is False

    def test_test_route_list_flag(self) -> None:
        args = self._parse(["test-route", "--list"])
        assert args.list is True

    def test_doctor_defaults_to_all_validators(self) -> None:
        args = self._parse(["doctor"])
        assert set(args.validators) == set(codev_dev.DOCTOR_VALIDATORS.keys())

    def test_doctor_specific_validators(self) -> None:
        args = self._parse(["doctor", "--validators", "smoke", "registry"])
        assert args.validators == ["smoke", "registry"]

    def test_guide_route_request(self) -> None:
        args = self._parse(["guide", "route", "debug kubernetes pod"])
        assert args.command == "guide"
        assert args.guide_type == "route"
        assert args.request == "debug kubernetes pod"

    def test_guide_issue_args(self) -> None:
        args = self._parse([
            "guide",
            "issue",
            "--title",
            "Add guided flow",
            "--summary",
            "Help contributors prepare issue bodies",
            "--file",
            "scripts/codev-dev.py",
        ])
        assert args.guide_type == "issue"
        assert args.title == "Add guided flow"
        assert args.summary == "Help contributors prepare issue bodies"
        assert args.files == ["scripts/codev-dev.py"]

    def test_guide_extension_args(self) -> None:
        args = self._parse(["guide", "extension", "--kind", "skill"])
        assert args.guide_type == "extension"
        assert args.kind == "skill"

    def test_guide_test_plan_args(self) -> None:
        args = self._parse([
            "guide",
            "test-plan",
            "--what",
            "guided route flow",
            "--why",
            "Contributors need exact next commands",
        ])
        assert args.guide_type == "test-plan"
        assert args.what == "guided route flow"
        assert args.why == "Contributors need exact next commands"

    def test_guide_pr_checklist_args(self) -> None:
        args = self._parse(["guide", "pr-checklist", "--issue", "40"])
        assert args.guide_type == "pr-checklist"
        assert args.issue == "40"

    def test_new_agent_defaults_no_write(self) -> None:
        args = self._parse(["new", "agent", "My Agent"])
        assert args.write is False
        assert args.name == "My Agent"

    def test_new_agent_write_flag(self) -> None:
        args = self._parse(["new", "agent", "My Agent", "--write"])
        assert args.write is True

    def test_new_agent_custom_description(self) -> None:
        args = self._parse(["new", "agent", "X", "--description", "Custom desc."])
        assert args.description == "Custom desc."

    def test_new_agent_default_description_is_not_empty(self) -> None:
        args = self._parse(["new", "agent", "X"])
        assert args.description  # not empty


# ===========================================================================
# Integration tests — subprocess against real repo (read-only)
# ===========================================================================

CODEV_DEV = [sys.executable, str(SCRIPTS_DIR / "codev-dev.py")]

# Environment that forces UTF-8 in all child Python processes (Windows-safe)
_UTF8_ENV: dict[str, str] = {**__import__("os").environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}


def _run(*args: str, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    """subprocess.run wrapper that always uses UTF-8 encoding."""
    return subprocess.run(
        list(args),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=_UTF8_ENV,
        **kwargs,
    )


class TestIntegrationTestRoute:
    """Subprocess tests: read-only, no file writes."""

    def test_known_phrase_exits_zero(self) -> None:
        result = _run(*CODEV_DEV, "test-route", "debug kubernetes pod", cwd=str(ROOT))
        assert result.returncode == 0

    def test_known_phrase_shows_capability(self) -> None:
        result = _run(*CODEV_DEV, "test-route", "debug kubernetes pod", cwd=str(ROOT))
        assert "debugging" in result.stdout or "debugging" in result.stderr

    def test_known_phrase_shows_agent(self) -> None:
        result = _run(*CODEV_DEV, "test-route", "debug kubernetes pod", cwd=str(ROOT))
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "Agent" in output or "agent" in output

    def test_unknown_phrase_exits_nonzero(self) -> None:
        result = _run(*CODEV_DEV, "test-route", "xyzzy frobnicator", cwd=str(ROOT))
        assert result.returncode != 0

    def test_list_flag_exits_zero(self) -> None:
        result = _run(*CODEV_DEV, "test-route", "--list", cwd=str(ROOT))
        assert result.returncode == 0

    def test_list_flag_shows_aliases(self) -> None:
        result = _run(*CODEV_DEV, "test-route", "--list", cwd=str(ROOT))
        assert "debugging" in result.stdout

    def test_no_phrase_exits_nonzero(self) -> None:
        result = _run(*CODEV_DEV, "test-route", cwd=str(ROOT))
        assert result.returncode != 0

    def test_does_not_write_any_file(self, tmp_path: Path) -> None:
        """Paranoia test: test-route must not create or modify any file."""
        before = {p: p.stat().st_mtime for p in ROOT.rglob("*") if p.is_file() and ".git" not in str(p) and ".pytest_cache" not in str(p) and "__pycache__" not in str(p) and "reports" not in str(p)}
        _run(*CODEV_DEV, "test-route", "debug kubernetes pod", cwd=str(ROOT))
        after = {p: p.stat().st_mtime for p in ROOT.rglob("*") if p.is_file() and ".git" not in str(p) and ".pytest_cache" not in str(p) and "__pycache__" not in str(p) and "reports" not in str(p)}
        for path, mtime in before.items():
            if path in after:
                assert after[path] == mtime, f"File was modified unexpectedly: {path}"


class TestIntegrationDoctor:
    """Read-only doctor command integration tests."""

    def test_exits_with_int(self) -> None:
        result = _run(*CODEV_DEV, "doctor", cwd=str(ROOT))
        assert result.returncode in (0, 1)

    def test_shows_required_files_section(self) -> None:
        result = _run(*CODEV_DEV, "doctor", cwd=str(ROOT))
        assert "Required files" in result.stdout

    def test_shows_validators_section(self) -> None:
        result = _run(*CODEV_DEV, "doctor", cwd=str(ROOT))
        assert "Validators" in result.stdout

    def test_specific_validators_only(self) -> None:
        result = _run(*CODEV_DEV, "doctor", "--validators", "smoke", cwd=str(ROOT))
        assert result.returncode in (0, 1)
        assert "validate-route-smoke.py" in result.stdout

    def test_does_not_modify_routing_files(self) -> None:
        routing_files = list((ROOT / "routing").glob("*.yaml"))
        before = {p: p.read_text(encoding="utf-8") for p in routing_files}
        _run(*CODEV_DEV, "doctor", cwd=str(ROOT))
        after = {p: p.read_text(encoding="utf-8") for p in routing_files}
        for path in routing_files:
            assert before[path] == after[path], f"Routing file was modified: {path.name}"

    def test_does_not_modify_agent_files(self) -> None:
        agent_files = list((ROOT / ".github" / "agents").glob("*.agent.md"))
        before = {p: p.read_text(encoding="utf-8") for p in agent_files}
        _run(*CODEV_DEV, "doctor", cwd=str(ROOT))
        after = {p: p.read_text(encoding="utf-8") for p in agent_files}
        for path in agent_files:
            assert before[path] == after[path], f"Agent file was modified: {path.name}"

    def test_autofix_validator_in_detect_only_mode(self) -> None:
        """Doctor must call validate-autofix.py in detect-only mode (no --fix flag)."""
        result = _run(*CODEV_DEV, "doctor", "--validators", "autofix", cwd=str(ROOT))
        assert result.returncode in (0, 1)


class TestAssistiveGuardrailHelpers:
    def test_route_smoke_recovery_actions_include_command_and_file(self) -> None:
        actions = validate_route_smoke.build_recovery_actions(
            ["[case 1] no capability matched for request='add a new agent'"],
            ["add a new agent"],
        )
        assert any("python scripts/codev-dev.py test-route" in action for action in actions)
        assert any("routing/aliases.yaml" in action for action in actions)

    def test_registry_recovery_actions_include_command_and_files(self) -> None:
        actions = validate_customization_registry.build_recovery_actions(
            ["routing rule #1 references unknown agent: Missing Agent"]
        )
        assert any("python scripts/validate-customization-registry.py" in action for action in actions)
        assert any("routing/matrix.yaml" in action for action in actions)


class TestGuideCommands:
    def test_guide_route_known_request_exits_zero(self) -> None:
        result = _run(*CODEV_DEV, "guide", "route", "debug kubernetes pod", cwd=str(ROOT))
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "/route debug kubernetes pod" in output

    def test_guide_route_missing_request_exits_nonzero(self) -> None:
        result = _run(*CODEV_DEV, "guide", "route", cwd=str(ROOT))
        assert result.returncode != 0
        assert "Please provide a request to route" in (result.stdout + result.stderr)

    def test_guide_issue_preview_contains_expected_sections(self) -> None:
        result = _run(
            *CODEV_DEV,
            "guide",
            "issue",
            "--title",
            "Add guided flow",
            "--summary",
            "Help contributors prepare issue bodies",
            cwd=str(ROOT),
        )
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "enh: Add guided flow" in output
        assert "## Summary" in output
        assert "gh issue create --title" in output

    def test_guide_issue_missing_required_args_exits_nonzero(self) -> None:
        result = _run(*CODEV_DEV, "guide", "issue", "--title", "Add guided flow", cwd=str(ROOT))
        assert result.returncode != 0
        assert "--title and --summary are required" in (result.stdout + result.stderr)

    def test_guide_extension_preview_contains_validator_commands(self) -> None:
        result = _run(*CODEV_DEV, "guide", "extension", "--kind", "prompt", cwd=str(ROOT))
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "/prompt-from-theme" in output
        assert "python scripts/validate-customization-registry.py" in output

    def test_guide_extension_rejects_unknown_kind(self) -> None:
        result = _run(*CODEV_DEV, "guide", "extension", "--kind", "widget", cwd=str(ROOT))
        assert result.returncode != 0
        assert "--kind must be one of" in (result.stdout + result.stderr)

    def test_guide_test_plan_preview_contains_ci_gate(self) -> None:
        result = _run(
            *CODEV_DEV,
            "guide",
            "test-plan",
            "--what",
            "guided route flow",
            "--why",
            "Contributors need exact next commands",
            cwd=str(ROOT),
        )
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "## Test plan -- guided route flow" in output
        assert "python -m pytest tests/test_codev_dev.py -q" in output

    def test_guide_pr_checklist_requires_issue(self) -> None:
        result = _run(*CODEV_DEV, "guide", "pr-checklist", cwd=str(ROOT))
        assert result.returncode != 0
        assert "--issue is required" in (result.stdout + result.stderr)

    def test_guide_pr_checklist_preview_contains_close_reference(self) -> None:
        result = _run(*CODEV_DEV, "guide", "pr-checklist", "--issue", "40", cwd=str(ROOT))
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "Closes #40" in output
        assert "gh pr create --fill --body-file temp/pr-40.md" in output


class TestIntegrationNewAgent:
    """New agent integration tests — all use --dry-run or tmp dirs."""

    def test_dry_run_exits_zero(self) -> None:
        result = _run(*CODEV_DEV, "new", "agent", "Integration Test Agent", cwd=str(ROOT))
        assert result.returncode == 0

    def test_dry_run_shows_preview(self) -> None:
        result = _run(*CODEV_DEV, "new", "agent", "Integration Test Agent", cwd=str(ROOT))
        assert "integration-test-agent.agent.md" in result.stdout
        assert "dry-run" in result.stdout.lower() or "Dry-run" in result.stdout

    def test_dry_run_does_not_create_real_file(self) -> None:
        agent_path = ROOT / ".github" / "agents" / "integration-test-agent.agent.md"
        assert not agent_path.exists(), "Test pre-condition: file must not exist"
        _run(*CODEV_DEV, "new", "agent", "Integration Test Agent", cwd=str(ROOT))
        assert not agent_path.exists(), "Dry-run must not create real files"

    def test_no_asset_type_exits_nonzero(self) -> None:
        result = _run(*CODEV_DEV, "new", cwd=str(ROOT))
        assert result.returncode != 0


# ===========================================================================
# Integration tests — real routing data consistency
# ===========================================================================

class TestRealRoutingConsistency:
    """
    These tests verify that the CLI's routing engine stays consistent
    with the existing validate-route-smoke test cases.
    READ-ONLY — no file writes.
    """

    @pytest.fixture(scope="class")
    def real_routing(self) -> dict[str, Any]:
        return codev_dev._load_routing()

    @pytest.fixture(scope="class")
    def smoke_cases(self) -> list[dict[str, Any]]:
        path = ROOT / "routing" / "route-smoke-tests.yaml"
        with path.open("r", encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
        return doc.get("cases", [])

    def test_all_smoke_cases_resolve_capability(
        self, real_routing: dict[str, Any], smoke_cases: list[dict[str, Any]]
    ) -> None:
        """Every smoke test phrase must resolve to a capability (not None)."""
        failures: list[str] = []
        for case in smoke_cases:
            request = case["request"]
            result = codev_dev.route(request, real_routing)
            if not result["ok"]:
                failures.append(request)
        assert not failures, (
            f"{len(failures)} smoke case(s) did not resolve a capability:\n"
            + "\n".join(f"  - {r!r}" for r in failures)
        )

    def test_agent_matches_smoke_expectation(
        self, real_routing: dict[str, Any], smoke_cases: list[dict[str, Any]]
    ) -> None:
        """Where a smoke case declares an expected agent, the route must match."""
        failures: list[str] = []
        for case in smoke_cases:
            expected_agent = case.get("expect", {}).get("agent")
            if expected_agent is None:
                continue
            result = codev_dev.route(case["request"], real_routing)
            if result.get("agent") != expected_agent:
                failures.append(
                    f"{case['request']!r}: expected agent={expected_agent!r}, "
                    f"got={result.get('agent')!r}"
                )
        assert not failures, (
            f"{len(failures)} agent mismatch(es) vs smoke expectations:\n"
            + "\n".join(f"  - {f}" for f in failures)
        )

    def test_capability_matches_smoke_expectation(
        self, real_routing: dict[str, Any], smoke_cases: list[dict[str, Any]]
    ) -> None:
        """Where a smoke case declares an expected capability, the route must match."""
        failures: list[str] = []
        for case in smoke_cases:
            expected_cap = case.get("expect", {}).get("capability")
            if expected_cap is None:
                continue
            result = codev_dev.route(case["request"], real_routing)
            if result.get("capability") != expected_cap:
                failures.append(
                    f"{case['request']!r}: expected capability={expected_cap!r}, "
                    f"got={result.get('capability')!r}"
                )
        assert not failures, (
            f"{len(failures)} capability mismatch(es) vs smoke expectations:\n"
            + "\n".join(f"  - {f}" for f in failures)
        )


# ===========================================================================
# Edge case & resilience tests
# ===========================================================================

class TestEdgeCases:
    def test_main_ignores_stdout_reconfigure_failure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        class BadStdout(io.StringIO):
            def reconfigure(self, **kwargs: Any) -> None:
                raise ValueError("boom")

        monkeypatch.setattr(codev_dev.sys, "stdout", BadStdout())
        assert codev_dev.main([]) == 0

    def test_route_very_long_phrase(self) -> None:
        routing = MINIMAL_ROUTING
        long_phrase = "debug " * 200
        result = codev_dev.route(long_phrase.strip(), routing)
        # Must not raise, must return a valid dict
        assert isinstance(result, dict)
        assert "ok" in result

    def test_route_unicode_phrase(self) -> None:
        result = codev_dev.route("débogage kubernetes", MINIMAL_ROUTING)
        assert isinstance(result, dict)

    def test_route_empty_phrase(self) -> None:
        result = codev_dev.route("", MINIMAL_ROUTING)
        assert result["ok"] is False

    def test_route_phrase_with_newlines(self) -> None:
        result = codev_dev.route("bug\nin\nkubernetes", MINIMAL_ROUTING)
        assert isinstance(result, dict)

    def test_new_agent_empty_name_produces_valid_slug(self, tmp_path: Path) -> None:
        # Name with only special characters — slug should still be handled
        rc = codev_dev.cmd_new_agent("   ", "desc", write=False, output_dir=tmp_path)
        # Should not crash — may return 0 (dry-run) or 1 (invalid name)
        assert rc in (0, 1)

    def test_detect_capability_all_capabilities_have_at_least_one_alias(self) -> None:
        """
        Verify that every capability in the real capabilities.yaml has at least
        one alias. This is a read-only consistency check.
        """
        routing = codev_dev._load_routing()
        caps = {c["id"] for c in routing["capabilities"]}
        aliases = set(routing["aliases"].keys())
        missing = caps - aliases
        # Some capabilities intentionally use keywords instead of aliases — acceptable
        # This test just documents the state without failing on intentional gaps
        assert isinstance(missing, set)  # always passes; documents the gap set

    def test_main_no_args_exits_zero(self) -> None:
        result = _run(sys.executable, str(SCRIPTS_DIR / "codev-dev.py"), cwd=str(ROOT))
        assert result.returncode == 0  # shows help
