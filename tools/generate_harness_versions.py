#!/usr/bin/env python3
"""Generate 3 harness versions for each of 4 remaining skills.
Strips IR frontmatter from source/SKILL.md and prepends harness-specific frontmatter.
"""
import pathlib

SEED = pathlib.Path("/Users/zhangshanshan/skillhub-seed/skills")

# (dir_name, file_name, claude_desc, cursor_desc, codex_desc, allowed_tools, globs, keywords)
SKILLS = [
    {
        "dir": "brainstorming",
        "name": "brainstorming",
        "claude_desc": "You MUST use this before any creative work — creating features, building components, adding functionality. Explores user intent before implementation.",
        "cursor_desc": "Brainstorm: turn ideas into approved spec via Socratic dialogue before any implementation",
        "codex_desc": "Use before any creative work to turn ideas into approved spec",
        "allowed_tools": "Read, Write",
        "globs": "[]",
        "keywords": '["new feature", "build", "design", "想法", "新功能"]',
        "permissions_read": True,
        "permissions_edit": False,
    },
    {
        "dir": "systematic-debugging",
        "name": "systematic-debugging",
        "claude_desc": "Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes. 4-phase root cause process.",
        "cursor_desc": "Systematic debugging: 4-phase root cause process before any fix",
        "codex_desc": "Use for any bug/test failure before proposing fixes",
        "allowed_tools": "Read, Edit, Bash, Grep",
        "globs": "[]",
        "keywords": '["bug", "debug", "error", "test failure", "调试", "排查"]',
        "permissions_read": True,
        "permissions_edit": True,
    },
    {
        "dir": "code-review",
        "name": "code-review",
        "claude_desc": "Use when completing tasks, implementing major features, or before merging to verify work meets requirements. Dispatch a fresh subagent reviewer.",
        "cursor_desc": "Dispatch a code reviewer subagent with crafted context (not session history)",
        "codex_desc": "Code review: dispatch a fresh subagent reviewer before merge",
        "allowed_tools": "Read, Bash",
        "globs": "[]",
        "keywords": '["review", "merge", "PR", "审查"]',
        "permissions_read": True,
        "permissions_edit": False,
    },
    {
        "dir": "refactor",
        "name": "refactor",
        "claude_desc": "Use when changing code structure without changing behavior. Keeps tests green, makes one structural change at a time, defers premature abstractions.",
        "cursor_desc": "Refactor: structural change without behavior change. One smell, one move, tests green throughout",
        "codex_desc": "Refactor without behavior change. One step at a time, tests green",
        "allowed_tools": "Read, Edit, Bash, Grep",
        "globs": "[]",
        "keywords": '["refactor", "rename", "extract", "restructure", "重构"]',
        "permissions_read": True,
        "permissions_edit": True,
    },
]


def strip_ir_frontmatter(text: str) -> str:
    """Remove the leading YAML frontmatter block (--- ... ---) and return body."""
    parts = text.split("---", 2)
    return parts[2].lstrip() if len(parts) >= 3 else text


def main():
    for s in SKILLS:
        src = SEED / s["dir"] / "source" / "SKILL.md"
        body = strip_ir_frontmatter(src.read_text())

        # claude-code
        claude_fm = (
            f"---\n"
            f"name: {s['name']}\n"
            f"description: {s['claude_desc']}\n"
            f"license: MIT\n"
            f"allowed-tools: [{s['allowed_tools']}]\n"
            f"---\n\n"
        )
        (SEED / s["dir"] / "claude-code" / "SKILL.md").write_text(claude_fm + body)

        # cursor
        cursor_fm = (
            f"---\n"
            f"description: {s['cursor_desc']}\n"
            f"globs: {s['globs']}\n"
            f"alwaysApply: false\n"
            f"---\n\n"
        )
        (SEED / s["dir"] / "cursor" / f"{s['name']}.mdc").write_text(cursor_fm + body)

        # codex SKILL.md
        codex_md_fm = (
            f"---\n"
            f"name: {s['name']}\n"
            f"description: {s['codex_desc']}\n"
            f"---\n\n"
        )
        (SEED / s["dir"] / "codex" / "SKILL.md").write_text(codex_md_fm + body)

        # codex manifest.toml
        shell_perms = (
            '["npm test", "pytest", "go test", "cargo test", "git", "grep"]'
            if s["permissions_edit"]
            else "[]"
        )
        toml = (
            f'[plugin]\n'
            f'name = "{s["name"]}"\n'
            f'version = "1.0.0"\n'
            f'description = "{s["codex_desc"]}"\n'
            f'license = "MIT"\n'
            f'authors = ["SkillHub contributors"]\n'
            f'\n'
            f'[triggers]\n'
            f'keywords = {s["keywords"]}\n'
            f'always_apply = false\n'
            f'\n'
            f'[permissions]\n'
            f'read = {str(s["permissions_read"]).lower()}\n'
            f'edit = {str(s["permissions_edit"]).lower()}\n'
            f'shell = {shell_perms}\n'
            f'\n'
            f'[content]\n'
            f'file = "SKILL.md"\n'
        )
        (SEED / s["dir"] / "codex" / "manifest.toml").write_text(toml)

        print(f"✓ {s['dir']}: 4 files generated")


if __name__ == "__main__":
    main()
