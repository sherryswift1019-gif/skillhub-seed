# SkillHub IR (Intermediate Representation) — Draft v0.1

> 这是 Phase 0 的最小 IR 草稿。它不是 final spec — 跑完 Phase 0 验证后 Phase 1 才会冻结。

## 设计原则

1. **轻量**：基于 Markdown + YAML frontmatter，不引入新 DSL
2. **最小公约数**：先抽 5 大 Harness 共有的字段
3. **逃生通道**：Harness 特定字段走 `platform_specific.<name>` 段
4. **可验证**：每个字段有 JSON Schema 校验（Phase 1 落地）

## 完整 frontmatter 示例

```yaml
---
# === 标识 (required) ===
name: tdd-strict                  # kebab-case, 全局唯一
version: 1.0.0                    # semver
description: Use when implementing any feature or bugfix, before writing implementation code
description_zh: 任何特性或 bug 修复前，先用 TDD 流程

# === 归属 (required) ===
license: MIT                      # SPDX 标识符
author:
  name: Jesse Vincent
  email: jesse@example.com        # 可选
homepage: https://blog.fsck.com   # 可选
repository: github.com/obra/superpowers
upstream:                         # 如果是转译，标注上游
  source: github.com/obra/superpowers/skills/test-driven-development
  license: MIT

# === 触发 (optional, 启发式) ===
triggers:
  keywords: ["test", "tdd", "测试驱动"]
  file_patterns: ["**/*.test.ts", "**/*_test.py"]
  always_apply: false

# === 兼容性 (required) ===
compatibility:
  claude-code: ">=2.0"
  cursor: ">=0.40"
  codex: ">=1.5"
  gemini: false                   # 主动声明不兼容
  copilot: false
  opencode: false

# === 检索 (required) ===
tags: [testing, tdd, methodology]
category: testing                 # testing | debugging | design | review | refactor | meta
maturity: stable                  # experimental | beta | stable | deprecated

# === 依赖 (optional) ===
dependencies:
  - name: testing-anti-patterns
    version: "^1.0.0"

# === Harness 特定 (optional, 逃生通道) ===
platform_specific:
  cursor:
    globs: ["**/*.test.*", "**/*_test.*"]
    alwaysApply: false
  claude-code:
    allowed_tools: [Read, Edit, Bash]
  codex:
    permissions: ["read", "edit"]
---

# 正文：标准 Markdown 指令
# 各 Adapter 会把这部分包装到目标 Harness 的原生格式
```

## IR → 各 Harness 的映射

| IR 字段 | Claude Code | Cursor (.mdc) | Codex (manifest.toml) |
|---|---|---|---|
| `name` | 目录名 `~/.claude/skills/<name>/` | 文件名 `<name>.mdc` | `[plugin] name` |
| `description` | frontmatter `description` | frontmatter `description` | `[plugin] description` |
| `version` | frontmatter `version` | frontmatter `version` | `[plugin] version` |
| `triggers.always_apply` | 注入 description（Claude 自决） | `alwaysApply: true/false` | `[triggers] always_apply` |
| `triggers.file_patterns` | 注入 description 提示 | `globs: [...]` | `[triggers] file_patterns` |
| `triggers.keywords` | 注入 description | 注入正文头 | `[triggers] keywords` |
| 正文 | `SKILL.md` 全文 | `.mdc` 正文 | 相邻的 `SKILL.md` |
| `assets/` | 复制到 `.claude/skills/<name>/` | 复制到 `.cursor/assets/<name>/` | 复制到 plugin 目录 |
| `dependencies` | 嵌套安装 | 嵌套安装 | 嵌套安装 |
| `platform_specific.<X>` | 仅 X=claude-code 时生效 | 仅 X=cursor 时生效 | 仅 X=codex 时生效 |

## 已知限制

- Cursor 的 `manualOnly` Rule 类型 → 用 `triggers.always_apply: false` + 文档提示
- Claude Code 的 hooks → 不在 Skill 表达范围（属于 plugin/settings 层）
- Gemini 的复杂权限模型 → 走 `platform_specific.gemini`

## 待 Phase 1 决定的字段

- 多版本依赖解析（peer deps 风格）
- i18n 全字段（不只 description_zh）
- 安全声明（脚本沙箱级别、所需网络访问等）
- benchmark task_set 引用
