---
# === SkillHub IR (中间表示) ===
name: tdd-strict
version: 1.0.0
description: Use when implementing any feature or bugfix, before writing implementation code
description_zh: 任何特性或 bug 修复实现前，先用 TDD 流程

license: MIT
author:
  name: Jesse Vincent
upstream:
  source: github.com/obra/superpowers/skills/test-driven-development
  license: MIT

triggers:
  keywords: ["test", "tdd", "test-driven", "测试驱动"]
  file_patterns: ["**/*.test.*", "**/*_test.*", "**/test_*.py"]
  always_apply: false

compatibility:
  claude-code: ">=2.0"
  cursor: ">=0.40"
  codex: ">=1.5"
  gemini: false
  copilot: false
  opencode: false

tags: [testing, tdd, methodology, red-green-refactor]
category: testing
maturity: stable

platform_specific:
  cursor:
    globs: ["**/*.test.*", "**/*_test.*", "**/test_*.py"]
    alwaysApply: false
  claude-code:
    allowed_tools: [Read, Edit, Bash]
---

# TDD Strict — Test-Driven Development

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code first? **Delete it. Start over.** No exceptions:
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

## When to Use

**Always:** new features, bug fixes, refactoring, behavior changes.

**Exceptions (ask your human partner):** throwaway prototypes, generated code, config files.

Thinking "skip TDD just this once"? Stop. That's rationalization.

## Red-Green-Refactor Cycle

### 1. RED — Write a failing test

```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const op = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };
  const result = await retryOperation(op);
  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```

Requirements: one behavior per test, clear name, real code (no mocks unless unavoidable).

### 2. Verify RED — Watch it fail (MANDATORY)

```bash
npm test path/to/test.test.ts
```

Confirm: test fails (not errors), failure message expected, fails because feature missing — not because of typos.

**Test passes immediately?** You're testing existing behavior. Fix the test.

### 3. GREEN — Minimal code

Write the simplest code that passes:

```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try { return await fn(); }
    catch (e) { if (i === 2) throw e; }
  }
  throw new Error('unreachable');
}
```

Don't add features, refactor other code, or "improve" beyond the test. **YAGNI.**

### 4. Verify GREEN — Watch it pass (MANDATORY)

Confirm: test passes, other tests still pass, output pristine (no warnings).

### 5. REFACTOR — Clean up (only after green)

Remove duplication, improve names, extract helpers. **Keep tests green. Don't add behavior.**

### 6. Repeat

Next failing test for next feature.

## Red Flags — STOP and Start Over

- Code written before test
- Test passes immediately on first run
- Can't explain why test failed
- "I'll write tests after"
- "Already manually tested"
- "Keep as reference and adapt"
- "Just this once / I'm being pragmatic"

All of these mean: **delete code, start with TDD.**

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Bug Fix Example

**Bug:** Empty email accepted.

```
RED      test('rejects empty email', async () => {
           const r = await submitForm({ email: '' });
           expect(r.error).toBe('Email required');
         });
Verify   FAIL: expected 'Email required', got undefined  ✓
GREEN    if (!data.email?.trim()) return { error: 'Email required' };
Verify   PASS  ✓
REFACTOR (skip — nothing to clean)
```

## Verification Checklist

Before marking work complete:

- [ ] Every new function has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for the expected reason
- [ ] Wrote minimal code to pass
- [ ] All tests pass, output pristine
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases covered

Can't check all boxes? You skipped TDD. Start over.

## Final Rule

```
Production code → test exists and failed first
Otherwise      → not TDD
```

No exceptions without your human partner's permission.

---

> **Source:** Adapted from [obra/superpowers test-driven-development](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) (MIT License, © Jesse Vincent and contributors). Condensed for cross-Harness format demonstration.
