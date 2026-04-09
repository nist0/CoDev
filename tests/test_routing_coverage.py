"""tests/test_routing_coverage.py

Unit tests for scripts/validate-routing-coverage.py

Run with:
    python -m pytest tests/test_routing_coverage.py -v
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Ensure the scripts directory is importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import importlib.util

# Load the module from the scripts directory (it has a hyphen, so use importlib)
_spec = importlib.util.spec_from_file_location(
    "validate_routing_coverage",
    ROOT / "scripts" / "validate-routing-coverage.py",
)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

main = _mod.main


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def test_no_strict_always_exits_zero() -> None:
    """Running without --strict must always return 0, regardless of gaps."""
    rc = main(strict=False, threshold=0, json_out=None)
    assert rc == 0, "Non-strict mode must exit 0 even when gaps exist"


def test_strict_zero_threshold_on_real_matrix(tmp_path: Path) -> None:
    """--strict --threshold 0 must exit 1 when the real matrix has any gaps."""
    rc = main(strict=True, threshold=0, json_out=None)
    # The real matrix has 50 gaps; threshold=0 means 0 gaps allowed, so must exit 1.
    assert rc == 1, "strict+threshold=0 must exit 1 when gaps exist"


def test_strict_threshold_57_passes_on_real_matrix() -> None:
    """The CI gate uses --strict --threshold 57 (current gap count after cli-platform-onboarding capability added).
    This must pass on the real matrix, proving the gate is correctly calibrated."""
    rc = main(strict=True, threshold=57, json_out=None)
    assert rc == 0, "strict+threshold=57 must exit 0 on the current matrix (57 gaps)"


def test_strict_high_threshold_exits_zero() -> None:
    """With a very high threshold, strict mode should never fail."""
    rc = main(strict=True, threshold=10_000, json_out=None)
    assert rc == 0, "With threshold=10000, strict mode should always pass"


def test_json_out_creates_file(tmp_path: Path) -> None:
    """--json-out must write a valid JSON file with the required schema keys."""
    out = tmp_path / "coverage.json"
    main(strict=False, threshold=0, json_out=str(out))

    assert out.exists(), "JSON artifact file was not created"

    data = json.loads(out.read_text(encoding="utf-8"))

    # Top-level keys
    assert "generated_at" in data, "Missing 'generated_at'"
    assert "summary" in data, "Missing 'summary'"
    assert "gaps_by_capability" in data, "Missing 'gaps_by_capability'"
    assert "domain_agnostic_capabilities" in data, "Missing 'domain_agnostic_capabilities'"

    # Summary sub-keys
    summary = data["summary"]
    for key in (
        "capabilities",
        "domains",
        "domain_aware_caps",
        "domain_agnostic_caps",
        "explicit_rules",
        "possible_pairs",
        "coverage_pct",
        "gaps",
    ):
        assert key in summary, f"Summary missing key: {key}"

    # Types
    assert isinstance(summary["capabilities"], int)
    assert isinstance(summary["coverage_pct"], (int, float))
    assert isinstance(data["gaps_by_capability"], dict)


def test_json_out_coverage_pct_range(tmp_path: Path) -> None:
    """coverage_pct must be in the range [0, 100]."""
    out = tmp_path / "coverage.json"
    main(strict=False, threshold=0, json_out=str(out))
    data = json.loads(out.read_text(encoding="utf-8"))
    pct = data["summary"]["coverage_pct"]
    assert 0 <= pct <= 100, f"coverage_pct {pct} is out of range [0, 100]"


def test_json_out_generated_at_is_iso8601(tmp_path: Path) -> None:
    """generated_at must be a parseable ISO-8601 timestamp."""
    from datetime import datetime
    out = tmp_path / "coverage.json"
    main(strict=False, threshold=0, json_out=str(out))
    data = json.loads(out.read_text(encoding="utf-8"))
    ts = data["generated_at"]
    # datetime.fromisoformat accepts YYYY-MM-DDTHH:MM:SS+HH:MM in Python 3.7+
    parsed = datetime.fromisoformat(ts)
    assert parsed is not None


def test_json_out_parent_dir_created(tmp_path: Path) -> None:
    """--json-out must create intermediate directories if they don't exist."""
    out = tmp_path / "nested" / "dir" / "coverage.json"
    main(strict=False, threshold=0, json_out=str(out))
    assert out.exists(), "JSON artifact not created when parent dir is missing"


def test_no_json_out_does_not_create_file(tmp_path: Path) -> None:
    """Without --json-out, no JSON file should be written."""
    default_out = tmp_path / "routing-coverage.json"
    main(strict=False, threshold=0, json_out=None)
    assert not default_out.exists(), "JSON file created unexpectedly without --json-out"
