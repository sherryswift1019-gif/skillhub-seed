---
# === SkillHub IR ===
name: verification-before-completion
version: 1.0.0
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
description_zh: 在声称工作完成/修复/通过前，必须先跑验证命令并核对输出。证据先于断言。

license: MIT
author:
  name: Jesse Vincent
upstream:
  source: github.com/obra/superpowers/skills/verification-before-completion
  license: MIT

triggers:
  keywords: ["complete", "done", "passing", "fixed", "verify", "完成", "通过", "修好"]
  file_patterns: []
  always_apply: false

compatibility:
  claude-code: ">=2.0"
  cursor: ">=0.40"
  codex: ">=1.5"
  gemini: false
  copilot: false
  opencode: false

tags: [verification, evidence, methodology, completion]
category: review
maturity: stable

platform_specific:
  claude-code:
    allowed_tools: [Read, Bash]
  cursor:
    description: "Verification gate: run the test/build/lint command BEFORE claiming work is complete"
  codex:
    description: Run verification command before claiming completion. Evidence before assertions.
---

# Verification Before Completion

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN:      Execute the FULL command (fresh, complete)
3. READ:     Full output, check exit code, count failures
4. VERIFY:   Does output confirm the claim?
             - If NO: State actual status with evidence
             - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|---|---|---|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|---|---|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.

---

> **Source:** Adapted from [obra/superpowers verification-before-completion](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) (MIT License, © Jesse Vincent and contributors).
