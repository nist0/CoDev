from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import re
import sys
import yaml


ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / ".github" / "agents"
PROMPTS_DIR = ROOT / ".github" / "prompts"
SKILLS_DIR = ROOT / ".github" / "skills"
INSTRUCTIONS_DIR = ROOT / ".github" / "instructions"
ROUTING_DIR = ROOT / "routing"
REVIEWER_AGENT = AGENTS_DIR / "reviewer.agent.md"

# Frontmatter attribute allowlists — sourced from VS Code Copilot official docs (2026-03-04)
# https://code.visualstudio.com/docs/copilot/customization/prompt-files
# https://code.visualstudio.com/docs/copilot/customization/custom-agents
# https://code.visualstudio.com/docs/copilot/customization/agent-skills
# https://code.visualstudio.com/docs/copilot/customization/custom-instructions
ALLOWED_ATTRS: dict[str, set[str]] = {
    "prompt": {"description", "name", "argument-hint", "agent", "model", "tools"},
    "agent": {
        "description", "name", "argument-hint", "tools", "agents", "model",
        "user-invocable", "disable-model-invocation", "target", "mcp-servers", "handoffs",
    },
    "skill": {"name", "description", "argument-hint", "user-invocable", "disable-model-invocation"},
    "instruction": {"name", "description", "applyTo"},
}
DEPRECATED_ATTRS: dict[str, dict[str, str]] = {
    "prompt": {"mode": "use 'agent: ask|agent|plan' instead", "skills": "reference skills in the prompt body"},
    "agent": {"infer": "use 'user-invocable' and 'disable-model-invocation' instead"},
    "skill": {"user-invokable": "use 'user-invocable' instead"},
    "instruction": {},
}


FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass
class ValidationContext:
    errors: list[str]

    def add(self, message: str) -> None:
        self.errors.append(message)


def build_recovery_actions(errors: list[str]) -> list[str]:
    actions: list[str] = []
    if any(
        marker in error
        for error in errors
        for marker in ("frontmatter", "reviewer agent", "missing SKILL.md")
    ):
        actions.append(
            "Review .github/agents/, .github/prompts/, .github/skills/*/SKILL.md, and .github/instructions/ for the referenced frontmatter or contract issue."
        )
    if any(
        marker in error
        for error in errors
        for marker in ("routing rule", "capability references", "aliases references")
    ):
        actions.append(
            "Review routing/matrix.yaml, routing/capabilities.yaml, routing/aliases.yaml, and routing/domains.yaml for the referenced ID mismatch."
        )
    actions.append("Re-run: python scripts/validate-customization-registry.py")
    actions.append("Optional overview: python scripts/codev-dev.py doctor --validators registry")
    return actions


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return {}

    block = match.group(1)
    try:
        data = yaml.safe_load(block)
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        # Fallback for loose frontmatter patterns (for example unquoted ':' in values).
        fallback: dict[str, Any] = {}
        for line in block.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip("\"").strip("'")
            if key:
                fallback[key] = value
        return fallback


def assert_unique(values: list[str], context: ValidationContext, label: str) -> None:
    counts: dict[str, int] = {}
    for value in values:
        key = value.strip().lower()
        counts[key] = counts.get(key, 0) + 1

    for key, count in counts.items():
        if count > 1:
            context.add(f"duplicate {label}: '{key}' appears {count} times")


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data if isinstance(data, dict) else {}


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def validate_registry(context: ValidationContext) -> None:
    agent_files = sorted(AGENTS_DIR.glob("*.agent.md"))
    prompt_files = sorted(PROMPTS_DIR.glob("*.prompt.md"))
    instruction_files = sorted(INSTRUCTIONS_DIR.glob("*.instructions.md"))
    skill_dirs = sorted([path for path in SKILLS_DIR.iterdir() if path.is_dir()])

    agent_names: list[str] = []
    prompt_ids: list[str] = []
    instruction_names: list[str] = []
    skill_ids: list[str] = []

    for path in agent_files:
        frontmatter = parse_frontmatter(path)
        name = str(frontmatter.get("name", "")).strip()
        if not name:
            context.add(f"missing frontmatter name in agent file: {display_path(path)}")
        else:
            agent_names.append(name)

    for path in prompt_files:
        frontmatter = parse_frontmatter(path)
        name = str(frontmatter.get("name", "")).strip()
        prompt_id = name if name else path.name.removesuffix(".prompt.md")
        prompt_ids.append(prompt_id)

    for path in instruction_files:
        frontmatter = parse_frontmatter(path)
        name = str(frontmatter.get("name", "")).strip()
        if not name:
            # security.instructions.md intentionally has no name in this repo
            if path.name != "security.instructions.md":
                context.add(f"missing frontmatter name in instruction file: {display_path(path)}")
        else:
            instruction_names.append(name)

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            context.add(f"missing SKILL.md in skill directory: {skill_dir.relative_to(ROOT)}")
            continue

        frontmatter = parse_frontmatter(skill_md)
        name = str(frontmatter.get("name", "")).strip()
        skill_id = name if name else skill_dir.name
        skill_ids.append(skill_id)
        if name and name != skill_dir.name:
            context.add(
                "skill name mismatch: "
                f"{display_path(skill_md)} frontmatter name '{name}' != folder '{skill_dir.name}'"
            )

    assert_unique(agent_names, context, "agent name")
    assert_unique(prompt_ids, context, "prompt id")
    assert_unique(instruction_names, context, "instruction name")
    assert_unique(skill_ids, context, "skill id")


