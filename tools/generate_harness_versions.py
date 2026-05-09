#!/usr/bin/env python3
"""Auto-discover and generate harness versions for all skills.

Scans skills/<name>/source/SKILL.md, parses the IR YAML frontmatter, and
generates the 3 Harness-native versions:

    skills/<name>/claude-code/SKILL.md
    skills/<name>/cursor/<name>.mdc
    skills/<name>/codex/SKILL.md
    skills/<name>/codex/manifest.toml

To add a new skill:
    1. mkdir -p skills/<new-name>/{source,claude-code,cursor,codex}
    2. write skills/<new-name>/source/SKILL.md (copy frontmatter from another skill)
    3. python3 tools/generate_harness_versions.py
    4. git add -A && git commit && git push

Usage:
    python3 tools/generate_harness_versions.py            # all skills
    python3 tools/generate_harness_versions.py --skill X  # only skill X
    python3 tools/generate_harness_versions.py --check    # dry-run
    python3 tools/generate_harness_versions.py -v         # verbose

Requires: PyYAML (`pip install pyyaml` or `pip3 install pyyaml`)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

try:
    import yaml
except ImportError:
    print(
        "✗ PyYAML not installed. Run: pip3 install pyyaml\n"
        "  (or: python3 -m pip install --user pyyaml)",
        file=sys.stderr,
    )
    sys.exit(2)

REPO_ROOT = pathlib.Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

# YAML chars that force quoting in plain scalars
_UNSAFE = set(", :#\"'\n[]{}|>&*%@`?!")


def yaml_flow_list(items: list) -> str:
    """Render a list as YAML flow style with minimal quoting.

    >>> yaml_flow_list(["Read", "Write"])
    '[Read, Write]'
    >>> yaml_flow_list(["**/*.test.*"])
    '["**/*.test.*"]'
    >>> yaml_flow_list([])
    '[]'
    """
    if not items:
        return "[]"
    parts = []
    for item in items:
        s = str(item)
        if any(c in _UNSAFE for c in s) or s in ("true", "false", "null", "yes", "no"):
            parts.append('"' + s.replace('"', '\\"') + '"')
        else:
            parts.append(s)
    return "[" + ", ".join(parts) + "]"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split a Markdown file with YAML frontmatter into (meta, body).

    Returns ({}, full_text) if no frontmatter found.
    """
    if not text.startswith("---"):
        return {}, text
    # split into ['', frontmatter, body]
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_text = parts[1]
    body = parts[2]
    try:
        meta = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"YAML parse error: {e}")
    return meta, body.lstrip("\n")


def _platform(meta: dict, harness: str) -> dict:
    return (meta.get("platform_specific") or {}).get(harness) or {}


def _desc(meta: dict, harness: str) -> str:
    """Per-Harness description: platform_specific.<harness>.description if set,
    else fall back to IR top-level description."""
    return _platform(meta, harness).get("description") or meta["description"]


