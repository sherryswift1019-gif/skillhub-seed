# skillhub-seed

> **Phase 0 验证仓库** — 5 个明星 AI Coding Skill，跨 3 个主流 Harness（Claude Code / Cursor / Codex）手工转译。
>
> 用来验证 [SkillHub 项目](https://github.com/sherryswift1019-gif/skillhub)（跨平台 AI Coding Skill 公共市场）的核心假设：开发者真的需要"写一次跑遍所有 Harness"吗？

## TL;DR

**问题**：你写的 AI Coding Skill 只能在一个 Harness 上跑。换工具就要重写。

**示范**：本仓库把 5 个 superpowers 明星 Skill 转译到 Claude Code / Cursor / Codex 三平台，每个版本都能直接装上用。

**目的**：测试需求 — 如果你想在其他 Harness 上看到这些 Skill，请到 [Discussions](https://github.com/sherryswift1019-gif/skillhub-seed/discussions) 留言/给 Issue / star 仓库。

---

## 收录的 Skill

| Skill | 来源 | 用途 |
|---|---|---|
| `tdd-strict` | obra/superpowers (MIT) | 强制 RED-GREEN-REFACTOR TDD 流程 |
| `brainstorming` | obra/superpowers (MIT) | 用 Socratic 对话把模糊想法变成 spec |
| `systematic-debugging` | obra/superpowers (MIT) | 4 阶段根因分析，避免 patch-and-pray |
| `code-review` | obra/superpowers (MIT) | 派子 agent 做严格代码审查 |
| `verification-before-completion` | obra/superpowers (MIT) | 在声称完成/通过前必须跑验证命令 |
| `refactor` | 本仓库原创 (MIT) | 在保持测试绿的前提下安全重构 |

---

## 仓库结构

```
skills/
└── <skill-name>/
    ├── source/SKILL.md          # SkillHub IR (中间表示，含全字段 frontmatter)
    ├── claude-code/SKILL.md     # Claude Code 原生格式
    ├── cursor/<name>.mdc        # Cursor .mdc 格式
    └── codex/
        ├── manifest.toml        # Codex plugin manifest
        └── SKILL.md             # 内容
docs/
└── ir-spec.md                   # IR 字段规范草稿
promo/                           # 推广文案草稿
tools/                           # （Phase 1 才会有 build 脚本）
```

---

## 怎么用

### Claude Code 用户

```bash
# 把某个 skill 复制到本地
cp -r skills/tdd-strict/claude-code ~/.claude/skills/tdd-strict
# 重启 Claude Code 或运行 /reload-plugins
```

### Cursor 用户

```bash
# 在你的项目根目录
mkdir -p .cursor/rules
cp skills/tdd-strict/cursor/tdd-strict.mdc .cursor/rules/
```

### Codex 用户

```bash
mkdir -p ~/.codex/plugins/tdd-strict
cp skills/tdd-strict/codex/* ~/.codex/plugins/tdd-strict/
```

---

## 我们想知道的

1. 你同时用几个 AI Coding Agent？
2. 你写过 Skill 吗？有没有为了换工具重写过？
3. 如果有「写一次跑所有 Harness」的工具，你愿意付钱吗？多少？
4. 你最希望先支持哪些 Harness？

请到 [Discussions](https://github.com/sherryswift1019-gif/skillhub-seed/discussions) 留言，或开 Issue。Star 仓库 = 投票。

---

## Roadmap

- [x] 5 Skill × 3 Harness 手工转译（Phase 0）
- [ ] 100 GitHub star + 10 条独立用户跨平台关键词反馈（Phase 0 退出标准）
- [ ] 启动 SkillHub MVP：CLI + Registry + Web 站（Phase 1）
- [ ] 加 Gemini / Copilot / OpenCode 3 个 Harness（Phase 2）
- [ ] 商业化：付费精品 Skill + 企业版（Phase 3）

完整 PRD 在主仓库（链接将在公测时公开）。

---

## License & 致谢

本仓库 [MIT License](LICENSE)。

5 个 Skill（tdd-strict / brainstorming / systematic-debugging / code-review / verification-before-completion）的内容源自 [obra/superpowers](https://github.com/obra/superpowers)（Jesse Vincent 维护，MIT），按 IR 格式重新组织以适配各 Harness。每个 skill 文件头都标注了 upstream 来源。

`refactor` 是本仓库原创。

> 致谢 Jesse Vincent 把 superpowers 开源 — 没有这套基础工作，跨 Harness 转译验证无从谈起。