def validate_routing_references(context: ValidationContext) -> None:
    capabilities_doc = read_yaml(ROUTING_DIR / "capabilities.yaml")
    aliases_doc = read_yaml(ROUTING_DIR / "aliases.yaml")
    domains_doc = read_yaml(ROUTING_DIR / "domains.yaml")
    matrix_doc = read_yaml(ROUTING_DIR / "matrix.yaml")

    capabilities = capabilities_doc.get("capabilities", [])
    domains = domains_doc.get("domains", [])
    aliases = aliases_doc.get("aliases", {})
    rules = matrix_doc.get("routing_rules", [])

    capability_ids = [str(item.get("id", "")).strip() for item in capabilities if isinstance(item, dict)]
    domain_ids = [str(item.get("id", "")).strip() for item in domains if isinstance(item, dict)]

    assert_unique(capability_ids, context, "capability id")
    assert_unique(domain_ids, context, "domain id")

    capability_set = {cid for cid in capability_ids if cid}
    domain_set = {did for did in domain_ids if did}

    prompt_name_set: set[str] = set()
    agent_name_set: set[str] = set()

    for path in AGENTS_DIR.glob("*.agent.md"):
        frontmatter = parse_frontmatter(path)
        name = str(frontmatter.get("name", "")).strip()
        if name:
            agent_name_set.add(name)

    for path in PROMPTS_DIR.glob("*.prompt.md"):
        frontmatter = parse_frontmatter(path)
        name = str(frontmatter.get("name", "")).strip()
        prompt_name_set.add(name if name else path.name.removesuffix(".prompt.md"))

        prompt_agent = str(frontmatter.get("agent", "")).strip()
        if prompt_agent and prompt_agent not in agent_name_set:
            context.add(
                "prompt references unknown agent: "
                f"{path.relative_to(ROOT)} -> {prompt_agent}"
            )

    for item in capabilities:
        if not isinstance(item, dict):
            continue
        default_agent = str(item.get("default_agent", "")).strip()
        capability_id = str(item.get("id", "")).strip() or "<unknown-capability>"
        if default_agent and default_agent not in agent_name_set:
            context.add(
                "capability references unknown default agent: "
                f"{capability_id} -> {default_agent}"
            )
    skill_set = {path.name for path in SKILLS_DIR.iterdir() if path.is_dir()}

    for alias_capability in aliases.keys():
        if alias_capability not in capability_set:
            context.add(f"aliases references unknown capability: {alias_capability}")

    for index, rule in enumerate(rules, start=1):
        if not isinstance(rule, dict):
            context.add(f"routing rule #{index} is not a mapping")
            continue

        when = rule.get("when", {})
        suggest = rule.get("suggest", {})

        capability = when.get("capability")
        domain = when.get("domain")

        if capability and capability not in capability_set:
            context.add(f"routing rule #{index} references unknown capability: {capability}")

        if domain and domain not in domain_set:
            context.add(f"routing rule #{index} references unknown domain: {domain}")

        suggested_agent = str(suggest.get("agent", "")).strip()
        if suggested_agent and suggested_agent not in agent_name_set:
            context.add(
                f"routing rule #{index} references unknown agent: {suggested_agent}"
            )

        for prompt_name in suggest.get("prompts", []) or []:
            if prompt_name not in prompt_name_set:
                context.add(f"routing rule #{index} references unknown prompt: {prompt_name}")

        for skill_name in suggest.get("skills", []) or []:
            if skill_name not in skill_set:
                context.add(f"routing rule #{index} references unknown skill: {skill_name}")


