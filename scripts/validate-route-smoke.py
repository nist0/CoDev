from __future__ import annotations

from pathlib import Path
from typing import Any

import sys
import yaml


ROOT = Path(__file__).resolve().parents[1]
ROUTING_DIR = ROOT / "routing"


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def detect_capability(request: str, aliases: dict[str, list[str]]) -> str | None:
    text = request.lower()
    best_match: tuple[int, str] | None = None

    for capability, phrases in aliases.items():
        for phrase in phrases:
            p = phrase.lower()
            if p in text:
                score = len(p)
                if best_match is None or score > best_match[0]:
                    best_match = (score, capability)

    return best_match[1] if best_match else None


def detect_domain(request: str, domains: list[dict[str, Any]]) -> str | None:
    text = request.lower()
    best_match: tuple[int, str] | None = None

    for domain in domains:
        domain_id = domain["id"]
        for kw in domain.get("keywords", []):
            k = str(kw).lower()
            if k in text:
                score = len(k)
                if best_match is None or score > best_match[0]:
                    best_match = (score, domain_id)

    return best_match[1] if best_match else None


def resolve_route(
    capability: str,
    domain: str | None,
    matrix_rules: list[dict[str, Any]],
    capabilities: list[dict[str, Any]],
) -> dict[str, Any]:
    for rule in matrix_rules:
        when = rule.get("when", {})
        if when.get("capability") != capability:
            continue
        required_domain = when.get("domain")
        if required_domain is not None and required_domain != domain:
            continue
        return rule.get("suggest", {})

    default_agent = None
    for item in capabilities:
        if item.get("id") == capability:
            default_agent = item.get("default_agent")
            break

    return {"agent": default_agent, "prompts": [], "skills": []}


def assert_expected(
    actual: dict[str, Any],
    expected: dict[str, Any],
    case_idx: int,
    request: str,
) -> list[str]:
    errors: list[str] = []
    for key, expected_value in expected.items():
        actual_value = actual.get(key)
        if actual_value != expected_value:
            errors.append(
                f"[case {case_idx}] mismatch on '{key}': "
                f"expected={expected_value!r} actual={actual_value!r} request={request!r}"
            )
    return errors


def build_recovery_actions(errors: list[str], failing_requests: list[str]) -> list[str]:
    actions: list[str] = []
    if any("no capability matched" in error for error in errors):
        if failing_requests:
            actions.append(
                "Replay the failing phrase with: "
                f'python scripts/codev-dev.py test-route "{failing_requests[0]}"'
            )
        actions.append(
            "Review routing/aliases.yaml and routing/route-smoke-tests.yaml for the missing alias coverage."
        )
    if any("mismatch on" in error for error in errors):
        actions.append(
            "Review routing/matrix.yaml and routing/route-smoke-tests.yaml for the mismatched capability, domain, or suggestion."
        )
    actions.append("Re-run: python scripts/validate-route-smoke.py")
    return actions


def main() -> int:
    capabilities_doc = load_yaml(ROUTING_DIR / "capabilities.yaml")
    aliases_doc = load_yaml(ROUTING_DIR / "aliases.yaml")
    domains_doc = load_yaml(ROUTING_DIR / "domains.yaml")
    matrix_doc = load_yaml(ROUTING_DIR / "matrix.yaml")
    smoke_doc = load_yaml(ROUTING_DIR / "route-smoke-tests.yaml")

    capabilities = capabilities_doc.get("capabilities", [])
    aliases = aliases_doc.get("aliases", {})
    domains = domains_doc.get("domains", [])
    routing_rules = matrix_doc.get("routing_rules", [])
    cases = smoke_doc.get("cases", [])

    errors: list[str] = []
    failing_requests: list[str] = []

    for index, case in enumerate(cases, start=1):
        request = str(case["request"])
        expected = case.get("expect", {})

        capability = detect_capability(request, aliases)
        domain = detect_domain(request, domains)

        if capability is None:
            errors.append(f"[case {index}] no capability matched for request={request!r}")
            failing_requests.append(request)
            continue

        suggest = resolve_route(capability, domain, routing_rules, capabilities)

        actual = {
            "capability": capability,
            "domain": domain,
            "agent": suggest.get("agent"),
            "prompts": suggest.get("prompts", []),
            "skills": suggest.get("skills", []),
        }

        case_errors = assert_expected(actual, expected, index, request)
        if case_errors:
            failing_requests.append(request)
        errors.extend(case_errors)

    total_cases = len(cases)
    if errors:
        print(f"Route smoke validation failed: {len(errors)} issue(s) across {total_cases} case(s).")
        for error in errors:
            print(f" - {error}")
        print("Next actions:")
        for action in build_recovery_actions(errors, failing_requests):
            print(f" - {action}")
        return 1

    print(f"Route smoke validation passed: {total_cases} case(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
