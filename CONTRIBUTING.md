# Contributing

> Phase 0 阶段，本仓库主要由维护者手工转译。欢迎贡献，但请先看下方说明。

## 我们最需要的反馈

1. **Skill 在你 Harness 上不工作？** 开 Issue 说明：哪个 Skill / 哪个 Harness / 哪个版本 / 报错截图
2. **你有跨 Harness 的 Skill 转译需求？** 在 Discussions 留言：你用哪些 Harness？哪些 Skill 想要跨平台？
3. **格式建议？** IR 规范 [`docs/ir-spec.md`](docs/ir-spec.md) 是草稿，欢迎拍砖

## 想加新 Skill？

Phase 0 我们只接受**已在某个 Harness 已经被验证有效**的 Skill 转译。流程：

1. Fork
2. 在 `skills/<your-skill-name>/source/SKILL.md` 写 IR 源版本（参考 `skills/tdd-strict/source/SKILL.md`）
3. 至少转译到 1 个目标 Harness（理想是 3 个全做）
4. 提 PR，附上：
   - License 声明（必须 MIT 兼容）
   - 上游来源（如有）
   - 你测试过的 Harness 列表

## 想加新 Harness 适配？

如 Gemini / Copilot / OpenCode：

1. 先在 `docs/harness-format-notes.md` 加该 Harness 的格式说明（路径、frontmatter、触发机制、工具权限模型）
2. 给 1 个 Skill 做 PoC 适配（建议从 `tdd-strict` 开始）
3. 提 PR

## 风格

- 中英文之间空格（Markdown）
- frontmatter 用 YAML，全 lowercase + kebab-case
- 文件名 kebab-case
- License attribution 必须在文件头或 README

## 行为准则

[Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/)。和善、专业、对事不对人。