def validate_frontmatter_attributes(context: ValidationContext) -> None:
    """Ensure all frontmatter keys are on the official VS Code Copilot allowlist."""
    checks: list[tuple[Path, str]] = (
        [(p, "prompt") for p in sorted(PROMPTS_DIR.glob("*.prompt.md"))]
        + [(p, "agent") for p in sorted(AGENTS_DIR.glob("*.agent.md"))]
        + [(skill_dir / "SKILL.md", "skill") for skill_dir in sorted(SKILLS_DIR.iterdir())
           if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists()]
        + [(p, "instruction") for p in sorted(INSTRUCTIONS_DIR.glob("*.instructions.md"))]
    )
    for path, ftype in checks:
        keys = set(parse_frontmatter(path).keys())
        allowed = ALLOWED_ATTRS.get(ftype, set())
        deprecated = DEPRECATED_ATTRS.get(ftype, {})
        for key in sorted(keys):
            if key in deprecated:
                context.add(
                    f"deprecated frontmatter attribute '{key}' in {path.relative_to(ROOT)} "
                    f"({deprecated[key]})"
                )
            elif key not in allowed:
                context.add(
                    f"unknown frontmatter attribute '{key}' in {display_path(path)} "
                    f"(allowed for {ftype}: {sorted(allowed)})"
                )


def validate_structure_contracts(context: ValidationContext) -> None:
    for path in sorted(PROMPTS_DIR.glob("*.prompt.md")):
        frontmatter = parse_frontmatter(path)
        description = str(frontmatter.get("description", "")).strip()
        if not description:
            context.add(f"prompt missing required description: {display_path(path)}")

        tools = frontmatter.get("tools")
        if isinstance(tools, list) and not tools:
            context.add(
                f"prompt uses empty tools override: {display_path(path)} (omit 'tools:' to inherit agent tools)"
            )

    for path in sorted(AGENTS_DIR.glob("*.agent.md")):
        frontmatter = parse_frontmatter(path)
        description = str(frontmatter.get("description", "")).strip()
        if not description:
            context.add(f"agent missing required description: {display_path(path)}")

        agents = frontmatter.get("agents")
        tools = frontmatter.get("tools")
        if isinstance(tools, list) and not tools:
            context.add(
                f"agent uses empty tools override: {display_path(path)} (omit 'tools:' unless the agent explicitly needs tools)"
            )
        if not isinstance(agents, list) or not agents:
            continue

        normalized_tools: set[str] = set()
        if isinstance(tools, str):
            normalized_tools = {tools.strip().lower()}
        elif isinstance(tools, list):
            normalized_tools = {str(tool).strip().lower() for tool in tools}
        else:
            normalized_tools = set()

        if normalized_tools and "agent" not in normalized_tools:
            context.add(
                f"agent declares subagents without agent tool: {display_path(path)}"
            )

def validate_reviewer_agent_contract(context: ValidationContext) -> None:
    if not REVIEWER_AGENT.exists():
        context.add(f"missing reviewer agent file: {display_path(REVIEWER_AGENT)}")
        return

    frontmatter = parse_frontmatter(REVIEWER_AGENT)
    tools = frontmatter.get("tools", [])
    if isinstance(tools, str):
        tools = [tools]
    if not isinstance(tools, list):
        context.add("reviewer agent frontmatter 'tools' must be a list")
        tools = []

    normalized_tools = {str(tool).strip().lower() for tool in tools}
    if "search/codebase" not in normalized_tools:
        context.add("reviewer agent must include 'search/codebase' in frontmatter tools")

    text = REVIEWER_AGENT.read_text(encoding="utf-8").lower()
    required_markers = ["instructions", "skills", "verdict"]
    for marker in required_markers:
        if marker not in text:
            context.add(f"reviewer agent missing required marker: {marker}")

    if "#search/codebase" not in text and "#codebase" not in text:
        context.add("reviewer agent missing required marker: #search/codebase")


def main() -> int:
    context = ValidationContext(errors=[])
    validate_registry(context)
    validate_frontmatter_attributes(context)
    validate_structure_contracts(context)
    validate_routing_references(context)
    validate_reviewer_agent_contract(context)

    if context.errors:
        print("Customization registry validation failed:")
        for error in context.errors:
            print(f" - {error}")
        print("Next actions:")
        for action in build_recovery_actions(context.errors):
            print(f" - {action}")
        return 1

    print("Customization registry validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
