# Reddit r/ChatGPTCoding 推广帖（草稿）

**Title 候选**（选一个，A/B 测）：
- "I transcoded 5 famous Skills to run on Claude Code, Cursor, AND Codex — looking for feedback"
- "Skills shouldn't be locked to one AI agent. Tested it on 5 superpowers skills × 3 platforms"
- "Help me validate: do you actually need cross-platform AI coding skills?"

**推荐标题**：第一个，最具体。

---

## 帖子正文

I've been using both Claude Code and Cursor depending on the task, and every time I find a great Skill (like obra/superpowers' TDD or systematic-debugging), it's locked to one tool. Rewriting them by hand each time is tedious.

So I tried something: I took 5 of the most popular Skills and manually transcoded each to **Claude Code, Cursor, and Codex** formats. One canonical "source" with full metadata, and three drop-in versions that work natively in each tool.

Repo: **https://github.com/<your-handle>/skillhub-seed**

Skills included (4 from obra/superpowers, MIT-attributed; 1 original):
- `tdd-strict` — RED-GREEN-REFACTOR enforcement
- `brainstorming` — Socratic spec design before coding
- `systematic-debugging` — 4-phase root cause analysis
- `code-review` — dispatch a fresh subagent reviewer
- `refactor` — safe structural change with tests-green guarantee

This is **Phase 0 validation** for a larger project (a cross-Harness Skill marketplace called SkillHub). Before I build the actual platform, I want to know:

1. **Do you use Skills today?** Where? Claude Code, Cursor, Codex, Gemini, Copilot, OpenCode?
2. **Have you ever rewritten a Skill for a different tool?** How long did it take?
3. **Would "write once, run everywhere" actually be valuable to you?** Or is the format adaptation too trivial to bother?
4. **What 5 Skills would YOU want cross-platform first?**

Drop a comment, file an Issue, or just star the repo (= vote). I'll listen to feedback for 2 weeks before deciding whether to build the platform.

(Tagging /u/obra — your superpowers work is exactly the kind of content that should be portable. Hope the MIT-attributed transcoding is useful, happy to adjust if not.)

---

## 在 HN 投递的版本（更技术）

**Title:** Show HN: skillhub-seed — 5 AI coding skills, transcoded to 3 agent platforms

**正文：**

Different AI coding agents (Claude Code, Cursor, Codex) all have plugin/skill mechanisms, but the formats are mutually incompatible. Authors duplicate work, users can't carry skills across tools.

I'm validating whether a cross-platform skill marketplace is worth building. As a Phase 0 test, I manually transcoded 5 popular skills (4 derived from obra/superpowers, 1 original) into native formats for Claude Code, Cursor, and Codex.

Repo: **https://github.com/<your-handle>/skillhub-seed**

Each skill has 4 versions:
- `source/SKILL.md` — proposed cross-platform IR (Markdown + YAML frontmatter, mostly Markdown body)
- `claude-code/SKILL.md` — native Anthropic format
- `cursor/<name>.mdc` — native Cursor format with globs/alwaysApply
- `codex/{manifest.toml, SKILL.md}` — TOML manifest + content

The IR draft is in `docs/ir-spec.md`. It's intentionally minimal — Markdown content stays the same, only frontmatter and file structure change per platform.

Looking for feedback on:
- IR field design (what's missing? what's overkill?)
- The "platform_specific" escape hatch — too much or not enough?
- Whether the format adaptation is genuinely useful or just bikeshedding

If 100+ people star or 10+ leave substantive comments in 2 weeks, I'll build the actual platform (CLI + registry + benchmark CI). Otherwise this stays as a useful seed repo and nothing more.

---

## Anthropic Discord（更简短）

> **#showcase**
> 
> Hey folks, I made a small experiment: took 5 famous AI coding Skills (TDD, brainstorming, systematic-debugging, code-review, refactor) and transcoded each to work natively on Claude Code, Cursor, AND Codex. 
> 
> Repo: https://github.com/<your-handle>/skillhub-seed
> 
> Looking for feedback before I decide whether to build a cross-platform Skill marketplace ("SkillHub"). If the cross-tool problem is real for you, please drop a comment in the repo or here. If it's not, that saves me 6 months of building the wrong thing 🙃

---

## 投递时机建议

| 平台 | 时段 (US Eastern) | 备注 |
|---|---|---|
| Reddit r/ChatGPTCoding | 周二/周三 9-11am ET | 工作日早晨流量峰值 |
| Reddit r/cursor | 同上 | 二次发，错开 1 天 |
| HN | 周二 8-10am ET | weekday morning 最佳 |
| Anthropic Discord #showcase | 任何工作日 | 小社区，时段不太敏感 |
| Twitter/X | 周三 11am ET | 最佳工程师活跃度 |

## 跟进 14 天计划

- Day 1：HN + Reddit + Discord 同步发
- Day 2：Twitter / 知乎转发
- Day 3-5：评论区互动，回应每条 substantive 反馈
- Day 7：Reddit r/cursor 二次发
- Day 10：写一篇短 blog 总结到目前为止学到的，发 dev.to / Medium
- Day 14：盘点退出标准（star ≥ 100 ？关键词评论 ≥ 10？）→ 决策 PRD §4.1
