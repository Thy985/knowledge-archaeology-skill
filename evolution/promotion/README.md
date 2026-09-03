# Promotion —— Skill 晋升记录

> 晋升 = 新 Skill 版本对比旧版本的 Benchmark 指标。**必须用数据说话，不是"Prompt 改了一版，感觉应该更好了"。**

## 晋升门槛（Promotion Gate，硬门槛，不可放松）

| 指标 | 门槛 |
|------|------|
| regression | 必须 pass |
| critical_coverage | ≥ 0.90 |
| fidelity | ≥ 0.95 |
| abstraction_validity | ≥ 0.90 |
| false_acceptance | ≤ 0.10 |
| critical_regressions | = 0 |

**即使 Overall +10%，只要 Critical Coverage -4% → FAIL**——可能是用"多产生了一堆漂亮但错误的知识"换来的。

## v1 → v2/v3 晋升基准（Codex）

| 指标 | v1 | v2/v3 | 是否晋升 |
|------|----|-------|---------|
| Fidelity | ~0.90 | 0.96 | ✅ |
| Critical Coverage | 缺 3 大机制 | 0.94 | ✅ |
| Abstraction Validity | 0.78 | 0.91 | ✅ |
| False Acceptance | 0.43 | ~0.08 | ✅ |
| Critical Regressions | — | 0 | ✅ |
| **结论** | | | **PROMOTION PASS** |

## 记录格式

```markdown
## Promotion P-001 · v3.1 → v3.2
- Date: YYYY-MM-DD
- Benchmark: codex
- Old → New:
  - False Acceptance: X% → Y%
  - Critical Coverage: X → Y
- Gate result: PASS / FAIL
- 触发晋升的变更:
  - ...
```

> 注意：晋升判断只看"知识质量有没有变差"，不看"报告漂不漂亮"。
