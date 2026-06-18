# Testing & Acceptance Report Template

## Test Report: [Feature/Module/Release]

**Version**: [X.Y.Z]
**Test Date**: YYYY-MM-DD
**Test Environment**: [Local / Staging / Production]
**Tester**: [Name/AI Agent]

---

## Test Summary | 测试摘要

| Metric | Value |
|---|---|
| Total Test Cases | N |
| Passed | N |
| Failed | N |
| Blocked | N |
| Pass Rate | XX% |

## Test Cases | 测试用例

### TC-001: [Happy Path]
- **Steps**: [Step-by-step]
- **Expected**: [What should happen]
- **Actual**: [What actually happened]
- **Status**: [PASS / FAIL]
- **Evidence**: [Screenshot / curl output / log]

### TC-002: [Edge Case]
[...]

## Regression Check | 回归检查

| Existing Feature | Status | Notes |
|---|---|---|
| [Feature 1] | PASS | — |
| [Feature 2] | PASS | — |

## Issues Found | 发现的问题

| ID | Severity | Description | Reproduction Steps | Status |
|---|---|---|---|---|
| BUG-001 | P0 | [...] | [...] | Open |
| BUG-002 | P2 | [...] | [...] | Fixed |

## Acceptance | 验收结论

- [ ] All P0/P1 test cases pass
- [ ] No regression on existing features
- [ ] Performance within acceptable range
- [ ] Documentation updated

**Decision**: [ACCEPTED / REJECTED / CONDITIONAL]
