---
# === SkillHub IR ===
name: brainstorming
version: 1.0.0
description: You MUST use this before any creative work — creating features, building components, adding functionality. Explores user intent before implementation.
description_zh: 任何创造性工作前先用：通过对话把模糊想法变成 spec，避免假设。

license: MIT
author:
  name: Jesse Vincent
upstream:
  source: github.com/obra/superpowers/skills/brainstorming
  license: MIT

triggers:
  keywords: ["new feature", "build", "design", "想法", "新功能"]
  file_patterns: []
  always_apply: false

compatibility:
  claude-code: ">=2.0"
  cursor: ">=0.40"
  codex: ">=1.5"
  gemini: false
  copilot: false
  opencode: false

tags: [design, spec, methodology, socratic]
category: design
maturity: stable

platform_specific:
  claude-code:
    allowed_tools: [Read, Write]
  cursor:
    description: "Brainstorm: turn ideas into approved spec via Socratic dialogue before any implementation"
  codex:
    description: Use before any creative work to turn ideas into approved spec
---

# Brainstorming — Ideas → Designs

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

## HARD GATE

> **Do NOT** invoke any implementation skill, write any code, scaffold any project, or take any implementation action **until** you have presented a design and the user has approved it.

This applies to **every** project, no matter how simple it seems.

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences), but you MUST present it and get approval.

## Process

You MUST complete each step in order:

1. **Explore project context** — check files, docs, recent commits
2. **Ask clarifying questions** — one at a time. Understand purpose / constraints / success criteria
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design** — in sections scaled to complexity. Get user approval after each section
5. **Write design doc** — save to `docs/specs/YYYY-MM-DD-<topic>-design.md` and commit
6. **Self-review** — scan for placeholders, contradictions, ambiguity, scope
7. **User reviews written spec** — wait for explicit approval
8. **Transition to implementation** — invoke writing-plans skill (and only that)

## Asking Questions

- **One question per message** — don't overwhelm
- **Multiple choice preferred** when possible (easier to answer than open-ended)
- Focus: purpose, constraints, success criteria
- If the request describes multiple subsystems (e.g., "build a platform with chat + storage + billing"), flag this and decompose first — don't refine details of a project that needs splitting

## Proposing Approaches

- 2-3 approaches with trade-offs
- Lead with your recommended option and why
- Conversational, not RFC-style

## Presenting Design

Cover: **architecture, components, data flow, error handling, testing**. Each section scaled to its complexity (a few sentences ~ 200-300 words). Ask after each section "looks right so far?"

## Design for Isolation and Clarity

- Break the system into smaller units, each with one clear purpose
- Each unit answers: what does it do, how do you use it, what does it depend on
- If you can't change internals without breaking consumers, the boundaries need work
- Smaller well-bounded units = easier for the agent to reason about

## In Existing Codebases

- Explore current structure first, follow existing patterns
- Where existing code has problems that affect this work, include targeted improvements
- Don't propose unrelated refactoring — stay focused on the current goal

## Self-Review Checklist

After writing the spec, with fresh eyes:

1. **Placeholders** — any TBD/TODO/incomplete sections? Fix them
2. **Internal consistency** — sections contradicting each other? Architecture matching feature descriptions?
3. **Scope** — focused enough for one plan? Or needs decomposition?
4. **Ambiguity** — any requirement interpretable two ways? Pick one, make it explicit

Fix inline. No re-review — just fix and move on.

## User Review Gate

After self-review:

> "Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start writing out the implementation plan."

Wait for the response. If they request changes, make them and re-run self-review. Only proceed once approved.

## Key Principles

- **YAGNI ruthlessly** — remove unnecessary features from all designs
- **Explore alternatives** — always 2-3 approaches before settling
- **Incremental validation** — present design, get approval, move on
- **Be flexible** — go back and clarify when something doesn't make sense

---

> **Source:** Adapted from [obra/superpowers brainstorming](https://github.com/obra/superpowers/tree/main/skills/brainstorming) (MIT, © Jesse Vincent and contributors). Visual companion section omitted; see upstream for browser-based mockup support.
