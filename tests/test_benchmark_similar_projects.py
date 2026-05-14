from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "benchmark-similar-projects.py"


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


benchmark = _load_module("benchmark_similar_projects", SCRIPT)


def test_weighted_score_is_capped_and_weighted() -> None:
    project = {
        "full_name": "example/repo",
        "signals": {
            "community": 10,
            "maintenance": 8,
            "documentation": 7,
            "architecture": 6,
            "quality_gates": 5,
            "extensibility": 4,
            "testing": 3,
        },
    }
    score, breakdown = benchmark.weighted_score(project, benchmark.DEFAULT_RUBRIC_WEIGHTS)

    assert breakdown["community"] == 10
    assert breakdown["testing"] == 3
    assert score == 66


def test_select_top_projects_dedupes_and_orders() -> None:
    projects = [
        {"full_name": "b/proj", "stargazers_count": 10},
        {"full_name": "a/proj", "stargazers_count": 10},
        {"full_name": "b/proj", "stargazers_count": 15},
        {"full_name": "c/proj", "stargazers_count": 9},
    ]

    selected = benchmark.select_top_projects(projects, top_count=2)

    assert len(selected) == 2
    assert selected[0]["full_name"] == "b/proj"
    assert selected[0]["stargazers_count"] == 15
    assert selected[1]["full_name"] == "a/proj"


def test_score_projects_orders_by_score_then_stars() -> None:
    projects = [
        {
            "full_name": "a/proj",
            "stargazers_count": 50,
            "signals": {k: 7 for k in benchmark.DEFAULT_RUBRIC_WEIGHTS},
        },
        {
            "full_name": "b/proj",
            "stargazers_count": 5,
            "signals": {k: 9 for k in benchmark.DEFAULT_RUBRIC_WEIGHTS},
        },
    ]

    ranked = benchmark.score_projects(projects, benchmark.DEFAULT_RUBRIC_WEIGHTS)

    assert ranked[0]["full_name"] == "b/proj"
    assert ranked[0]["score"] > ranked[1]["score"]


def test_render_markdown_report_contains_required_sections() -> None:
    report = {
        "mode": "baseline",
        "top_count": 1,
        "query": "copilot",
        "weights": benchmark.DEFAULT_RUBRIC_WEIGHTS,
        "projects": [
            {
                "full_name": "x/y",
                "score": 88,
                "stargazers_count": 100,
                "description": "Sample repo",
            }
        ],
        "clone_actions": ["dry-run clone --depth 1 https://github.com/x/y.git -> external/x__y"],
    }

    markdown = benchmark.render_markdown_report(report)

    assert "# Competitive benchmark report" in markdown
    assert "## Weighted rubric" in markdown
    assert "## Ranked projects" in markdown
    assert "| 1 | x/y | 88 | 100 | Sample repo |" in markdown
    assert "## Rerun" in markdown


def test_build_json_report_preserves_core_fields() -> None:
    payload = benchmark.build_json_report(
        mode="manual",
        query="x",
        top_count=3,
        weights=benchmark.DEFAULT_RUBRIC_WEIGHTS,
        projects=[{"full_name": "x/y", "score": 12}],
        clone_actions=["skip existing"],
    )

    assert payload["mode"] == "manual"
    assert payload["top_count"] == 3
    assert payload["projects"][0]["full_name"] == "x/y"
    assert payload["clone_actions"][0] == "skip existing"
    assert "generated_at" in payload


def test_clone_projects_dry_run_does_not_create_clone_dir(tmp_path: Path) -> None:
    clone_dir = tmp_path / "clones"
    projects = [
        {
            "full_name": "owner/repo",
            "clone_url": "https://github.com/owner/repo.git",
        }
    ]

    actions = benchmark.clone_projects(projects, clone_dir, dry_run=True)

    assert not clone_dir.exists()
    assert len(actions) == 1
    assert "dry-run clone --depth 1 https://github.com/owner/repo.git" in actions[0]


def test_main_auto_mode_gh_failure_warns_and_falls_back_to_baseline(capsys: Any, monkeypatch: Any) -> None:
    args = argparse.Namespace(
        top_count=3,
        clone_dir="external",
        markdown_output="reports/out.md",
        json_output="reports/out.json",
        input_file=None,
        mode="auto",
        query="copilot framework prompts agents routing",
        dry_run=True,
        no_clone=True,
    )

    def _boom(query: str, limit: int) -> list[dict[str, Any]]:
        raise RuntimeError("gh unavailable for test")

    monkeypatch.setattr(benchmark, "parse_args", lambda: args)
    monkeypatch.setattr(benchmark, "discover_projects_via_gh", _boom)

    exit_code = benchmark.main()
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Warning: auto mode fallback to baseline because gh failed: gh unavailable for test" in output
    assert "Discovery mode: baseline" in output