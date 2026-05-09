---
# === SkillHub IR ===
name: systematic-debugging
version: 1.0.0
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes. 4-phase root cause process.
description_zh: 遇到 bug、测试失败、异常行为时使用，4 阶段根因分析，避免 patch-and-pray。

license: MIT
author:
  name: Jesse Vincent
upstream:
  source: github.com/obra/superpowers/skills/systematic-debugging
  license: MIT

triggers:
  keywords: ["bug", "debug", "error", "test failure", "调试", "排查"]
  file_patterns: []
  always_apply: false

compatibility:
  claude-code: ">=2.0"
  cursor: ">=0.40"
  codex: ">=1.5"
  gemini: false
  copilot: false
  opencode: false

tags: [debugging, root-cause, methodology]
category: debugging
maturity: stable

platform_specific:
  claude-code:
    allowed_tools: [Read, Edit, Bash, Grep]
  cursor:
    description: "Systematic debugging: 4-phase root cause process before any fix"
  codex:
    description: Use for any bug/test failure before proposing fixes
---

# Systematic Debugging

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Random fixes waste time and create new bugs. Quick patches mask underlying issues. **Symptom fixes are failure.**

## When to Use

ANY technical issue: test failures, production bugs, unexpected behavior, performance problems, build failures, integration issues.

**Especially when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple — simple bugs have root causes too
- You're in a hurry — rushing guarantees rework
- Manager wants it fixed NOW — systematic is faster than thrashing

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1 — Root Cause Investigation

BEFORE attempting ANY fix:

1. **Read error messages carefully** — don't skip past errors. Stack traces, line numbers, file paths, error codes
2. **Reproduce consistently** — exact steps. Every time? If not reproducible → gather more data, don't guess
3. **Check recent changes** — git diff, recent commits, new dependencies, config changes
4. **Gather evidence in multi-component systems** — for each component boundary, log what enters / exits / config state. Run once to see WHERE it breaks, then investigate that component
5. **Trace data flow** — where does the bad value originate? What called this with the bad value? Keep tracing up. Fix at source, not symptom

### Phase 2 — Pattern Analysis

1. **Find working examples** — similar working code in the same codebase
2. **Compare against references** — read reference implementations COMPLETELY, every line. Don't skim
3. **Identify differences** — list every difference, however small. Don't assume "that can't matter"
4. **Understand dependencies** — what other components, settings, configs, environment, assumptions

### Phase 3 — Hypothesis & Testing

1. **Form a single hypothesis** — "I think X is the root cause because Y". Write it down. Specific, not vague
2. **Test minimally** — smallest possible change to test the hypothesis. ONE variable at a time
3. **Verify before continuing** — worked? Phase 4. Didn't work? Form NEW hypothesis. DON'T pile on
4. **When you don't know** — say "I don't understand X". Don't pretend. Ask, research

### Phase 4 — Implementation

1. **Create a failing test case** — simplest reproduction. MUST exist before fixing. Use TDD skill.
2. **Implement single fix** — address the root cause. ONE change. No "while I'm here" improvements
3. **Verify fix** — test passes, no other tests broken, issue actually resolved
4. **If fix doesn't work**:
   - STOP. Count attempts.
   - < 3? Return to Phase 1, re-analyze with new info
   - **≥ 3? Question the architecture (step 5).** Don't try Fix #4 without that discussion

5. **3+ fixes failed → architectural problem**:
   - Each fix reveals new shared state / coupling / problem in different places
   - Fixes require "massive refactoring"
   - Each fix creates new symptoms elsewhere
   - **STOP** and discuss with your human partner. This isn't a failed hypothesis — this is wrong architecture.

## Red Flags — STOP and Restart Phase 1

- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**

## Real-World Impact

| Approach | Time-to-fix | First-time success | New bugs |
|---|---|---|---|
| Systematic | 15-30 min | 95% | Near zero |
| Random fixes | 2-3 hours of thrashing | 40% | Common |

---

> **Source:** Adapted from [obra/superpowers systematic-debugging](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) (MIT, © Jesse Vincent and contributors). Supporting techniques (`root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md`) available upstream.
