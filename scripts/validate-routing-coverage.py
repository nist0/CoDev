"""validate-routing-coverage.py

Analyses routing/matrix.yaml against routing/capabilities.yaml and
routing/domains.yaml and reports which capability×domain combinations
lack a dedicated rule and rely only on the generic capability fallback.

Exit code: 0  — report only (default).
             1  — if --strict and uncovered pairs exceed --threshold.

Usage:
    python scripts/validate-routing-coverage.py
    python scripts/validate-routing-coverage.py --strict --threshold 5
    python scripts/validate-routing-coverage.py --json-out routing-coverage.json
    python scripts/validate-routing-coverage.py --strict --threshold 0 --json-out routing-coverage.json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ROUTING_DIR = ROOT / "routing"


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main(strict: bool = False, threshold: int = 0, json_out: str | None = None) -> int:
    caps_data = load_yaml(ROUTING_DIR / "capabilities.yaml")
    domains_data = load_yaml(ROUTING_DIR / "domains.yaml")
    matrix_data = load_yaml(ROUTING_DIR / "matrix.yaml")

    capabilities: list[str] = [c["id"] for c in caps_data["capabilities"]]
    domains: list[str] = [d["id"] for d in domains_data["domains"]]
    rules: list[dict[str, Any]] = matrix_data["routing_rules"]

    # Index rules ---------------------------------------------------------
    # explicit: set of (capability, domain) pairs that have a dedicated rule
    explicit: set[tuple[str, str]] = set()
    # fallback_agent: capability → agent name for the capability-only fallback
    fallback_agent: dict[str, str] = {}
    # domain_aware: capabilities that have at least one domain-specific rule
    domain_aware: set[str] = set()

    for rule in rules:
        when = rule.get("when", {})
        cap: str | None = when.get("capability")
        dom: str | None = when.get("domain")
        if not cap:
            continue
        if dom:
            explicit.add((cap, dom))
            domain_aware.add(cap)
        else:
            fallback_agent[cap] = rule.get("suggest", {}).get("agent", "?")

    # Classify capabilities -----------------------------------------------
    agnostic = [c for c in capabilities if c not in domain_aware]
    aware = [c for c in capabilities if c in domain_aware]

    # Compute gaps --------------------------------------------------------
    gaps: dict[str, list[str]] = {}
    for cap in aware:
        missing = [d for d in domains if (cap, d) not in explicit]
        if missing:
            gaps[cap] = missing

    total_explicit = len(explicit)
    total_possible = len(aware) * len(domains) if aware else 0
    coverage_pct = (
        round(100 * total_explicit / total_possible) if total_possible else 100
    )
    total_gaps = sum(len(v) for v in gaps.values())

    # Report --------------------------------------------------------------
    W = 62
    print("=" * W)
    print("Routing Coverage Report")
    print("=" * W)
    print(f"  Capabilities            : {len(capabilities)}")
    print(f"  Domains                 : {len(domains)}")
    print(f"  Domain-aware caps       : {len(aware)}")
    print(f"  Domain-agnostic caps    : {len(agnostic)}")
    print(f"  Explicit rules (cap+dom): {total_explicit} / {total_possible}")
    print(f"  Coverage                : {coverage_pct}%")
    print(f"  Gaps (fallback only)    : {total_gaps}")
    print("=" * W)
    print()

    # Domain-agnostic capabilities (informational, not gaps)
    print("Domain-agnostic capabilities (fallback-only - intentional):")
    for cap in agnostic:
        fb = fallback_agent.get(cap)
        marker = f"-> {fb}" if fb else "[X] NO fallback rule - fix required!"
        print(f"  {cap:<28}  {marker}")
    print()

    # Gap table
    if not gaps:
        print("[OK] No gaps - every domain-aware capability has a rule for every domain.")
    else:
        print(
            f"[WARN] {total_gaps} capability x domain pair(s) have no dedicated rule"
            " and fall back to the generic handler:\n"
        )
        for cap in sorted(gaps):
            fb = fallback_agent.get(cap, "?")
            print(f"  [{cap}]  fallback -> {fb}")
            for dom in gaps[cap]:
                print(f"    - {dom}")
        print()
        print(
            "  These are not necessarily bugs - a generic fallback may be fine.\n"
            "  Add a domain-specific rule only when a richer skill/agent pairing\n"
            "  would meaningfully improve the recommendation quality."
        )

    print()
    print("=" * W)

    # JSON artifact -----------------------------------------------------------
    if json_out is not None:
        artifact: dict[str, Any] = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "capabilities": len(capabilities),
                "domains": len(domains),
                "domain_aware_caps": len(aware),
                "domain_agnostic_caps": len(agnostic),
                "explicit_rules": total_explicit,
                "possible_pairs": total_possible,
                "coverage_pct": coverage_pct,
                "gaps": total_gaps,
            },
            "gaps_by_capability": {
                cap: gaps[cap] for cap in sorted(gaps)
            },
            "domain_agnostic_capabilities": {
                cap: fallback_agent.get(cap, "?") for cap in agnostic
            },
        }
        out_path = Path(json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
        print(f"\nJSON artifact written to: {out_path}")

    if strict and total_gaps > threshold:
        print(
            f"\nSTRICT MODE: {total_gaps} gap(s) exceed threshold of {threshold}. Exiting 1."
        )
        return 1

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Report routing coverage: capability × domain vs matrix rules."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if the number of gaps exceeds --threshold.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=0,
        help="Maximum allowed gaps in --strict mode (default: 0).",
    )
    parser.add_argument(
        "--json-out",
        metavar="PATH",
        default=None,
        help="Write a machine-readable JSON coverage artifact to PATH.",
    )
    args = parser.parse_args()

    if args.threshold != 0 and not args.strict:
        print(
            "Warning: --threshold has no effect without --strict. "
            "Add --strict to enable the gap threshold gate.",
            file=sys.stderr,
        )

    sys.exit(main(strict=args.strict, threshold=args.threshold, json_out=args.json_out))
