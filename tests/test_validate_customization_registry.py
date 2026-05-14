from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    sys.modules[name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


registry = _load_module(
    "validate_customization_registry",
    ROOT / "scripts" / "validate-customization-registry.py",
)


def test_validate_structure_contracts_flags_empty_prompt_tools(tmp_path: Path, monkeypatch) -> None:
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "bad.prompt.md").write_text(
        "---\n"
        'name: bad\n'
        'description: "Test prompt."\n'
        "tools: []\n"
        "---\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(registry, "PROMPTS_DIR", prompts_dir)
    monkeypatch.setattr(registry, "AGENTS_DIR", tmp_path / "agents")
    monkeypatch.setattr(registry, "INSTRUCTIONS_DIR", tmp_path / "instructions")
    (tmp_path / "agents").mkdir()
    (tmp_path / "instructions").mkdir()

    context = registry.ValidationContext(errors=[])
    registry.validate_structure_contracts(context)

    assert any("prompt uses empty tools override" in error for error in context.errors)


def test_validate_structure_contracts_flags_missing_agent_tool_for_subagents(tmp_path: Path, monkeypatch) -> None:
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    (agents_dir / "bad.agent.md").write_text(
        "---\n"
        'name: bad-agent\n'
        'description: "Test agent."\n'
        "tools:\n"
        "  - search/codebase\n"
        "agents:\n"
        "  - reviewer\n"
        "---\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(registry, "PROMPTS_DIR", tmp_path / "prompts")
    monkeypatch.setattr(registry, "AGENTS_DIR", agents_dir)
    monkeypatch.setattr(registry, "INSTRUCTIONS_DIR", tmp_path / "instructions")
    (tmp_path / "prompts").mkdir()
    (tmp_path / "instructions").mkdir()

    context = registry.ValidationContext(errors=[])
    registry.validate_structure_contracts(context)

    assert any("agent declares subagents without agent tool" in error for error in context.errors)


def test_validate_structure_contracts_flags_missing_instruction_apply_to(tmp_path: Path, monkeypatch) -> None:
    instructions_dir = tmp_path / "instructions"
    instructions_dir.mkdir()
    (instructions_dir / "bad.instructions.md").write_text(
        "---\n"
        'name: bad-instruction\n'
        'description: "Test instruction."\n'
        "---\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(registry, "PROMPTS_DIR", tmp_path / "prompts")
    monkeypatch.setattr(registry, "AGENTS_DIR", tmp_path / "agents")
    monkeypatch.setattr(registry, "INSTRUCTIONS_DIR", instructions_dir)
    (tmp_path / "prompts").mkdir()
    (tmp_path / "agents").mkdir()

    context = registry.ValidationContext(errors=[])
    registry.validate_structure_contracts(context)

    assert any("instruction missing required applyTo" in error for error in context.errors)