def render_claude_code(meta: dict, body: str) -> str:
    name = meta["name"]
    desc = _desc(meta, "claude-code")
    license_id = meta.get("license", "MIT")
    allowed_tools = _platform(meta, "claude-code").get("allowed_tools")

    lines = [
        "---",
        f"name: {name}",
        f"description: {desc}",
        f"license: {license_id}",
    ]
    if allowed_tools:
        lines.append(f"allowed-tools: {yaml_flow_list(allowed_tools)}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines) + "\n" + body


def render_cursor(meta: dict, body: str) -> str:
    desc = _desc(meta, "cursor")
    triggers = meta.get("triggers") or {}
    cursor_specific = _platform(meta, "cursor")
    globs = cursor_specific.get("globs") or triggers.get("file_patterns") or []
    always_apply = cursor_specific.get(
        "alwaysApply", triggers.get("always_apply", False)
    )

    lines = [
        "---",
        f"description: {desc}",
        f"globs: {yaml_flow_list(globs)}",
        f"alwaysApply: {str(bool(always_apply)).lower()}",
        "---",
        "",
    ]
    return "\n".join(lines) + "\n" + body


def render_codex_md(meta: dict, body: str) -> str:
    lines = [
        "---",
        f"name: {meta['name']}",
        f"description: {_desc(meta, 'codex')}",
        "---",
        "",
    ]
    return "\n".join(lines) + "\n" + body


def render_codex_toml(meta: dict) -> str:
    """Generate Codex plugin manifest.toml.

    Permissions are derived from claude-code allowed_tools as a heuristic;
    each skill's source/SKILL.md can override via platform_specific.codex.
    """
    triggers = meta.get("triggers") or {}
    keywords = triggers.get("keywords", []) or []
    file_patterns = triggers.get("file_patterns", []) or []
    always_apply = bool(triggers.get("always_apply", False))

    cc_tools = set(_platform(meta, "claude-code").get("allowed_tools", []) or [])
    codex_specific = _platform(meta, "codex")

    can_read = codex_specific.get("read", "Read" in cc_tools or True)
    can_edit = codex_specific.get(
        "edit", "Edit" in cc_tools or "Write" in cc_tools
    )
    has_bash = "Bash" in cc_tools or "Grep" in cc_tools
    # Shell access depends on Bash, not Edit — read-only verification skills
    # (e.g. running tests/lint) legitimately need shell without write.
    shell_default = (
        ["npm test", "pytest", "go test", "cargo test", "git", "grep"]
        if has_bash
        else []
    )
    shell = codex_specific.get("shell", shell_default)

    trigger_lines = [
        "[triggers]",
        f"keywords = {json.dumps(keywords, ensure_ascii=False)}",
    ]
    if file_patterns:
        trigger_lines.append(
            f"file_patterns = {json.dumps(file_patterns, ensure_ascii=False)}"
        )
    trigger_lines.append(f"always_apply = {str(always_apply).lower()}")

    lines = [
        "[plugin]",
        f'name = "{meta["name"]}"',
        f'version = "{meta.get("version", "1.0.0")}"',
        f'description = "{_desc(meta, "codex")}"',
        f'license = "{meta.get("license", "MIT")}"',
        'authors = ["SkillHub contributors"]',
        "",
        *trigger_lines,
        "",
        "[permissions]",
        f"read = {str(bool(can_read)).lower()}",
        f"edit = {str(bool(can_edit)).lower()}",
        f"shell = {json.dumps(shell, ensure_ascii=False)}",
        "",
        "[content]",
        'file = "SKILL.md"',
    ]
    return "\n".join(lines) + "\n"


def discover_skills() -> list[pathlib.Path]:
    """Return sorted list of skill directories that have source/SKILL.md."""
    if not SKILLS_DIR.is_dir():
        return []
    return sorted(
        d for d in SKILLS_DIR.iterdir()
        if d.is_dir() and (d / "source" / "SKILL.md").is_file()
    )


def process_skill(
    skill_dir: pathlib.Path, *, check: bool = False, verbose: bool = False
) -> dict:
    src = skill_dir / "source" / "SKILL.md"
    raw = src.read_text(encoding="utf-8")
    try:
        meta, body = parse_frontmatter(raw)
    except ValueError as e:
        return {"error": str(e), "path": str(src)}
    if not meta or "name" not in meta:
        return {"error": "missing required field 'name' in frontmatter", "path": str(src)}

    name = meta["name"]
    targets = [
        (skill_dir / "claude-code" / "SKILL.md", render_claude_code(meta, body)),
        (skill_dir / "cursor" / f"{name}.mdc", render_cursor(meta, body)),
        (skill_dir / "codex" / "SKILL.md", render_codex_md(meta, body)),
        (skill_dir / "codex" / "manifest.toml", render_codex_toml(meta)),
    ]

    written = 0
    unchanged = 0
    for path, content in targets:
        existing = path.read_text(encoding="utf-8") if path.exists() else None
        if existing == content:
            unchanged += 1
            if verbose:
                print(f"    = {path.relative_to(REPO_ROOT)}")
            continue
        if check:
            written += 1
            if verbose:
                action = "create" if existing is None else "update"
                print(f"    ~ would {action}: {path.relative_to(REPO_ROOT)}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written += 1
        if verbose:
            action = "wrote" if existing is None else "updated"
            print(f"    + {action}: {path.relative_to(REPO_ROOT)}")

    return {"name": name, "written": written, "unchanged": unchanged}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--skill", help="Only process one skill (by directory name)")
    p.add_argument("--check", action="store_true", help="Dry-run; don't write any files")
    p.add_argument("-v", "--verbose", action="store_true", help="Show per-file actions")
    args = p.parse_args()

    if args.skill:
        d = SKILLS_DIR / args.skill
        if not (d / "source" / "SKILL.md").is_file():
            print(f"✗ skill not found or missing source/SKILL.md: {args.skill}", file=sys.stderr)
            return 1
        skill_dirs = [d]
    else:
        skill_dirs = discover_skills()
        if not skill_dirs:
            print("✗ no skills found under skills/*/source/SKILL.md", file=sys.stderr)
            return 1

    errors = 0
    total_written = 0
    total_unchanged = 0
    for d in skill_dirs:
        result = process_skill(d, check=args.check, verbose=args.verbose)
        if "error" in result:
            print(f"✗ {d.name}: {result['error']}", file=sys.stderr)
            errors += 1
            continue
        verb = "would write" if args.check else "wrote"
        print(
            f"{'~' if args.check else '✓'} {result['name']}: "
            f"{result['written']} {verb}, {result['unchanged']} unchanged"
        )
        total_written += result["written"]
        total_unchanged += result["unchanged"]

    print(
        f"\nSummary: {len(skill_dirs)} skill(s), "
        f"{total_written} {'would write' if args.check else 'written'}, "
        f"{total_unchanged} unchanged, {errors} error(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
