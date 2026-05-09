# Contributing

> Phase 0 阶段，本仓库主要由维护者手工转译。欢迎贡献，但请先看下方说明。

## 我们最需要的反馈

1. **Skill 在你 Harness 上不工作？** 开 Issue 说明：哪个 Skill / 哪个 Harness / 哪个版本 / 报错截图
2. **你有跨 Harness 的 Skill 转译需求？** 在 Discussions 留言：你用哪些 Harness？哪些 Skill 想要跨平台？
3. **格式建议？** IR 规范 [`docs/ir-spec.md`](docs/ir-spec.md) 是草稿，欢迎拍砖

## 想加新 Skill？

Phase 0 我们只接受**已在某个 Harness 已经被验证有效**的 Skill 转译。流程：

1. Fork
2. `mkdir -p skills/<your-skill-name>/{source,claude-code,cursor,codex}`
3. 在 `skills/<your-skill-name>/source/SKILL.md` 写 IR 源版本（参考 `skills/tdd-strict/source/SKILL.md`），包含：
   - 完整 frontmatter（name / version / description / license / triggers / compatibility / tags / category / maturity）
   - 可选：`platform_specific.<harness>.description` 给某个 Harness 单独写更短/更针对的描述
   - 可选：`platform_specific.claude-code.allowed_tools` 等 Harness 特定字段
   - 正文（Markdown）
4. **跑生成脚本**：
   ```bash
   pip3 install pyyaml  # 一次性
   python3 tools/generate_harness_versions.py
   ```
   脚本自动扫描 `skills/*/source/SKILL.md`，为每个 Skill 生成 3 Harness 的 4 个文件
5. 至少在 1 个目标 Harness 上手动测试（理想是 3 个全测）
6. 提 PR，附上：
   - License 声明（必须 MIT 兼容）
   - 上游来源（如有，写 `upstream:` 字段）
   - 你测试过的 Harness 列表

### 工具说明

`tools/generate_harness_versions.py`：
- `python3 tools/generate_harness_versions.py` — 全部生成
- `... --skill <name>` — 只生成某个 skill
- `... --check` — dry-run，不写
- `... -v` — 详细输出每个文件

**重要**：harness 子目录下的文件（claude-code/ / cursor/ / codex/）是**生成产物**，不要手动编辑。所有改动应该在 `source/SKILL.md`，然后跑脚本同步。手动编辑的话下次跑脚本会被覆盖。

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
